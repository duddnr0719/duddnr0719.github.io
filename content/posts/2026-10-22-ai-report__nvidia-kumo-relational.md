---
weight: 162
title: "NVIDIA Kumo Relational — 학습 없이 관계형 DB에서 직접 추론한다"
date: 2026-10-22T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 여러 테이블로 쪼개진 RDBMS 데이터를 한 줄로 합치거나 모델을 새로 학습시키지 않고도, 외래키와 타임스탬프를 그대로 읽어 단일 순방향 패스로 이탈이나 수요를 예측하는 관계형 파운데이션 모델이 나왔다 !

# 개요
- 무엇 : NVIDIA와 Kumo AI 팀이 2026.10.21 사전학습 관계형 파운데이션 모델 'Kumo Relational'(논문 KumoRFM-2)을 발표함.
- 한 줄 정의 : Kumo Relational은 여러 테이블 간 관계와 시점 정보를 보존하면서, 추가 학습 없이 인컨텍스트 러닝만으로 관계형 DB의 예측 작업을 수행하는 기초 모델이다.
- 원문 : [NVIDIA Kumo Relational Outperforms Supervised Machine Learning on Relational Data, No Training Required](https://huggingface.co/blog/nvidia/kumo-relational)

# 그래서 도대체 뭔데 ?
- 실무 데이터는 고객, 주문, 상품 등 여러 테이블이 외래키로 얽힌 관계형 DB에 저장됨.
- 기존 머신러닝은 테이블을 조인하고 30일 평균 구매액 같은 피처를 수작업으로 뽑아 평탄화(flattening)해야 했음.
- Kumo Relational은 이 전처리를 건너뛰고 DB 스키마와 과거 이력을 그대로 입력받아 단일 순방향 패스로 결과를 출력함.
- 추론 시점에 최대 10,000개의 과거 이력 예시를 문맥(context)으로 읽어 별도 학습 없이도 대상 엔티티의 결과를 바로 맞힘.
	- 💡 관계형 파운데이션 모델(Relational Foundation Model) : 단일 테이블이 아니라 외래키로 연결된 다중 테이블 구조 자체를 직접 처리하도록 설계된 사전학습 신경망.
	- 💡 PQL(Predictive Query Language) : 파이프라인을 직접 짜는 대신 "어떤 엔티티의 향후 행동을 예측하라"는 목표만 선언하는 예측 전용 쿼리 언어.

# 어떻게 동작하나 ?
1. 자동 컨텍스트 생성 (Automatic Context Generation)
	- PQL 예측 질의를 받아 과거 DB 시점을 재현함.
	- 특정 기준 시점(anchor timestamp) 이전의 엔티티 중심 서브그래프를 샘플링하고, 타깃 레이블은 기준 시점 이후 발생한 이벤트에서 계산함.
	→ 미래 정보가 입력으로 흐르는 시간적 데이터 누수(data leakage)가 원천 차단됨.

2. 테이블 내 추론 (Reasoning Within Tables)
	- 경량 네트워크가 각 테이블을 개별적으로 처리함.
	- 컬럼 어텐션(column attention)과 로우 어텐션(row attention)을 교차 적용하여 무관한 노이즈 컬럼을 초기에 걸러냄.
	→ 상위 계층으로 노이즈가 전파되지 않고 정제된 행 임베딩(row embedding)이 만들어짐.

3. 테이블 간 추론 (Reasoning Across Tables)
	- 기본키와 외래키(PK/FK) 연결 구조를 따라 그래프 어텐션(graph attention)을 적용함.
	- 컨텍스트 예시 간 크로스 샘플 어텐션(cross-sample attention)을 번갈아 수행하며, 셀이 아닌 행 임베딩 단위로 메시지를 주고받음.
	→ 2차 복잡도(quadratic cost)를 피하면서 500B+ 행 규모의 대형 DB까지 확장할 수 있게 됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 :
	- 테이블마다 수동 집계 피처 엔지니어링 수행 (수주일 소요).
	- 하나의 거대한 단일 테이블로 합친 뒤 XGBoost 같은 그래디언트 부스팅 트리(GBT)를 각 태스크마다 따로 학습함.
	- 시간 경과에 따른 관계망의 미세한 구조적 신호가 평균값 속에 묻혀 유실됨.
- 이번 방식 :
	- DB 원본 테이블과 외래키 관계를 유지한 채 PQL 쿼리 하나로 즉시 질의함.
	- 별도 모델 학습 없이 사전학습 가중치가 최대 10,000개 컨텍스트 예시를 바탕으로 단일 순방향 패스 추론을 끝냄.
	- 최고 성능이 필요할 경우 특정 태스크에 맞춰 파인튜닝도 지원함.
→ 복잡한 데이터 파이프라인 개발 공수를 없애고, 구조적 관계망 전체를 신경망이 직접 참조하기 때문임.

# 숫자로 보면
| 항목 | 이전 (기존 베이스라인) | 이번 (Kumo Relational) | 출처 |
|---|---|---|---|
| RelBench V1 분류 AUROC | 전문가 수작업 피처 GBT 파이프라인 | 평균 약 4 AUROC 포인트 향상 | [Hugging Face 원문](https://huggingface.co/blog/nvidia/kumo-relational) |
| SAP SALT 엔터프라이즈 MRR | 피처 엔지니어링 기반 XGBoost | 기본 상태에서 7 MRR 포인트 향상 (파인튜닝 시 13 MRR 포인트 향상) | [Hugging Face 원문](https://huggingface.co/blog/nvidia/kumo-relational) |
| SAP SALT vs AutoGluon MRR | 대규모 AutoGluon 앙상블 | 기본 8% 우수 (파인튜닝 시 16% 우수) | [Hugging Face 원문](https://huggingface.co/blog/nvidia/kumo-relational), [arXiv:2604.12596](https://arxiv.org/abs/2604.12596) |
| SAP SALT vs 단일 테이블 기초모델 | 최근 테이블 파운데이션 모델들 | 약 25% 향상 | [Hugging Face 원문](https://huggingface.co/blog/nvidia/kumo-relational) |
| RelArena-α 리더보드 (1,000샘플 추론시간 / Elo) | rt-plurel (약 7,300초 / Elo 1,878) | 약 17초 / Elo 1,842 (유사 성능 유지하며 약 430배 빠름) | [Hugging Face 원문](https://huggingface.co/blog/nvidia/kumo-relational) |

# 주의할 점 / 한계
- 엔티티 간 연결 관계와 시간적 동역학이 풍부한 데이터셋(예: 사용자 행동 이력, 거래 내역)에서 장점이 발휘되며, 단순 독립 레코드 테이블에서는 이점이 덜할 수 있음.
- 학습 데이터가 극도로 많은 대형 태스크의 경우, 최대 10,000개 컨텍스트 예시를 활용하는 제로샷/퓨샷 인컨텍스트 추론이 전용 지도학습 모델에 근소하게 뒤처질 수 있음 (원문은 이 경우 파인튜닝을 대안으로 권장함).
- 타깃과 관련된 신호가 그래프 상에서 지나치게 먼 홉(hops)에 있으면 포착하기 어려우므로, 핵심 테이블 위주로 시작해 점진적으로 스키마를 넓혀야 함.
- 모델 가중치는 오픈 라이선스지만 Apache 2.0이 아닌 OpenMDW 1.1 라이선스가 적용되어 있으므로 배포 전 라이선스 조항 확인이 필요함.
- 전체 모델 파라미터 수 및 구체적인 학습 하드웨어 구성 : 원문에 없음.

# 정리
- 테이블을 합치고 피처를 깎던 수작업 파이프라인을 건너뛰고, RDBMS 스키마 그대로 단일 순방향 패스로 추론하는 관계형 기초 모델이 본격적으로 실용권에 들어섬.
- 매번 새 모델을 학습시키기 번거로운 엔터프라이즈 환경이나, 실시간으로 DB 예측 질의를 던져야 하는 자율 에이전트 시스템에 유용함.

# 참고
- [NVIDIA Kumo Relational Outperforms Supervised Machine Learning on Relational Data, No Training Required](https://huggingface.co/blog/nvidia/kumo-relational) — Hugging Face 공식 블로그
- [KumoRFM-2: Scaling Foundation Models for Relational Learning](https://arxiv.org/abs/2604.12596) — arXiv 연구 논문
- [NVIDIA/structured-data-models](https://github.com/NVIDIA/structured-data-models) — GitHub 공식 레포지토리
- [nvidia/Kumo-Relational](https://huggingface.co/nvidia/Kumo-Relational) — Hugging Face 공식 모델 카드
