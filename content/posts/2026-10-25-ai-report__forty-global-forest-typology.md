---
weight: 167
title: "ForTy — 10m 해상도로 전 지구 숲 유형과 열화 이력을 분류한다"
date: 2026-10-25T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 단순한 나무 유무를 넘어 원시림부터 플랜테이션까지 6개 숲 유형을 10m 단위로 구분하고, 2017년부터 2025년까지의 열화 경로를 추적하는 전 지구 산림 지도 파이프라인이다 !

# 개요
- 무엇 : Google DeepMind, Google Research, WRI, IIASA가 2026.10.22 ForTy (Forest Typology) 2020 맵과 2017 ~ 2025 시계열 데이터셋을 공개함.
- 한 줄 정의 : ForTy는 전 지구 육상의 10m x 10m 격자를 6개 산림 및 토지 이용 유형으로 분류하는 딥러닝 파이프라인이자 오픈 데이터셋이다.
- 원문 : [Beyond tree cover: mapping the world’s forest types](https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/)

# 그래서 도대체 뭔데 ?
- 위성에서 내려다보면 원시림이나 유칼립투스 플랜테이션이나 기름야자 농장이나 똑같은 초록색 패치로 보임.
- 기존 위성 지도는 나무의 유무만 따지는 수관 피복(Tree Cover) 이진 분류에 머물러 있었음.
- 유럽연합의 산림벌채방지법(EUDR)은 2020.12.31을 기준일로 삼아, 원시림이 목재 농장으로 변하는 산림 열화와 숲이 농경지로 바뀌는 산림 벌채를 가려낼 것을 요구함.
- ForTy는 FAO 정의와 EUDR 규정에 맞춰 전 지구 육상을 6개 클래스로 쪼개어 분류함:
  - 클래스 1 (원시림) : 인간 간섭 흔적이 없는 자연림.
  - 클래스 2 (자연 재생림) : 인간의 개입 이후 스스로 회복 중인 2차림.
  - 클래스 3 (식재림) : 사람이 파종하거나 심어 40년 초과 주기로 관리하는 산림.
  - 클래스 4 (플랜테이션 산림) : 1~2개 수종을 40년 이하 주기로 집약 재배하는 단기 목재림.
  - 클래스 5 (농업용 수목 작물 및 혼농임업) : 팜유 · 고무 · 카카오 등 목재 외 작물 생산지로 EUDR상 산림에서 제외.
  - 클래스 6 (기타 토지) : 초지 · 일반 농경지 · 도시 · 수역 및 수관 피복률 10% 미만 토지.
- 💡 수관 피복(Tree Cover) : 나뭇가지와 잎이 지표면을 덮는 비율을 뜻하며, 숲의 생태적 보전 가치나 토지 이용 목적은 반영하지 못함.
- 💡 EUDR(EU Deforestation Regulation) : 2020.12.31 이후 벌채되거나 열화된 산림에서 생산된 목재 · 팜유 · 카카오 등의 EU 역내 유통을 금지하는 규제.
- 💡 윤벌기(Rotation Period) : 나무를 심어서 최종 벌채해 수확하기까지 걸리는 기간.

# 어떻게 동작하나 ?
1. AlphaEarth Foundations(AEF) 시계열 임베딩 입력
   - Sentinel-1 · Sentinel-2 · Landsat · ALOS PALSAR-2 등 다중 위성의 연간 관측치를 10m 해상도의 per-pixel 임베딩 벡터로 압축해 활용함.
   - Stage 1에는 지형 특성을 반영하기 위해 Copernicus DEM 30m 수치표고모델(고도 · 경사 · 경사향)을 10m로 업샘플링해 함께 투입함.
   → 단일 시점 위성 사진의 한계를 벗어나 계절별 식생 주기와 다년치 패턴을 파악하게 됨.

2. Swin Transformer v2 기반 5개 앙상블 백본
   - 계층적 비전 트랜스포머인 SwinV2-Ti/4(Tiny 변형, 패치 크기 4) 아키텍처와 시맨틱 분할 헤드를 적용함.
   - 128 x 128 픽셀(1,280m x 1,280m 패치) 단위로 연산하며, 독립 초기화된 5개 모델의 소프트맥스 출력을 평균 내어 불확실성을 낮춤.
   → 숲의 미세한 질감과 주변 경관 맥락을 함께 학습함.

3. 3단계 캐스케이드 학습(Cascaded Training)
   - Stage 1 (기반 분류기) : 450,275개의 전문가 레이블 표본으로 학습. 모호하거나 상위 범주만 있는 데이터는 엔트로피 정규화 가중치 0.1의 부분 레이블 손실(Partial label loss)로 처리함.
   - Stage 2 (대규모 의사 레이블 학습) : Stage 1 예측 확률에 자연림 지도(NFW 2020) · 토지피복도(WorldCover) · 브라질 MapBiomas 시계열 이력을 융합해 120만 개(1.2M) 패치의 의사 레이블을 생성함. 2019 · 2020 · 2021년 중 무작위 1개년을 선택하는 시간 증강을 거쳐 10 에포크 학습함.
   - Stage 3 (시계열 보정 학습) : 2019 ~ 2024년 6개년치 시계열 텐서(시간 패치 크기 6)를 120만 개 패치에 한 번에 주입해 10 에포크 학습함.
   → 연도별 관측 노이즈를 걸러내고 실제 벌채나 식생 천이 같은 지표면 변화만 유지하게 됨.

4. 3차례 능동 학습(Active Learning)과 타일 중첩 추론
   - 전문가 피드백 루프를 통해 3개 라운드에 걸쳐 약 43000개 표본을 추가로 투입함 (1차 22131개 · 2차 1016개 · 3차 19880개).
   - 전 지구 인퍼런스 시 패치 중심 간격을 210m로 촘촘히 겹쳐 추론한 뒤, 중심점과의 역거리 가중 평균을 적용함.
   → 타일 경계선이 튀는 격자 아티팩트를 없애고 매끄러운 전 지구 지도를 완성함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 :
  - 기존 전 지구 수관 피복도는 숲이 있는지 없는지만 30m나 10m 단위로 따지는 이진 분류에 그침.
  - 전 지구 산림 관리 지도(GFM 2015)는 100m로 해상도가 거칠었고, 식재림 데이터베이스(SDPT)는 지역적 누락이 심했음.
  - 구글의 선행 연구인 NFW 2020도 자연림 여부만 이진 분류하는 수준이었음.
- 이번 방식 :
  - 10m 해상도로 전 지구 육상을 6개 세부 산림 및 토지 이용 유형으로 동시에 정밀 분류함.
  - 2017년부터 2025년까지의 시계열을 함께 제공해, 원시림이 베어진 뒤 목재 농장이 되었는지 농경지가 되었는지 구체적 열화 과정을 추적할 수 있음.
  - 단순 확정 라벨이 아니라 0 ~ 250 정량화 신뢰도 점수를 담은 래스터 맵을 제공해, 사용자 목적에 맞춰 임계값을 조절할 수 있음.
→ 단일 시점 위성 사진 대신 다년치 다중 위성 데이터를 압축한 AlphaEarth 임베딩을 쓰고, 3단계 캐스케이드 학습과 능동 학습으로 복잡한 토지 이용 이력을 모델에 주입했기 때문.

# 숫자로 보면
| 항목 | 이전 | 이번 (ForTy) | 출처 |
|---|---|---|---|
| 공간 해상도 | 30m ~ 100m (GFC · GFM) | 10m x 10m | Nature Scientific Data 논문 |
| 분류 범주 | 2개 (숲/비산림) 또는 3개 | 6개 클래스 | Nature Scientific Data 논문 |
| 6개 클래스 층화 전체 정확도 | 해당 없음 | 90.2% (SE = 0.3%) | Nature Scientific Data 논문 |
| 자연림 이진 분류 정확도 | 92.2% (NFW 2020) | 94.8% (SE = 0.3%) | Nature Scientific Data / 구글 리서치 블로그 |
| 산림 대 비산림 판별 정확도 | 원문에 없음 (기존 지도 대비 우수) | 95% | DeepMind 공식 블로그 |
| 검증 표본 규모 | 단편적 지역 데이터 | 9,100개 무작위 층화 표본 (합의 완료 8,190개) | Nature Scientific Data 논문 |
| 학습 데이터 규모 | 450,275개 (기반 Stage 1) | 1,200,000개 (대규모 Stage 2 · 3) | Nature Scientific Data 논문 |
| 능동 학습 추가 표본 | 없음 | 약 43,000개 (3개 라운드) | Nature Scientific Data 논문 |
| 시계열 추적 범위 | 단일 연도 베이스라인 | 2017년 ~ 2025년 (9개년) | DeepMind 공식 블로그 |
| 식재림/플랜테이션 윤벌기 기준 | 정성적 관리 정의 | 40년 임계값 | Nature Scientific Data 논문 |

# 주의할 점 / 한계
- 40년 윤벌기 프록시의 한계 : FAO와 EUDR 규정은 수종 구성 · 식재 간격 · 균일 수령 같은 관리 집약도로 식재림과 플랜테이션을 가르지만, 위성 영상에서 이를 직접 재기 어려워 40년 윤벌기를 대리 지표로 삼음. 지역별 고유한 임업 관행이나 40년 안팎의 경계에서는 오분류가 생길 수 있음.
- 기타 목본지(OWL) 미분리 : 수관 피복률 5% ~ 10% 사이의 성긴 목본지는 6번째 클래스인 기타 토지(Other Land)로 합쳐짐. 따라서 원시림이 기타 목본지로 서서히 열화되는 현상은 ForTy 단독으로 잡지 못하며, 별도의 수관 피복 변화 지도와 함께 봐야 함.
- 사후 보정 없는 상대 신뢰도 : 5개 모델 앙상블의 소프트맥스 평균값을 담았으며, 사후 보정(post-hoc calibration)을 거친 엄밀한 통계적 사후 확률이 아님. 절대적 확률이라기보다는 상대적 확신도로 취급해야 함.
- 관리림 검증에서의 전문가 판단 불확실성 : 9,100개 검증점 중 미합의(738개)와 불확실(172개) 표본 대다수가 플랜테이션(163개 미합의 / 40개 불확실) · 식재림(146개 미합의 / 38개 불확실) · 수목 작물(44개 불확실)에 쏠려 있음. 토지 이용 의도를 육안으로 가리기 힘든 관리형 산림 특성상 보고된 정확도에 미세한 편향이 존재할 가능성이 있음.

# 정리
- 인공위성 사진의 단순 초록색 피복을 넘어 6가지 산림 및 토지 이용 목적을 10m 해상도로 가려내고, 2017년부터 2025년까지의 연도별 변화 경로를 밝혀낸 점이 새로움.
- EUDR 규제 대응이 필요한 무역 · 수출 기업, 공급망 감사기관, 전 지구 생물다양성 보전 연구자가 기준점으로 삼을 만함.
- 구글 어스 엔진(GEE)과 Figshare에 완전 공개(CC-BY 4.0)되어 연구와 실무에 바로 활용할 수 있음.

# 참고
- [Beyond tree cover: mapping the world’s forest types](https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/) — Google DeepMind Blog
- [Global forest typology at 10-meter resolution for forest and land-use monitoring](https://www.nature.com/articles/s41597-026-08299-5) — Nature Scientific Data
- [Separating natural forests from other tree cover with AI for deforestation-free supply chains](https://research.google/blog/separating-natural-forests-from-other-tree-cover-with-ai-for-deforestation-free-supply-chains/) — Google Research Blog
- [Mapping, modeling, and understanding nature with AI](https://deepmind.google/blog/mapping-modeling-and-understanding-nature-with-ai/) — Google DeepMind Blog
