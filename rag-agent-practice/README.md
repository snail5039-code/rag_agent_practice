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
    │   └─ commerce · finance · law · medical · public
    │
    ├─ pipeline/               실행 순서대로
    │   ├─ extract.py          1. PDF → 글·표 추출, 이미지 위치 표시
    │   ├─ ocr_images.py       2. 이미지 OCR + 이미지 속 표
    │   ├─ find_figures.py     3. 그래프·다이어그램 찾기
    │   ├─ vision_gemini.py    4. Gemini로 그래프·다이어그램 → 마크다운
    │   ├─ chunk.py            5. 청킹 (논문=문단, 일반=300/50, 표=행 단위)
    │   └─ embed.py            6. 임베딩 → Chroma 저장, 검색 확인
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
    │   │   └─ base_300_50/     chunks.jsonl, STATS.md, preview/
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
python -m pipeline.chunk           # 5. 청킹 → output/chunks/base_300_50/
python -m pipeline.embed           # 6. 임베딩 → vectordb/ (.env 필요)
```

검색만 확인:

```bash
python -m pipeline.embed --query "보험업권 상생금융이 뭐야?" --k 5
```

## 현재 상태

| 단계 | 상태 |
|---|---|
| 추출 (글·표·OCR·Gemini) | 완료 - 59개 PDF, 1,258쪽 |
| 청킹 | 완료 - 300/50, 6,383개 |
| 임베딩·벡터DB | 완료 - gemini-embedding-2, Chroma 컬렉션 `base_300_50` |
| 골든셋 | 진행 전 |
| 검색기 비교·에이전트 | 진행 전 |
