# 검색 평가 - goldenset_my.csv / base_300_50

- 문제 73개, k=5, MMR·Hybrid 후보 fetch_k=20, Hybrid=RRF(c=60)
- 정답 판정: 검색된 청크의 (파일명, 쪽)이 정답과 같으면 정답

### 전체

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 73 | 0.712 | 0.904 | 0.945 | 0.395 | 0.874 | 0.927 | 0.796 | 457.7 |
| mmr | 73 | 0.712 | 0.863 | 0.877 | 0.238 | 0.847 | 0.861 | 0.779 | 467.1 |
| bm25 | 73 | 0.603 | 0.781 | 0.822 | 0.282 | 0.751 | 0.792 | 0.692 | 35.0 |
| hybrid | 73 | 0.753 | 0.890 | 0.932 | 0.359 | 0.861 | 0.902 | 0.822 | 490.2 |
| table_mmr_hybrid | 73 | 0.027 | 0.753 | 0.836 | 0.247 | 0.740 | 0.813 | 0.411 | 1003.7 |

### 분야: commerce

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 3 | 0.333 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 0.556 | 629.3 |
| mmr | 3 | 0.333 | 0.667 | 0.667 | 0.200 | 0.667 | 0.667 | 0.500 | 476.5 |
| bm25 | 3 | 0.333 | 0.667 | 0.667 | 0.333 | 0.667 | 0.667 | 0.500 | 15.9 |
| hybrid | 3 | 0.333 | 0.667 | 1.000 | 0.333 | 0.667 | 1.000 | 0.583 | 508.3 |
| table_mmr_hybrid | 3 | 0.000 | 0.333 | 0.667 | 0.200 | 0.333 | 0.667 | 0.250 | 1002.8 |

### 분야: finance

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 4 | 0.750 | 0.750 | 0.750 | 0.400 | 0.625 | 0.750 | 0.750 | 453.8 |
| mmr | 4 | 0.750 | 0.750 | 0.750 | 0.250 | 0.750 | 0.750 | 0.750 | 457.0 |
| bm25 | 4 | 0.250 | 0.750 | 0.750 | 0.300 | 0.750 | 0.750 | 0.458 | 17.7 |
| hybrid | 4 | 0.500 | 0.750 | 0.750 | 0.350 | 0.625 | 0.625 | 0.625 | 457.7 |
| table_mmr_hybrid | 4 | 0.000 | 0.500 | 0.750 | 0.200 | 0.500 | 0.625 | 0.312 | 981.8 |

### 분야: law

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 1 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 1.000 | 0.200 | 448.4 |
| mmr | 1 | 0.000 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 0.333 | 556.2 |
| bm25 | 1 | 1.000 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 28.4 |
| hybrid | 1 | 1.000 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 1.000 | 476.8 |
| table_mmr_hybrid | 1 | 1.000 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1017.8 |

### 분야: medical

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 27 | 0.556 | 0.889 | 0.926 | 0.348 | 0.827 | 0.877 | 0.699 | 449.4 |
| mmr | 27 | 0.556 | 0.815 | 0.852 | 0.215 | 0.772 | 0.809 | 0.668 | 466.8 |
| bm25 | 27 | 0.222 | 0.481 | 0.593 | 0.215 | 0.401 | 0.512 | 0.359 | 25.0 |
| hybrid | 27 | 0.630 | 0.778 | 0.852 | 0.311 | 0.716 | 0.790 | 0.702 | 467.9 |
| table_mmr_hybrid | 27 | 0.037 | 0.630 | 0.667 | 0.178 | 0.593 | 0.623 | 0.343 | 978.6 |

### 분야: public

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 38 | 0.868 | 0.947 | 0.974 | 0.437 | 0.947 | 0.974 | 0.904 | 450.8 |
| mmr | 38 | 0.868 | 0.921 | 0.921 | 0.258 | 0.921 | 0.921 | 0.895 | 465.3 |
| bm25 | 38 | 0.921 | 1.000 | 1.000 | 0.326 | 1.000 | 1.000 | 0.961 | 45.7 |
| hybrid | 38 | 0.895 | 1.000 | 1.000 | 0.395 | 1.000 | 1.000 | 0.943 | 508.4 |
| table_mmr_hybrid | 38 | 0.000 | 0.895 | 0.974 | 0.305 | 0.895 | 0.974 | 0.467 | 1023.6 |

### 근거 유형: image

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 2 | 0.500 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 0.667 | 459.2 |
| mmr | 2 | 0.500 | 1.000 | 1.000 | 0.200 | 1.000 | 1.000 | 0.750 | 505.2 |
| bm25 | 2 | 0.500 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 0.750 | 18.8 |
| hybrid | 2 | 0.500 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 0.750 | 471.4 |
| table_mmr_hybrid | 2 | 0.000 | 0.500 | 1.000 | 0.300 | 0.500 | 1.000 | 0.375 | 1004.0 |

### 근거 유형: paragraph

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 68 | 0.735 | 0.926 | 0.956 | 0.394 | 0.895 | 0.936 | 0.817 | 457.5 |
| mmr | 68 | 0.735 | 0.868 | 0.882 | 0.241 | 0.850 | 0.865 | 0.795 | 464.8 |
| bm25 | 68 | 0.603 | 0.765 | 0.809 | 0.274 | 0.733 | 0.777 | 0.687 | 35.9 |
| hybrid | 68 | 0.765 | 0.897 | 0.941 | 0.359 | 0.865 | 0.909 | 0.831 | 491.9 |
| table_mmr_hybrid | 68 | 0.015 | 0.765 | 0.838 | 0.247 | 0.750 | 0.814 | 0.408 | 1003.9 |

### 근거 유형: table

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 3 | 0.333 | 0.333 | 0.667 | 0.333 | 0.333 | 0.667 | 0.400 | 461.2 |
| mmr | 3 | 0.333 | 0.667 | 0.667 | 0.200 | 0.667 | 0.667 | 0.444 | 494.2 |
| bm25 | 3 | 0.667 | 1.000 | 1.000 | 0.333 | 1.000 | 1.000 | 0.778 | 25.6 |
| hybrid | 3 | 0.667 | 0.667 | 0.667 | 0.333 | 0.667 | 0.667 | 0.667 | 464.2 |
| table_mmr_hybrid | 3 | 0.333 | 0.667 | 0.667 | 0.200 | 0.667 | 0.667 | 0.500 | 999.4 |

### 출처: golden_set.csv

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 35 | 0.857 | 0.943 | 0.971 | 0.440 | 0.943 | 0.971 | 0.896 | 451.4 |
| mmr | 35 | 0.857 | 0.914 | 0.914 | 0.246 | 0.914 | 0.914 | 0.886 | 465.9 |
| bm25 | 35 | 0.914 | 1.000 | 1.000 | 0.337 | 1.000 | 1.000 | 0.957 | 48.2 |
| hybrid | 35 | 0.886 | 1.000 | 1.000 | 0.400 | 1.000 | 1.000 | 0.938 | 512.5 |
| table_mmr_hybrid | 35 | 0.000 | 0.886 | 0.971 | 0.309 | 0.886 | 0.971 | 0.464 | 1017.8 |

### 출처: medical_v1

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 26 | 0.538 | 0.885 | 0.923 | 0.331 | 0.821 | 0.872 | 0.687 | 449.2 |
| mmr | 26 | 0.538 | 0.808 | 0.846 | 0.215 | 0.763 | 0.801 | 0.655 | 464.3 |
| bm25 | 26 | 0.192 | 0.462 | 0.577 | 0.200 | 0.378 | 0.494 | 0.335 | 25.0 |
| hybrid | 26 | 0.615 | 0.769 | 0.846 | 0.300 | 0.705 | 0.782 | 0.690 | 467.8 |
| table_mmr_hybrid | 26 | 0.038 | 0.615 | 0.654 | 0.169 | 0.577 | 0.609 | 0.337 | 976.3 |

### 출처: my

| strategy | count | hit@1 | hit@3 | hit@5 | precision@5 | recall@3 | recall@5 | mrr | latency_ms |
|---|---|---|---|---|---|---|---|---|---|
| similarity | 12 | 0.667 | 0.833 | 0.917 | 0.400 | 0.792 | 0.917 | 0.739 | 494.7 |
| mmr | 12 | 0.667 | 0.833 | 0.833 | 0.267 | 0.833 | 0.833 | 0.736 | 476.6 |
| bm25 | 12 | 0.583 | 0.833 | 0.833 | 0.300 | 0.833 | 0.833 | 0.694 | 18.3 |
| hybrid | 12 | 0.667 | 0.833 | 0.917 | 0.367 | 0.792 | 0.875 | 0.771 | 473.7 |
| table_mmr_hybrid | 12 | 0.083 | 0.667 | 0.833 | 0.233 | 0.667 | 0.792 | 0.417 | 1022.1 |

## 놓친 문제 (top-5 안에 정답 쪽 없음)

- [similarity] Qmy-03 DC 퇴직연금에서 투자위험은 누가 부담하나요?  
  정답: 한-호주 퇴직연금 포럼_책자(최종) p.27  
  검색: finance/한-호주 퇴직연금 포럼_책자(최종)/p032/c02, finance/한-호주 퇴직연금 포럼_책자(최종)/p032/c01, finance/한-호주 퇴직연금 포럼_책자(최종)/p031/c00
- [mmr] Qmy-03 DC 퇴직연금에서 투자위험은 누가 부담하나요?  
  정답: 한-호주 퇴직연금 포럼_책자(최종) p.27  
  검색: finance/한-호주 퇴직연금 포럼_책자(최종)/p032/c02, finance/한-호주 퇴직연금 포럼_책자(최종)/p002/c01, finance/한-호주 퇴직연금 포럼_책자(최종)/p030/c01
- [hybrid] Qmy-03 DC 퇴직연금에서 투자위험은 누가 부담하나요?  
  정답: 한-호주 퇴직연금 포럼_책자(최종) p.27  
  검색: finance/한-호주 퇴직연금 포럼_책자(최종)/p032/c01, finance/한-호주 퇴직연금 포럼_책자(최종)/p030/c01, finance/한-호주 퇴직연금 포럼_책자(최종)/p031/c00
- [table_mmr_hybrid] Qmy-03 DC 퇴직연금에서 투자위험은 누가 부담하나요?  
  정답: 한-호주 퇴직연금 포럼_책자(최종) p.27  
  검색: public/(240411보도자료) 재정동향 4월호/p002/c08, finance/한-호주 퇴직연금 포럼_책자(최종)/p032/c01, law/[행정] 타인자금(예금, 보험료 등 고객의 예탁자금)이 아닌 자기자금(자본금, 대출금 등 자신의 고유재산)을 운용하는 경우에도 공정거래법 제11/p031/c01
- [mmr] Qmy-07 국내 이커머스 시장 변화를 알려줘  
  정답: 쿠팡 상장과 이베이 인수 이후 국내 이커머스 시장은 어떻게 변할까 p.10  
  검색: commerce/MezzoMedia 산업 보고서 e커머스/p003/c01, commerce/이커머스 솔루션 소개자료/p003/c00, commerce/쿠팡 상장과 이베이 인수  이후 국내 이커머스 시장은 어떻게 변할까/p005/c01
- [bm25] Qmy-07 국내 이커머스 시장 변화를 알려줘  
  정답: 쿠팡 상장과 이베이 인수 이후 국내 이커머스 시장은 어떻게 변할까 p.10  
  검색: commerce/쿠팡 상장과 이베이 인수  이후 국내 이커머스 시장은 어떻게 변할까/p005/c01, commerce/쿠팡 상장과 이베이 인수  이후 국내 이커머스 시장은 어떻게 변할까/p004/c02, commerce/쿠팡 상장과 이베이 인수  이후 국내 이커머스 시장은 어떻게 변할까/p005/c02
- [table_mmr_hybrid] Qmy-07 국내 이커머스 시장 변화를 알려줘  
  정답: 쿠팡 상장과 이베이 인수 이후 국내 이커머스 시장은 어떻게 변할까 p.10  
  검색: commerce/쿠팡 상장과 이베이 인수  이후 국내 이커머스 시장은 어떻게 변할까/p001/c03, commerce/쿠팡 상장과 이베이 인수  이후 국내 이커머스 시장은 어떻게 변할까/p005/c02, commerce/MezzoMedia 산업 보고서 e커머스/p015/c02
- [bm25] Qmy-10 금융기관의 고령화 대책은 뭐가 있어?  
  정답: 130292099630937500_KIFVIP2013-10 p.23, 130292099630937500_KIFVIP2013-10 p.24  
  검색: finance/130292099630937500_KIFVIP2013-10/p003/c00, finance/130292099630937500_KIFVIP2013-10/p047/c01, finance/130292099630937500_KIFVIP2013-10/p006/c01
- [mmr] Qpub-16 지금까지 학교도서관이 주로 수행해왔던 기능들과 그것이 디지털 시대에 직면한 새로운 독서교육 요구에 어떻게 부응해야 하는지 서술해주세요.  
  정답: 제4차(24_28)+학교도서관+진흥+기본계획 p.9  
  검색: public/제4차(24_28)+학교도서관+진흥+기본계획/p003/c01, public/제4차(24_28)+학교도서관+진흥+기본계획/p019/c03, public/제4차(24_28)+학교도서관+진흥+기본계획/p017/c00
- [table_mmr_hybrid] Qpub-16 지금까지 학교도서관이 주로 수행해왔던 기능들과 그것이 디지털 시대에 직면한 새로운 독서교육 요구에 어떻게 부응해야 하는지 서술해주세요.  
  정답: 제4차(24_28)+학교도서관+진흥+기본계획 p.9  
  검색: public/제4차(24_28)+학교도서관+진흥+기본계획/p030/c03, public/제4차(24_28)+학교도서관+진흥+기본계획/p003/c01, public/제4차(24_28)+학교도서관+진흥+기본계획/p012/c05
- [similarity] Qpub-20 2024년 세계경제 성장 및 교역 전망치를 바탕으로 미국, 중국, 독일, 대만의 경제 성장률 전망이 어떻게 달라지는지 설명해주세요.  
  정답: 2024년 주요업무 추진계획 p.4  
  검색: public/2023_2027 국가재정운용계획 주요내용/p004/c02, finance/2024년 3월_3. 향후 통화신용정책 방향/p008/c00, finance/2024년 3월_3. 향후 통화신용정책 방향/p008/c01
- [mmr] Qpub-20 2024년 세계경제 성장 및 교역 전망치를 바탕으로 미국, 중국, 독일, 대만의 경제 성장률 전망이 어떻게 달라지는지 설명해주세요.  
  정답: 2024년 주요업무 추진계획 p.4  
  검색: public/2023_2027 국가재정운용계획 주요내용/p004/c02, finance/2024년 3월_3. 향후 통화신용정책 방향/p008/c00, finance/★2019 제1회 증시콘서트 자료집_최종★/p023/c05
- [mmr] Qpub-32 2023년 기준 앙골라와의 교역규모는 얼마이며, 대앙골라 누계 투자액은 2022년 기준으로 얼마인가요?  
  정답: 외교부-2024년 앙골라개황(저) p.36  
  검색: public/외교부-2024년 앙골라개황(저)/p019/c04, public/외교부-2024년 앙골라개황(저)/p008/c04, public/외교부-2024년 앙골라개황(저)/p025/c00
- [similarity] Qsymptom-before-result 밥 먹고 나면 소화가 안 되고 속이 쓰려서 위 내시경을 했는데, 결과 나오기 전에 어떤 병인지 미리 알 수 있을까요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.8  
  검색: medical/20080813_E_2/p017/c00, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p005/c07, medical/14.cancer_info/p008/c06
- [mmr] Qsymptom-before-result 밥 먹고 나면 소화가 안 되고 속이 쓰려서 위 내시경을 했는데, 결과 나오기 전에 어떤 병인지 미리 알 수 있을까요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.8  
  검색: medical/20080813_E_2/p017/c00, medical/14.cancer_info/p008/c06, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p005/c01
- [bm25] Qsymptom-before-result 밥 먹고 나면 소화가 안 되고 속이 쓰려서 위 내시경을 했는데, 결과 나오기 전에 어떤 병인지 미리 알 수 있을까요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.8  
  검색: medical/14.cancer_info/p008/c05, medical/14.cancer_info/p008/c00, medical/14.cancer_info/p008/c06
- [hybrid] Qsymptom-before-result 밥 먹고 나면 소화가 안 되고 속이 쓰려서 위 내시경을 했는데, 결과 나오기 전에 어떤 병인지 미리 알 수 있을까요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.8  
  검색: medical/14.cancer_info/p008/c06, medical/14.cancer_info/p004/c02, medical/14.cancer_info/p008/c00
- [table_mmr_hybrid] Qsymptom-before-result 밥 먹고 나면 소화가 안 되고 속이 쓰려서 위 내시경을 했는데, 결과 나오기 전에 어떤 병인지 미리 알 수 있을까요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.8  
  검색: medical/08 알기 쉬운 대장암/p007/c02, medical/14.cancer_info/p008/c06, medical/20080813_E_2/p014/c01
- [bm25] Qheartburn-timing 속쓰림이 주로 식후에 생기는데, 보통 식사하고 얼마 뒤에 시작해서 얼마나 가나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.3  
  검색: medical/14.cancer_info/p008/c02, medical/14.cancer_info/p008/c03, medical/14.cancer_info/p008/c00
- [table_mmr_hybrid] Qheartburn-timing 속쓰림이 주로 식후에 생기는데, 보통 식사하고 얼마 뒤에 시작해서 얼마나 가나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.3  
  검색: medical/[3.22.목.석간]질병관리본부_-_대한안과학회,_눈건강_관리를_위한_9대_생활수칙_발표/p001/c00, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p009/c04, medical/08 알기 쉬운 대장암/p007/c02
- [bm25] Qacid-overproduction 저는 위산이 너무 많이 나와서 속이 쓰린 건가요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.1  
  검색: medical/jkan-38-140/p009/c10, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p005/c00, medical/14.cancer_info/p008/c05
- [table_mmr_hybrid] Qacid-overproduction 저는 위산이 너무 많이 나와서 속이 쓰린 건가요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.1  
  검색: medical/08 알기 쉬운 대장암/p007/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p005/c01, medical/20080813_E_2/p014/c01
- [bm25] Qph-test-indication 24시간 식도 산도 검사는 속쓰림이 있으면 누구나 먼저 받는 검사인가요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.9  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p008/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p008/c04, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p007/c02
- [table_mmr_hybrid] Qph-test-indication 24시간 식도 산도 검사는 속쓰림이 있으면 누구나 먼저 받는 검사인가요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.9  
  검색: medical/20080813_E_2/p014/c01, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p008/c04, medical/08 알기 쉬운 대장암/p007/c02
- [mmr] Qppi-duration 역류성 식도염 약은 얼마나 오래 먹어야 해요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.11, 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.14  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p013/c04, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p015/c03, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02
- [bm25] Qppi-duration 역류성 식도염 약은 얼마나 오래 먹어야 해요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.11, 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.14  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p006/c03, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p003/c03
- [hybrid] Qppi-duration 역류성 식도염 약은 얼마나 오래 먹어야 해요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.11, 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.14  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p013/c04, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p015/c03
- [table_mmr_hybrid] Qppi-duration 역류성 식도염 약은 얼마나 오래 먹어야 해요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.11, 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.14  
  검색: medical/[3.22.목.석간]질병관리본부_-_대한안과학회,_눈건강_관리를_위한_9대_생활수칙_발표/p001/c00, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02, medical/08 알기 쉬운 대장암/p007/c02
- [table_mmr_hybrid] Qrecurrence-after-stop 약 먹고 증상이 좋아졌는데 끊으면 다시 아플 수 있나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.14  
  검색: medical/[3.22.목.석간]질병관리본부_-_대한안과학회,_눈건강_관리를_위한_9대_생활수칙_발표/p001/c00, medical/jkan-38-140/p008/c05, medical/08 알기 쉬운 대장암/p007/c02
- [bm25] Qpregnancy-heartburn 임신 중인데 속쓰림이 심해요. 약을 먹어도 되나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.11  
  검색: medical/14.cancer_info/p008/c05, medical/14.cancer_info/p003/c04, medical/jkan-38-140/p007/c00
- [mmr] Qh2ra-long-term 속쓰림 약(H2 차단제)을 계속 매일 먹어도 되나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.15  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p011/c01, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p007/c04, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p002/c02
- [bm25] Qreflux-complication 역류성 식도염이 오래되면 어떤 합병증이 생길 수 있나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.4  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p006/c03, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c03
- [hybrid] Qreflux-complication 역류성 식도염이 오래되면 어떤 합병증이 생길 수 있나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.4  
  검색: medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p008/c01, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p003/c01
- [table_mmr_hybrid] Qreflux-complication 역류성 식도염이 오래되면 어떤 합병증이 생길 수 있나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.4  
  검색: medical/2017년-안과감염병-관리지침/p015/c02, medical/위식도역류성질환(Gastroesophageal Reflux Disease) (2)/p010/c02, medical/[3.22.목.석간]질병관리본부_-_대한안과학회,_눈건강_관리를_위한_9대_생활수칙_발표/p001/c00
- [bm25] Qkcab-with-meal 케이캡(테고프라잔)은 식사와 상관없이 먹어도 되나요? 얼마나 먹나요?  
  정답: 위식도역류성질환(Gastroesophageal Reflux Disease) (2) p.2  
  검색: medical/14.cancer_info/p008/c00, medical/14.cancer_info/p008/c01, medical/14.cancer_info/p008/c02
- [mmr] Qgastric-screening-age-interval 위내시경 암 검진은 몇 살부터 몇 년마다 받으라고 하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/08 알기 쉬운 대장암/p013/c00, medical/14.cancer_info/p009/c03, medical/20080813_E_2/p014/c01
- [bm25] Qgastric-screening-age-interval 위내시경 암 검진은 몇 살부터 몇 년마다 받으라고 하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/4e304ca4ed0e0b678457e0cf26e372f42395/p002/c00, medical/4e304ca4ed0e0b678457e0cf26e372f42395/p003/c02, medical/08 알기 쉬운 대장암/p012/c01
- [table_mmr_hybrid] Qgastric-screening-age-interval 위내시경 암 검진은 몇 살부터 몇 년마다 받으라고 하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/20080813_E_2/p014/c01, medical/08 알기 쉬운 대장암/p013/c00, medical/enm-26-126/p004/c02
- [similarity] Qgastric-diagnosis-basis 위 내시경에서 이상이 보이면 위암 여부는 어떻게 확진하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/14.cancer_info/p004/c00, medical/14.cancer_info/p005/c00, medical/14.cancer_info/p005/c01
- [bm25] Qgastric-diagnosis-basis 위 내시경에서 이상이 보이면 위암 여부는 어떻게 확진하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/14.cancer_info/p004/c00, medical/14.cancer_info/p005/c00, medical/14.cancer_info/p005/c01
- [hybrid] Qgastric-diagnosis-basis 위 내시경에서 이상이 보이면 위암 여부는 어떻게 확진하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/14.cancer_info/p004/c00, medical/14.cancer_info/p005/c00, medical/14.cancer_info/p005/c01
- [table_mmr_hybrid] Qgastric-diagnosis-basis 위 내시경에서 이상이 보이면 위암 여부는 어떻게 확진하나요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.1  
  검색: medical/20080813_E_2/p014/c01, medical/14.cancer_info/p004/c00, medical/enm-26-126/p004/c02
- [bm25] Qgastric-high-risk 위암 위험이 특히 높은 사람은 어떤 경우인가요?  
  정답: 4e304ca4ed0e0b678457e0cf26e372f42395 p.3  
  검색: medical/journal-31-3-308/p006/c03, medical/4e304ca4ed0e0b678457e0cf26e372f42395/p006/c05, medical/2017년-안과감염병-관리지침/p011/c01
