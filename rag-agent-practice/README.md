### RAG Agent 실습

데이터 출처: [Allganize RAG-Evaluation-Dataset-KO](https://huggingface.co/datasets/allganize/RAG-Evaluation-Dataset-KO)

과제 안내는 [PRACTICE.md](PRACTICE.md), 설계·추출 정리는 [../docs/](../docs/)에 있다.

## 폴더 구조

```
rag_agent_practice/
├─ docs/                      설계·정리 문서
│   ├─ 설계.md                 처음 설계 메모
│   ├─ agent와_설계.md          결정한 설계 (파이프라인, 추출·청킹·검색 기준)
│   └─ 추출.md                 추출에 쓴 라이브러리·방법·결과 정리
│
└─ rag-agent-practice/
    ├─ README.md               (이 파일)
    ├─ PRACTICE.md             과제 안내
    ├─ .env                    GOOGLE_API_KEY (git 제외)
    │
    ├─ data/                   제공 PDF 59개 + golden_set.csv (git 제외)
    │   ├─ goldenset_my.csv     직접 만든 골든셋 77문제
    │   ├─ goldenset_all.csv    제공 + 내 골든셋 합본 309문제 (겹치는 35문제는 한 번만)
    │   └─ commerce · finance · law · medical · public
    │
    ├─ pipeline/               실행 순서대로
    │   ├─ extract.py          1. PDF → 글·표 추출, 이미지 위치 표시
    │   ├─ ocr_images.py       2. 이미지 OCR + 이미지 속 표
    │   ├─ find_figures.py     3. 그래프·다이어그램 찾기
    │   ├─ vision_gemini.py    4. Gemini로 그래프·다이어그램 → 마크다운
    │   ├─ chunk.py            5. 청킹 (논문=문단, 일반=300/50, 표=행 단위)
    │   ├─ embed.py            6. 임베딩 → Chroma 저장, 검색 확인
    │   ├─ evaluate_retrievers.py  7. 검색기 비교 평가 (similarity·MMR·BM25·Hybrid)
    │   ├─ retriever.py        검색기 (표 질문=MMR, 나머지=Hybrid)
    │   ├─ agent.py            8. RAG 에이전트 (검색 최대 3회, 답변/보류)
    │   └─ evaluate_agent.py   9. 에이전트 평가 (골든셋, openevals 채점)
    │
    ├─ experiments/            단발성 실험 (table_ocr.py: 표 구조 인식 시험)
    │
    ├─ output/
    │   ├─ extracted/          추출 결과
    │   │   ├─ INDEX.md         ← 여기서 파일별 미리보기를 연다
    │   │   ├─ jsonl/           페이지별 추출 데이터 (청킹 입력)
    │   │   ├─ preview/         파일별 미리보기 md
    │   │   ├─ images/          이미지 영역 PNG (OCR 대상)
    │   │   └─ figures/         그래프·다이어그램 PNG + Gemini 결과
    │   ├─ chunks/
    │   │   ├─ base_500_60/     기본(최종) - chunks.jsonl, STATS.md, preview/
    │   │   └─ base_300_50/, base_800_100/   비교용
    │   ├─ experiments/        실험 결과
    │   └─ logs/               실행 로그
    │
    └─ vectordb/               Chroma 벡터DB (git 제외, embed로 다시 생성)
```

## 실행 순서

모든 명령은 `rag-agent-practice/` 폴더에서 실행한다.

```bash
python -m pipeline.extract         # 1. 글·표 추출 (이어서 실행 가능)
python -m pipeline.ocr_images      # 2. 이미지 OCR + 이미지 속 표
python -m pipeline.find_figures    # 3. 그래프·다이어그램 찾기
python -m pipeline.vision_gemini   # 4. Gemini 변환 (.env 필요)
python -m pipeline.chunk           # 5. 청킹 → output/chunks/base_500_60/ (--size/--overlap로 변경)
python -m pipeline.embed           # 6. 임베딩 → vectordb/ (.env 필요)
python -m pipeline.evaluate_retrievers --golden data/goldenset_my.csv   # 7. 검색기 비교
python -m pipeline.agent "질문" --show-searches                          # 8. 에이전트에 질문 하나
python -m pipeline.evaluate_agent --limit 5                              # 9. 에이전트 평가 (앞 5문제로 확인)
python -m pipeline.evaluate_agent                                        #    전체 (끊겨도 다시 실행하면 이어서)
```

에이전트 평가 결과는 `output/eval/agent/<골든셋>__<청킹설정>__<모델>/report.md`에 저장된다.
모델: 에이전트 기본 `gemini-3.5-flash-lite` (`--model`로 변경), 채점은 `gemini-3.5-flash-lite`로 고정.
채점: 답변 정확도(openevals CORRECTNESS, LLM 채점), 근거 쪽 적중, 검색 적중, 보류 판단, 검색 횟수, 응답 시간.

검색만 확인:

```bash
python -m pipeline.embed --query "보험업권 상생금융이 뭐야?" --k 5
```

## 현재 상태

| 단계 | 상태 |
|---|---|
| 추출 (글·표·OCR·Gemini) | 완료 - 59개 PDF, 1,258쪽 |
| 청킹 | 완료 - 기본 500/60 (4,747개), 비교용 300/50 (6,382개)·800/100 (3,960개) |
| 임베딩·벡터DB | 완료 - gemini-embedding-2, Chroma 컬렉션 `base_500_60`·`base_300_50`·`base_800_100` |
| 골든셋 | 완료 - 내 골든셋 77문제, 합본 309문제, 비율 맞춰 뽑은 200문제 |
| 검색기 비교 | 완료 - 표 질문=MMR, 나머지=Hybrid |
| 에이전트 | 완료 - `pipeline/agent.py` (gemini-3.5-flash-lite) |
| 에이전트 평가 | 완료 - 309문제 정답률 0.810 (300/50), 청킹 비교는 아래 |

## 청킹 비교 (검색 방식 고정: 표=MMR, 나머지=Hybrid)

| 청킹 | 검색 Hybrid MRR (309문제) | 에이전트 정답률 (200문제, 1차/2차) | 평균 검색 | 평균 시간 |
|---|---|---|---|---|
| 300/50 | **0.830** | 0.786 / 0.796 | 1.77회 | 4.1초 |
| **500/60** | 0.819 | **0.827 / 0.811** | **1.60회** | **3.8초** |
| 800/100 | 0.812 | 0.806 / - | 1.54회 | 3.9초 |

- 검색 지표는 300/50이 가장 좋지만, 에이전트 정답률은 500/60이 두 번 모두 더 높아서 500/60 선택
- 같은 설정을 두 번 돌려도 정답률이 1~2%p 흔들린다 (LLM 응답이 매번 조금씩 다름). 차이는 약 3%p로 작다
- 표 질문 정답률은 세 설정 모두 0.55~0.61 -> 청킹으로는 해결되지 않음
