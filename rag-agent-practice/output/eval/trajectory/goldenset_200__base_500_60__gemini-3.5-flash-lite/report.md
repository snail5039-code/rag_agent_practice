# 검색 과정 채점 - goldenset_200__base_500_60__gemini-3.5-flash-lite

- 답할 수 있는 문제 196개, agentevals superset 매칭

| 검사 | 대상 문제 | 지켜짐 | 지켜진 비율 | 지켜졌을 때 정답률 | 안 지켜졌을 때 정답률 |
|---|---|---|---|---|---|
| 표 질문에 is_table=true 사용 | 33 | 25 | 0.758 | 0.480 | 0.875 |
| 재검색 때 검색어를 바꿈 | 84 | 83 | 0.988 | 0.639 | 1.000 |
| 지정한 분야가 맞음 | 126 | 114 | 0.905 | 0.842 | 0.333 |

## 안 지켜진 사례

### 표 질문에 is_table=true 사용 (8)

- **my-02** [O, law] 궐련지(Cigarette paper)는 무엇으로 만드나요?  
  검색: `궐련지 무엇으로 만드나요` (is_table=False, domain=None)
- **my-03** [O, finance] DC 퇴직연금에서 투자위험은 누가 부담하나요?  
  검색: `DC 퇴직연금 투자위험 부담 가입자` (is_table=False, domain=finance) / `확정기여형 DC 투자위험 부담 가입자` (is_table=False, domain=finance)
- **my-04** [O, finance] 노후연금체계 중 성격이 "공적/강제"인 연금은?  
  검색: `노후연금체계 성격 공적 강제 연금` (is_table=False, domain=None)
- **gs-025** [O, finance] TCFD의 '전략' 핵심요소는 어떤 기후변화 시나리오를 고려하면서 잠재적 재무 리스크를 파악하며, 그 리스크는 어떤 종류로 나눌 수 있나요?  
  검색: `TCFD 전략 기후변화 시나리오 잠재적 재무 리스크 종류` (is_table=False, domain=None)
- **gs-122** [O, medical] 급성 출혈성 결막염은 어떠한 병원체로 인해 감염되며, 그 감염된 병원체의 잠복기는 얼마나 되나요?  
  검색: `급성 출혈성 결막염 병원체 잠복기` (is_table=False, domain=medical)
- **gs-200** [O, law] 재기중소기업인 특례 대상 확대와 적용기한 연장이 어떤 세법에 기반하여 이루어진 것인가요?  
  검색: `재기중소기업인 특례 대상 확대 적용기한 연장 세법` (is_table=False, domain=None) / `재기중소기업인 특례 대상 확대 및 적용기한 연장 조특법` (is_table=False, domain=None)
- **gs-217** [O, law] 2002.1.26 일부개정에서  의결권을 행사할 수 있는 경우는 무엇인가요?  
  검색: `2002.1.26 일부개정 의결권 행사` (is_table=False, domain=None)
- **gs-256** [X, commerce] 구매하고자 하는 품질에 대한 선호도 순위를 최고부터 최저까지 나열해 주세요  
  검색: `품질 선호도 순위 최고 최저` (is_table=False, domain=None)

### 재검색 때 검색어를 바꿈 (1)

- **gs-202** [O, law] 2024년부터 현금영수증을 의무발행해야하는 상황에 대해 구체적으로 설명해주세요.  
  검색: `2024년 현금영수증 의무발행 업종 대상` (is_table=False, domain=commerce) / `2024년 현금영수증 의무발행 업종` (is_table=False, domain=public) / `2024년 현금영수증 의무발행 업종` (is_table=False, domain=law)

### 지정한 분야가 맞음 (12)

- **pub-34** [O, public] 청년농 우대보증 한도를 5억으로 정하고 후계농 정책자금으로 3억을 사용한 후, 다른 정책자금으로 남은 2억을 사용하려면 우대보증이 적용되는지,   
  검색: `청년농 우대보증 한도 5억 후계농 정책자금 3억 다른 정책자금 2억` (is_table=False, domain=finance) / `청년농 우대보증 후계농 정책자금 5억 3억` (is_table=False, domain=)
- **pub-35** [X, public] 금융기관에서 담보 설정시 대출가능 금액이 토지와 시설물에서 각각 시세의 80%, 60% 수준인 이유와 이에 대한 기준을 어떻게 정하는지 설명해주  
  검색: `담보 설정 대출가능 금액 토지 시설물 시세 80% 60%` (is_table=False, domain=finance) / `담보 시세 80% 시설물 60%` (is_table=False, domain=finance)
- **gs-004** [X, finance] 은행법에 의거 예비인가를 신청할 수 있는지와, 그 경우 금융위원회가 검토했어야 하는 요건은 무엇인가요?  
  검색: `은행법 예비인가 신청 금융위원회 요건` (is_table=False, domain=law) / `은행법 예비인가 금융위원회` (is_table=False, domain=law)
- **gs-059** [X, finance] 100인 이하 근로자를 고용하는 사업체의 전체 근로자와 대비하여 가입 대상 근로자 수의 비율은 어떻게 되나요?  
  검색: `100인 이하 근로자 전체 근로자 가입 대상 근로자 수 비율` (is_table=True, domain=public) / `100인 이하 근로자 가입 대상 근로자 수 비율` (is_table=True, domain=) / `100인이하 근로자비중 가입 대상근로자수` (is_table=True, domain=finance)
- **gs-062** [X, public] 2023년과 2024년 사이에서 선진국의 성장률 변화와 신흥국 물가 상승률의 변화를 비교해보면 어떠한 경향을 발견할 수 있나요?  
  검색: `2023년 2024년 선진국 성장률 신흥국 물가 상승률` (is_table=True, domain=finance) / `선진국 성장률 신흥국 물가 상승률 2023년 2024년` (is_table=True, domain=finance)
- **gs-080** [X, public] 재해자금 지원 대상 농업인이라면 위기·재기보증 단계에서 받을 수 있는 최대 대출액과 보증비율은 얼마인가요?  
  검색: `재해자금 위기 재기보증 최대 대출액 보증비율` (is_table=True, domain=finance) / `위기 재기보증 대출액 보증비율 농업인 재해자금` (is_table=True, domain=finance) / `위기 재기보증 대출액 보증비율` (is_table=False, domain=finance)
- **gs-196** [X, law] 2023년부터 소득세법에 따른 출산 및 육아에 대한 세제지원이 강화되었는데, 6세 이하 자녀가 받는 보육수당의 비과세 한도는 어떻게 변경되었나요  
  검색: `출산 육아 세제지원 6세 이하 자녀 보육수당 비과세 한도 2023` (is_table=False, domain=public) / `6세 이하 자녀 보육수당 비과세 한도 2023 소득세법` (is_table=False, domain=finance) / `출산 보육수당 비과세 확대 6세 이하` (is_table=False, domain=public)
- **gs-197** [O, law] 6세 이하의 자녀에 대한 의료비 공제를 받을 수 있는 경우, 적용되는 공제율은 몇 퍼센트인가요? 또한, 이 공제를 받는 데에는 연간 지출액 제한  
  검색: `6세 이하 의료비 공제율 연간 지출액 제한` (is_table=False, domain=finance) / `6세 이하 자녀 의료비 공제율 연간 지출액 제한` (is_table=False, domain=public) / `6세 이하 의료비 공제` (is_table=False, domain=law)
- **gs-198** [O, law] 2023년 소득세법 개정 중 고소득 근로소득세액공제를 1억2천만원까지 적용한 후, 그 초과 금액에 대한 근로소득세액공제의 변경사항은 무엇인가요?  
  검색: `소득세법 근로소득세액공제 1억2천만원 고소득` (is_table=False, domain=finance) / `소득세법 개정 근로소득세액공제 1억2천만원` (is_table=False, domain=law)
- **gs-202** [O, law] 2024년부터 현금영수증을 의무발행해야하는 상황에 대해 구체적으로 설명해주세요.  
  검색: `2024년 현금영수증 의무발행 업종 대상` (is_table=False, domain=commerce) / `2024년 현금영수증 의무발행 업종` (is_table=False, domain=public) / `2024년 현금영수증 의무발행 업종` (is_table=False, domain=law)
- **gs-207** [X, law] 이지그릴 매직쿡과 원터치, 라이프 제품 중 어느 제품이 유일하게 검은색 베이스를 가지고 있는지 알려주세요.  
  검색: `이지그릴 매직쿡 원터치 라이프 베이스 색상 검은색` (is_table=False, domain=commerce) / `이지그릴 매직쿡 원터치 라이프 베이스 검은색` (is_table=False, domain=commerce)
- **gs-266** [X, commerce] 한국콘텐츠진흥원 북경비즈니스센터의 시설 중 상설전시공간에서는 어떤 종류의 한국 콘텐츠 상품들을 전시하고 있나요?  
  검색: `한국콘텐츠진흥원 북경비즈니스센터 상설전시공간 콘텐츠 상품 전시` (is_table=False, domain=public) / `북경비즈니스센터 상설전시공간 콘텐츠 상품` (is_table=False, domain=public) / `"북경비즈니스센터"` (is_table=False, domain=public)

