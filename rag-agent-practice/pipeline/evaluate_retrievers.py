"""검색기 비교 평가 (LLM 없이 검색 결과만 채점)

검색기 4개
- similarity: Chroma 벡터 검색 (gemini-embedding-2, 코사인)
- mmr       : 벡터 후보 fetch_k개 중 다양성을 고려해 k개
- bm25      : Kiwi 형태소 토큰 + BM25Okapi
- hybrid    : similarity·bm25 각각 fetch_k개를 RRF(순위 합산)로 합쳐 k개
- table_mmr_hybrid: 표 청크(content_type=table)는 MMR, 나머지 청크는 Hybrid로 따로 검색한 뒤
                    두 순위를 RRF로 합쳐 k개

채점: 검색된 청크의 (파일명, 쪽)이 골든셋 정답 (파일명, 쪽)과 같으면 정답
- 정답 쪽이 여러 개면 "23,24"처럼 쓴다 (하나만 찾아도 hit, recall은 찾은 비율)
- hit@k / precision@5 / recall@k / MRR / latency_ms
- 결과는 전체·분야별·근거 유형별로 묶어서 출력

실행
    python -m pipeline.evaluate_retrievers                                  # 내 골든셋
    python -m pipeline.evaluate_retrievers --golden data/golden_set.csv     # 제공 268문제
    python -m pipeline.evaluate_retrievers --strategies similarity,bm25

결과: output/eval/retrieval/<골든셋>__<청킹설정>/report.md, details.jsonl

흐름
    main()
     [1] 청크(chunks.jsonl) 읽기 -> 골든셋 읽기(load_golden)
         - 파일명은 norm_name()으로 맞춰 비교 (.pdf·공백·유니코드 차이 무시)
         - 답변 불가 문제는 빼고, "A.pdf || B.pdf" 처럼 여러 문서 정답도 처리
     [2] 검색기 준비(make_retrievers)
         - Chroma 컬렉션 열기(embed.get_store) -> similarity, mmr
         - BM25Search: 전체 청크를 Kiwi로 형태소 분석해 색인 (bm25, hybrid에서 사용)
         - hybrid: similarity·bm25 결과를 RRF로 합침
         - table_mmr_hybrid: 표 청크는 MMR, 나머지는 hybrid로 따로 찾아 RRF로 합침
     [3] 문제마다 × 검색기마다: 검색 -> 걸린 시간 측정 -> score()로 채점
     [4] summarize(): 검색기별 평균 -> 전체 / 분야별 / 근거 유형별 / 출처별로 묶기
     [5] 터미널에 표 출력(format_table) + report.md(format_md, 놓친 문제 목록) + details.jsonl 저장
"""

import sys
from pathlib import Path

# pipeline 폴더 안에서 python 파일명.py 로 바로 실행해도 pipeline 패키지를 찾게 한다
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import csv
import json
import re
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

from pipeline.chunk import CHUNK_DIR
from pipeline.embed import get_store
from pipeline.extract import BASE_DIR
from pipeline.retriever import RRF_C, BM25Search  # 에이전트와 같은 BM25 검색기

EVAL_DIR = BASE_DIR / "output" / "eval" / "retrieval"
STRATEGIES = ["similarity", "mmr", "bm25", "hybrid", "table_mmr_hybrid"]
METRICS = ["hit@1", "hit@3", "hit@5", "precision@5", "recall@3", "recall@5", "mrr", "latency_ms"]


def norm_name(name):
    """파일명 비교용: 유니코드 정규화, .pdf 제거, 공백 정리"""
    name = unicodedata.normalize("NFC", name or "").strip()
    name = re.sub(r"\.pdf$", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name)


def load_golden(path, known_files):
    """골든셋 CSV -> 문제 목록. 답변 불가(answerable=false) 문제는 정답 위치가 없어 검색 평가에서 뺀다.

    여러 문서에 걸친 정답은 "A.pdf || B.pdf", "1 || 13,14" 처럼 || 로 문서별로 나눠 쓴다.
    """
    rows, skipped = [], 0
    for i, r in enumerate(csv.DictReader(open(path, encoding="utf-8-sig"))):
        if str(r.get("answerable", "true")).strip().lower() == "false":
            skipped += 1
            continue
        files = [f for f in str(r["target_file_name"]).split("||")]
        page_groups = str(r["target_page_no"]).split("||")
        gold = set()
        for fname, pages in zip(files, page_groups):
            fname = norm_name(fname)
            if fname not in known_files:
                print(f"  [경고] {r.get('id') or i + 1} 문제의 파일을 찾을 수 없음: {fname}")
            gold |= {(fname, int(p)) for p in re.findall(r"\d+", pages)}
        rows.append({
            "qid": r.get("id") or i + 1, "domain": r.get("domain", ""),
            "context_type": r.get("context_type", ""), "source": r.get("source", ""),
            "question": r["question"], "gold": gold,
        })
    if skipped:
        print(f"  답변 불가 문제 {skipped}개는 검색 평가에서 제외")
    return rows


# ---------------- 검색기 ----------------

def doc_to_chunk(doc):
    """Chroma 검색 결과(Document) -> 채점에 필요한 {chunk_id, file_name, page_no}"""
    m = doc.metadata
    return {"chunk_id": m["chunk_id"], "file_name": m["file_name"], "page_no": m["page_no"]}


def make_retrievers(store, bm25, k, fetch_k):
    """검색기 이름 -> (질문 -> 상위 k개 청크) 함수 사전"""
    def similarity(q):
        return [doc_to_chunk(d) for d in store.similarity_search(q, k=k)]

    def mmr(q):
        return [doc_to_chunk(d) for d in store.max_marginal_relevance_search(q, k=k, fetch_k=fetch_k)]

    def bm25_search(q):
        return bm25.search(q, k)

    def rrf(*ranked_lists, top=k):
        # 여러 순위 목록을 RRF로 합친다: 점수 = Σ 1 / (60 + 순위)
        scores, items = defaultdict(float), {}
        for ranked in ranked_lists:
            for rank, c in enumerate(ranked, start=1):
                scores[c["chunk_id"]] += 1 / (RRF_C + rank)
                items[c["chunk_id"]] = c
        return [items[cid] for cid in sorted(scores, key=lambda x: -scores[x])[:top]]

    def hybrid(q):
        return rrf([doc_to_chunk(d) for d in store.similarity_search(q, k=fetch_k)],
                   bm25.search(q, fetch_k))

    def table_mmr_hybrid(q):
        # [표] 표 청크만 대상으로 MMR
        tables = [doc_to_chunk(d) for d in store.max_marginal_relevance_search(
            q, k=k, fetch_k=fetch_k, filter={"content_type": "table"})]
        # [나머지] 표가 아닌 청크만 대상으로 Hybrid (벡터 + BM25)
        others = rrf([doc_to_chunk(d) for d in store.similarity_search(
                          q, k=fetch_k, filter={"content_type": {"$ne": "table"}})],
                     bm25.search(q, fetch_k, keep=lambda c: c["content_type"] != "table"),
                     top=fetch_k)
        # 두 결과를 순위 기준으로 합쳐 상위 k개
        return rrf(tables, others)

    return {"similarity": similarity, "mmr": mmr, "bm25": bm25_search, "hybrid": hybrid,
            "table_mmr_hybrid": table_mmr_hybrid}


# ---------------- 채점 ----------------

def score(retrieved, gold):
    """검색 결과 한 번을 채점: 정답 쪽이 몇 등에 있는지로 hit@k, precision@5, recall@k, MRR 계산"""
    pages = [(norm_name(c["file_name"]), int(c["page_no"])) for c in retrieved]
    rel = [p in gold for p in pages]
    first = next((i + 1 for i, r in enumerate(rel) if r), None)
    found = lambda k: len({p for p in pages[:k] if p in gold}) / len(gold)
    return {
        "hit@1": float(any(rel[:1])), "hit@3": float(any(rel[:3])), "hit@5": float(any(rel[:5])),
        "precision@5": sum(rel[:5]) / 5, "recall@3": found(3), "recall@5": found(5),
        "mrr": 1 / first if first else 0.0, "rank": first,
    }


def summarize(results, strategies):
    """results: [{strategy, metrics...}] -> 검색기별 평균"""
    out = {}
    for s in strategies:
        rs = [r for r in results if r["strategy"] == s]
        if rs:
            out[s] = {"count": len(rs), **{m: sum(r[m] for r in rs) / len(rs) for m in METRICS}}
    return out


def format_table(title, summary):
    """터미널용 표 문자열"""
    head = f"{'strategy':>16} | {'count':>5} | " + " | ".join(f"{m:>11}" for m in METRICS)
    lines = [f"=== {title} ===", head, "-" * len(head)]
    for s, v in summary.items():
        vals = " | ".join(f"{v[m]:>11.1f}" if m == "latency_ms" else f"{v[m]:>11.3f}" for m in METRICS)
        lines.append(f"{s:>16} | {v['count']:>5} | {vals}")
    return "\n".join(lines)


def format_md(title, summary):
    """report.md용 마크다운 표"""
    lines = [f"### {title}", "", "| strategy | count | " + " | ".join(METRICS) + " |",
             "|---|---|" + "---|" * len(METRICS)]
    for s, v in summary.items():
        vals = " | ".join(f"{v[m]:.1f}" if m == "latency_ms" else f"{v[m]:.3f}" for m in METRICS)
        lines.append(f"| {s} | {v['count']} | {vals} |")
    return "\n".join(lines)


def main():
    """골든셋 × 검색기 채점 -> 표 출력·보고서 저장"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", default="data/golden_set.csv")
    parser.add_argument("--config", default="base_300_50")
    parser.add_argument("--strategies", default=",".join(STRATEGIES))
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--fetch-k", type=int, default=20)
    args = parser.parse_args()
    strategies = args.strategies.split(",")

    # [1] 청크·골든셋 읽기
    chunks = [json.loads(l) for l in (CHUNK_DIR / args.config / "chunks.jsonl").open(encoding="utf-8")]
    chunk_rows = [{"chunk_id": c["chunk_id"], "file_name": c["metadata"]["file_name"],
                   "page_no": c["metadata"]["page_no"], "content_type": c["metadata"]["content_type"],
                   "text": c["text"]} for c in chunks]
    golden_path = BASE_DIR / args.golden
    golden = load_golden(golden_path, {norm_name(c["file_name"]) for c in chunk_rows})
    print(f"골든셋 {golden_path.name}: {len(golden)}문제 / 청크 {args.config}: {len(chunks)}개")

    # [2] 검색기 준비
    store, _ = get_store(args.config)
    bm25 = BM25Search(chunk_rows) if {"bm25", "hybrid", "table_mmr_hybrid"} & set(strategies) else None
    retrievers = make_retrievers(store, bm25, args.k, args.fetch_k)

    # [3] 검색·채점
    results = []
    for q in golden:
        for s in strategies:
            t0 = time.perf_counter()
            retrieved = retrievers[s](q["question"])
            latency = (time.perf_counter() - t0) * 1000
            results.append({
                "qid": q["qid"], "strategy": s, "domain": q["domain"], "context_type": q["context_type"],
                "source": q["source"],
                "question": q["question"], "gold": sorted(f"{f} p.{p}" for f, p in q["gold"]),
                **score(retrieved, q["gold"]), "latency_ms": latency,
                "retrieved": [f"{c['chunk_id']}" for c in retrieved],
            })
        print(f"  {q['qid']}/{len(golden)}", end="\r", flush=True)
    print()

    # [4] 전체 / 분야별 / 근거 유형별 / 출처별로 묶기
    sections = [("전체", summarize(results, strategies))]
    for key, label in (("domain", "분야"), ("context_type", "근거 유형"), ("source", "출처")):
        for val in sorted({r[key] for r in results if r[key]}):
            sections.append((f"{label}: {val}", summarize([r for r in results if r[key] == val], strategies)))

    for title, summary in sections:
        print(format_table(title, summary), "\n")

    # [5] 저장
    out_dir = EVAL_DIR / f"{golden_path.stem}__{args.config}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "details.jsonl").open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    md = [f"# 검색 평가 - {golden_path.name} / {args.config}", "",
          f"- 문제 {len(golden)}개, k={args.k}, MMR·Hybrid 후보 fetch_k={args.fetch_k}, Hybrid=RRF(c={RRF_C})",
          "- 정답 판정: 검색된 청크의 (파일명, 쪽)이 정답과 같으면 정답", ""]
    md += [format_md(t, s) + "\n" for t, s in sections]
    md += ["## 놓친 문제 (top-5 안에 정답 쪽 없음)", ""]
    misses = [r for r in results if not r["hit@5"]]
    if not misses:
        md.append("없음")
    for r in misses:
        md.append(f"- [{r['strategy']}] Q{r['qid']} {r['question']}  \n  정답: {', '.join(r['gold'])}  \n"
                  f"  검색: {', '.join(r['retrieved'][:3])}")
    (out_dir / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"보고서: {out_dir / 'report.md'}")


if __name__ == "__main__":
    main()
