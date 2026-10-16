"""RAG 에이전트 평가 (골든셋으로 문제를 풀리고 채점)

채점 항목
- 답변 정확도: openevals CORRECTNESS_PROMPT (LLM 채점, 정답/오답)로 에이전트 답 vs target_answer
    - 답할 수 있는 문제인데 보류했으면 채점 없이 오답
    - 답변 불가 문제(answerable=false)는 보류했으면 정답, 답했으면 오답
- 근거 쪽 적중: 에이전트가 근거(citations)로 든 (파일명, 쪽)이 정답 쪽과 하나라도 같으면 적중
- 검색 적중: 검색한 청크 중 정답 쪽이 있었는지 (전체 검색 / 첫 검색만)
    -> "검색은 찾았는데 답이 틀림"과 "검색부터 못 찾음"을 나눠 보기 위함
- 보류 판단: 잘못된 보류(답할 수 있는데 보류) / 답변 불가 문제 보류
- 검색 횟수, 응답 시간

실행
    python -m pipeline.evaluate_agent --limit 5            # 앞 5문제만 먼저 확인
    python -m pipeline.evaluate_agent                      # 전체 (이미 푼 문제는 건너뛰고 이어서)
    python -m pipeline.evaluate_agent --ids my-03,gs-010   # 특정 문제만
    python -m pipeline.evaluate_agent --fresh              # 처음부터 다시
    python -m pipeline.evaluate_agent --report-only        # 저장된 결과로 보고서만 다시

결과: output/eval/agent/<골든셋>__<청킹설정>/details.jsonl (문제별), report.md (요약)

흐름
    main()
     [1] 골든셋 읽기(load_golden): 정답 쪽을 (파일명, 쪽) 집합으로, 답변 불가 문제도 포함
     [2] details.jsonl에서 이미 푼 문제 확인 -> 남은 문제만 (오류 난 문제는 다시)
     [3] RagAgent + 채점 LLM(create_llm_as_judge) 준비
     [4] 문제마다: agent.ask -> grade() 채점 -> details.jsonl에 한 줄씩 바로 저장 (중간에 끊겨도 이어서 가능)
     [5] summarize(): 전체 / 분야별 / 근거 유형별 / 출처별 -> 터미널 출력 + report.md
"""

import sys
from pathlib import Path

# pipeline 폴더 안에서 python 파일명.py 로 바로 실행해도 pipeline 패키지를 찾게 한다
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import csv
import json
import re
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from pipeline.evaluate_retrievers import norm_name
from pipeline.extract import BASE_DIR

EVAL_DIR = BASE_DIR / "output" / "eval" / "agent"


def load_golden(path):
    """골든셋 CSV -> 문제 목록. 여러 문서 정답은 "A.pdf || B.pdf", "1 || 13,14" 처럼 || 로 나눈다."""
    rows = []
    for i, r in enumerate(csv.DictReader(open(path, encoding="utf-8-sig"))):
        answerable = str(r.get("answerable", "true")).strip().lower() != "false"
        gold = set()
        if answerable:
            for fname, pages in zip(r["target_file_name"].split("||"), r["target_page_no"].split("||")):
                gold |= {(norm_name(fname), int(p)) for p in re.findall(r"\d+", pages)}
        rows.append({
            "qid": r.get("id") or str(i + 1), "domain": r.get("domain", ""),
            "context_type": r.get("context_type", ""), "source": r.get("source", ""),
            "question": r["question"], "target_answer": r.get("target_answer", ""),
            "answerable": answerable, "gold": gold,
        })
    return rows


def make_judge(model_name):
    """30-langgraph-evaluation 노트북과 같은 방식: CORRECTNESS_PROMPT + Gemini 채점"""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from openevals.llm import create_llm_as_judge
    from openevals.prompts import CORRECTNESS_PROMPT

    judge_llm = ChatGoogleGenerativeAI(model=model_name, timeout=120, max_retries=2)
    return create_llm_as_judge(prompt=CORRECTNESS_PROMPT, judge=judge_llm, feedback_key="answer_correct")


def page_keys(chunk_ids, by_id):
    return {(norm_name(by_id[cid]["file_name"]), by_id[cid]["page_no"]) for cid in chunk_ids if cid in by_id}


def grade(q, r, judge, by_id):
    """에이전트 실행 결과 r을 골든셋 문제 q로 채점한다."""
    withheld = r["status"] == "withheld"
    # 답변 정확도
    if not q["answerable"]:
        correct, comment = withheld, "답변 불가 문제: " + ("보류함" if withheld else "답을 지어냄")
    elif withheld:
        correct, comment = False, "답할 수 있는 문제인데 보류함"
    else:
        res = judge(inputs=q["question"], outputs=r["answer"], reference_outputs=q["target_answer"])
        correct, comment = bool(res["score"]), res.get("comment", "")

    # 근거 쪽·검색 적중 (답할 수 있는 문제만)
    cited = {(norm_name(c["file_name"]), int(c["page_no"])) for c in r["citations"]}
    first_ids = r["searches"][0]["chunk_ids"] if r["searches"] else []
    hits = {}
    if q["answerable"]:
        gold_files = {f for f, _ in q["gold"]}
        hits = {
            "citation_page_hit": bool(cited & q["gold"]),
            "citation_file_hit": bool({f for f, _ in cited} & gold_files),
            "retrieval_page_hit": bool(page_keys(r["retrieved_chunk_ids"], by_id) & q["gold"]),
            "first_search_page_hit": bool(page_keys(first_ids, by_id) & q["gold"]),
        }
    return {"correct": correct, "judge_comment": comment, **hits}


# ---------------- 요약 ----------------

def mean(vals):
    vals = list(vals)
    return sum(vals) / len(vals) if vals else None


def summarize(rows):
    ans = [r for r in rows if r["answerable"]]
    unans = [r for r in rows if not r["answerable"]]
    secs = sorted(r["elapsed_sec"] for r in rows)
    return {
        "n": len(rows), "n_answerable": len(ans), "n_unanswerable": len(unans),
        "answer_acc": mean(r["correct"] for r in ans),
        "acc_when_answered": mean(r["correct"] for r in ans if r["status"] == "answered"),
        "false_withhold": mean(r["status"] == "withheld" for r in ans),
        "unans_withheld": mean(r["status"] == "withheld" for r in unans),
        "citation_page_hit": mean(r["citation_page_hit"] for r in ans),
        "citation_file_hit": mean(r["citation_file_hit"] for r in ans),
        "retrieval_page_hit": mean(r["retrieval_page_hit"] for r in ans),
        "first_search_page_hit": mean(r["first_search_page_hit"] for r in ans),
        "avg_searches": mean(r["n_searches"] for r in rows),
        "searches_dist": {n: sum(r["n_searches"] == n for r in rows) for n in (1, 2, 3)},
        "avg_sec": mean(secs),
        "p90_sec": secs[int(len(secs) * 0.9)] if secs else None,
    }


COLS = [("answer_acc", "정답률"), ("acc_when_answered", "답한 것 중 정답"), ("false_withhold", "잘못된 보류"),
        ("citation_page_hit", "근거 쪽 적중"), ("retrieval_page_hit", "검색 적중"),
        ("first_search_page_hit", "첫 검색 적중"), ("avg_searches", "평균 검색"), ("avg_sec", "평균 초")]


def fmt(v, key):
    if v is None:
        return "-"
    return f"{v:.2f}" if key in ("avg_searches", "avg_sec") else f"{v:.3f}"


def group_table(title, groups):
    lines = [f"### {title}", "", "| 그룹 | 문제 | " + " | ".join(l for _, l in COLS) + " |",
             "|---|---|" + "---|" * len(COLS)]
    for name, s in groups:
        lines.append(f"| {name} | {s['n']} | " + " | ".join(fmt(s[k], k) for k, _ in COLS) + " |")
    return "\n".join(lines)


def write_report(rows, out_dir, golden_name, config, model):
    total = summarize(rows)
    md = [f"# 에이전트 평가 - {golden_name} / {config}", "",
          f"- 모델 {model}, 채점 openevals CORRECTNESS_PROMPT (정답/오답)",
          f"- 문제 {total['n']}개 (답할 수 있음 {total['n_answerable']}, 답변 불가 {total['n_unanswerable']})",
          "- 정답률·근거 쪽 적중·검색 적중은 답할 수 있는 문제 기준, 보류한 문제는 오답으로 셈", "",
          "## 전체", "",
          "| 지표 | 값 |", "|---|---|",
          f"| 정답률 | {fmt(total['answer_acc'], '')} |",
          f"| 답한 것 중 정답 | {fmt(total['acc_when_answered'], '')} |",
          f"| 잘못된 보류 (답할 수 있는데 보류) | {fmt(total['false_withhold'], '')} |",
          f"| 답변 불가 문제 보류 | {fmt(total['unans_withheld'], '')} |",
          f"| 근거 쪽 적중 | {fmt(total['citation_page_hit'], '')} |",
          f"| 근거 파일 적중 | {fmt(total['citation_file_hit'], '')} |",
          f"| 검색 적중 (전체 검색) | {fmt(total['retrieval_page_hit'], '')} |",
          f"| 검색 적중 (첫 검색만) | {fmt(total['first_search_page_hit'], '')} |",
          f"| 평균 검색 횟수 | {fmt(total['avg_searches'], 'avg_searches')} "
          f"(1회 {total['searches_dist'][1]} / 2회 {total['searches_dist'][2]} / 3회 {total['searches_dist'][3]}) |",
          f"| 평균 응답 시간 | {fmt(total['avg_sec'], 'avg_sec')}초 (p90 {fmt(total['p90_sec'], 'avg_sec')}초) |", ""]
    for key, label in (("domain", "분야별"), ("context_type", "근거 유형별"), ("source", "출처별")):
        vals = sorted({r[key] for r in rows if r[key]})
        md += [group_table(label, [(v, summarize([r for r in rows if r[key] == v])) for v in vals]), ""]

    def case(r):
        return (f"- **{r['qid']}** {r['question']}  \n  정답: {r['target_answer'][:150]}  \n"
                f"  에이전트[{r['status']}, 검색 {r['n_searches']}회]: {r['answer'][:150]}  \n"
                f"  채점: {r['judge_comment'][:200]}")

    fails = [
        ("답했는데 오답 - 검색은 정답 쪽을 찾음", lambda r: r["answerable"] and r["status"] == "answered"
         and not r["correct"] and r["retrieval_page_hit"]),
        ("답했는데 오답 - 검색도 못 찾음", lambda r: r["answerable"] and r["status"] == "answered"
         and not r["correct"] and not r["retrieval_page_hit"]),
        ("잘못된 보류", lambda r: r["answerable"] and r["status"] == "withheld"),
        ("답변 불가 문제에 답함", lambda r: not r["answerable"] and r["status"] != "withheld"),
    ]
    md += ["## 실패 사례", ""]
    for title, cond in fails:
        sel = [r for r in rows if cond(r)]
        md += [f"### {title} ({len(sel)})", ""] + ([case(r) for r in sel] or ["없음"]) + [""]
    (out_dir / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return total


def load_details(path):
    """문제별 마지막 기록만 (같은 문제를 다시 풀면 뒤 기록이 이긴다)"""
    done = {}
    if path.exists():
        for line in path.open(encoding="utf-8"):
            r = json.loads(line)
            done[r["qid"]] = r
    return done


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", default="data/goldenset_all.csv")
    parser.add_argument("--config", default="base_300_50")
    parser.add_argument("--limit", type=int, help="앞에서부터 N문제만")
    parser.add_argument("--ids", help="풀 문제 id (쉼표로 구분)")
    parser.add_argument("--workers", type=int, default=1, help="동시에 푸는 문제 수 (429가 나면 줄인다)")
    parser.add_argument("--fresh", action="store_true", help="이전 결과를 지우고 처음부터")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    # [1] 골든셋
    golden_path = BASE_DIR / args.golden
    golden = load_golden(golden_path)
    if args.ids:
        ids = set(args.ids.split(","))
        golden = [q for q in golden if q["qid"] in ids]
    if args.limit:
        golden = golden[:args.limit]

    out_dir = EVAL_DIR / f"{golden_path.stem}__{args.config}"
    out_dir.mkdir(parents=True, exist_ok=True)
    details_path = out_dir / "details.jsonl"
    if args.fresh and details_path.exists():
        details_path.unlink()

    # [2] 이미 푼 문제 건너뛰기 (오류 난 문제는 다시)
    done = load_details(details_path)
    todo = [q for q in golden if q["qid"] not in done or done[q["qid"]].get("error")]
    print(f"골든셋 {golden_path.name}: {len(golden)}문제 / 이미 채점 {len(golden) - len(todo)} / 이번에 {len(todo)}")

    model_name = None
    if todo and not args.report_only:
        # [3] 에이전트·채점 LLM
        from pipeline.agent import RagAgent
        agent = RagAgent(config=args.config)
        model_name = agent.model_name
        judge = make_judge(model_name)
        by_id = agent.retriever.by_id

        # 검색(BM25 Kiwi·Chroma)은 한 번에 하나씩: 여러 문제를 동시에 풀 때 안전하게
        search_lock, write_lock = threading.Lock(), threading.Lock()
        raw_search = agent.retriever.search

        def locked_search(*a, **kw):
            with search_lock:
                return raw_search(*a, **kw)
        agent.retriever.search = locked_search

        # [4] 풀고 채점
        def solve(q):
            base = {k: q[k] for k in ("qid", "domain", "context_type", "source", "question",
                                      "target_answer", "answerable")}
            base["gold"] = sorted(f"{f} p.{p}" for f, p in q["gold"])
            try:
                r = agent.ask(q["question"], save=False)
                return {**base, **{k: r[k] for k in ("status", "answer", "judgement", "citations", "n_searches",
                                                     "searches", "retrieved_chunk_ids", "elapsed_sec", "model")},
                        **grade(q, r, judge, by_id)}
            except Exception as e:
                return {**base, "error": f"{type(e).__name__}: {e}"}

        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = [ex.submit(solve, q) for q in todo]
            for i, fut in enumerate(as_completed(futures), start=1):
                row = fut.result()
                with write_lock, details_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                mark = "오류 " + row["error"][:80] if row.get("error") else ("O" if row["correct"] else "X")
                print(f"  [{i}/{len(todo)}] {row['qid']} {mark}", flush=True)

    # [5] 요약 (이번 골든셋 범위의 문제만, 오류는 빼고)
    done = load_details(details_path)
    qids = {q["qid"] for q in golden}
    rows = [r for qid, r in done.items() if qid in qids and not r.get("error")]
    errors = [r for qid, r in done.items() if qid in qids and r.get("error")]
    if not rows:
        print("채점된 문제가 없습니다.")
        return
    model_name = model_name or rows[0].get("model", "")
    total = write_report(rows, out_dir, golden_path.name, args.config, model_name)
    print(f"\n채점 {total['n']}문제 (오류 {len(errors)}개는 제외, 다시 실행하면 이어서 풂)")
    print(f"  정답률 {fmt(total['answer_acc'], '')} | 근거 쪽 적중 {fmt(total['citation_page_hit'], '')} | "
          f"잘못된 보류 {fmt(total['false_withhold'], '')} | 답변 불가 보류 {fmt(total['unans_withheld'], '')}")
    print(f"  평균 검색 {fmt(total['avg_searches'], 'avg_searches')}회 | 평균 {fmt(total['avg_sec'], 'avg_sec')}초")
    print(f"보고서: {out_dir / 'report.md'}")


if __name__ == "__main__":
    main()
