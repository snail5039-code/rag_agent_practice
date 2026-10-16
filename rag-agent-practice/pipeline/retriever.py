"""검색기 모듈 - 에이전트와 평가 코드가 같은 검색기를 쓰도록 한곳에 모았다.

검색 방식
- similarity: Chroma 벡터 검색 (gemini-embedding-2, 코사인)
- mmr       : 벡터 후보 fetch_k개 중 다양성을 고려해 k개
- bm25      : Kiwi 형태소 토큰 + BM25Okapi
- hybrid    : similarity·bm25 각각 fetch_k개를 RRF(순위 합산)로 합쳐 k개

에이전트 검색 규칙 (검색 평가 267문제 결과로 결정)
- 표 질문이면 전체 청크 대상 MMR  (표 질문 48개: MMR hit@5 0.979 / MRR 0.856 으로 가장 좋음)
- 아니면 Hybrid                    (전체 hit@5 0.944 / MRR 0.839 로 가장 좋음)
- domain을 주면 그 분야 청크 안에서만 찾는다

흐름
    Retriever(config)
     [1] chunks.jsonl 읽기 -> chunk_id로 본문·메타데이터를 찾을 수 있게 사전으로
     [2] Chroma 컬렉션 열기(embed.get_store) -> similarity, mmr
     [3] BM25Search로 전체 청크 색인 (Kiwi 형태소, vectordb/bm25_<설정>.pkl에 저장해 두고 재사용)
    Retriever.search(query, is_table, domain, k)
     -> is_table이면 mmr(), 아니면 hybrid() -> 청크 dict 목록 (chunk_id, 파일명, 쪽, 본문 ...)

실행 (동작 확인용)
    python -m pipeline.retriever "보험업권 상생금융이 뭐야?"
    python -m pipeline.retriever "DC 퇴직연금에서 투자위험은 누가 부담하나요?" --table
"""

import sys
from pathlib import Path

# pipeline 폴더 안에서 python 파일명.py 로 바로 실행해도 pipeline 패키지를 찾게 한다
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import hashlib
import json
import pickle
import time
from collections import defaultdict

from rank_bm25 import BM25Okapi

from pipeline.chunk import CHUNK_DIR
from pipeline.embed import VECTORDB_DIR, get_store

RRF_C = 60  # RRF 상수 (순위 1등 = 1/61)
DOMAINS = ("finance", "public", "commerce", "law", "medical")


class BM25Search:
    """Kiwi로 형태소를 나눠 BM25로 검색한다. 조사·어미는 빼고 의미 있는 품사만 쓴다.

    청크를 형태소로 나누는 데 20초쯤 걸려서, cache_path를 주면 나눈 결과를 파일로 저장해 두고
    다음부터는 읽어 온다. 청크 본문이 하나라도 바뀌면(fingerprint가 다르면) 다시 만든다.
    """
    KEEP = ("NN", "NR", "NP", "VV", "VA", "XR", "SL", "SN", "SH", "MAG")

    def __init__(self, chunks, cache_path=None):
        from kiwipiepy import Kiwi
        self.kiwi = Kiwi()
        self.chunks = chunks
        t0 = time.time()
        fingerprint = hashlib.sha1("".join(c["chunk_id"] + c["text"] for c in chunks).encode()).hexdigest()
        cache = pickle.loads(cache_path.read_bytes()) if cache_path and cache_path.exists() else {}
        if cache.get("fingerprint") == fingerprint:
            corpus, how = cache["corpus"], "저장된 색인 사용"
        else:
            corpus, how = [self.tokenize(c["text"]) for c in chunks], "새로 만듦"
            if cache_path:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_bytes(pickle.dumps({"fingerprint": fingerprint, "corpus": corpus}))
        self.bm25 = BM25Okapi(corpus)
        print(f"  BM25 색인: 청크 {len(chunks)}개, {how} ({time.time() - t0:.1f}초)")

    def tokenize(self, text):
        return [t.form.lower() for t in self.kiwi.tokenize(text) if t.tag.startswith(self.KEEP)]

    def search(self, query, k, keep=None):
        """BM25 상위 k개. keep(청크 -> bool)을 주면 조건에 맞는 청크 중에서만 고른다."""
        scores = self.bm25.get_scores(self.tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.chunks[i] for i in order if keep is None or keep(self.chunks[i])][:k]


def rrf(*ranked_lists, top):
    """여러 순위 목록을 RRF로 합친다: 점수 = Σ 1 / (60 + 순위). 청크 dict에는 chunk_id가 있어야 한다."""
    scores, items = defaultdict(float), {}
    for ranked in ranked_lists:
        for rank, c in enumerate(ranked, start=1):
            scores[c["chunk_id"]] += 1 / (RRF_C + rank)
            items[c["chunk_id"]] = c
    return [items[cid] for cid in sorted(scores, key=lambda x: -scores[x])[:top]]


def load_chunk_rows(config):
    """chunks.jsonl -> 검색에 쓰는 평평한 dict 목록 (본문 + 주요 메타데이터)"""
    rows = []
    for line in (CHUNK_DIR / config / "chunks.jsonl").open(encoding="utf-8"):
        c = json.loads(line)
        m = c["metadata"]
        rows.append({"chunk_id": c["chunk_id"], "file_name": m["file_name"], "page_no": m["page_no"],
                     "domain": m["domain"], "content_type": m["content_type"], "text": c["text"]})
    return rows


class Retriever:
    def __init__(self, config="base_300_50", k=5, fetch_k=20):
        self.k, self.fetch_k = k, fetch_k
        # [1] 청크 읽기
        self.rows = load_chunk_rows(config)
        self.by_id = {r["chunk_id"]: r for r in self.rows}
        # [2] 벡터DB / [3] BM25 색인
        self.store = get_store(config)
        self.bm25_index = BM25Search(self.rows, cache_path=VECTORDB_DIR / f"bm25_{config}.pkl")

    def _docs(self, docs):
        # Chroma 결과(Document) -> chunks.jsonl의 청크 dict
        return [self.by_id[d.metadata["chunk_id"]] for d in docs]

    def similarity(self, query, k, domain=None):
        flt = {"domain": domain} if domain else None
        return self._docs(self.store.similarity_search(query, k=k, filter=flt))

    def mmr(self, query, k, domain=None):
        flt = {"domain": domain} if domain else None
        return self._docs(self.store.max_marginal_relevance_search(query, k=k, fetch_k=self.fetch_k, filter=flt))

    def bm25(self, query, k, domain=None):
        keep = (lambda c: c["domain"] == domain) if domain else None
        return self.bm25_index.search(query, k, keep=keep)

    def hybrid(self, query, k, domain=None):
        return rrf(self.similarity(query, self.fetch_k, domain), self.bm25(query, self.fetch_k, domain), top=k)

    def search(self, query, is_table=False, domain=None, k=None):
        """에이전트 검색: 표 질문이면 MMR, 아니면 Hybrid"""
        k = k or self.k
        domain = domain if domain in DOMAINS else None
        return self.mmr(query, k, domain) if is_table else self.hybrid(query, k, domain)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--table", action="store_true", help="표 질문으로 검색 (MMR)")
    parser.add_argument("--domain", choices=DOMAINS)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    r = Retriever(k=args.k)
    for i, c in enumerate(r.search(args.query, args.table, args.domain), start=1):
        print(f"[{i}] {c['file_name']} p.{c['page_no']} ({c['content_type']}) {c['chunk_id']}")
        print("    ", c["text"][:150].replace("\n", " "))


if __name__ == "__main__":
    main()
