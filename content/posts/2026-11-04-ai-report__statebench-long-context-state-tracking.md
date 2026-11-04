---
weight: 178
title: "StateBench — 긴 문서 상태 추적에서 트랜스포머와 Gated DeltaNet의 한계를 가른다"
date: 2026-11-04T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 긴 문서 속 변수 변화를 4단계 대수학 난이도로 쪼개어 트랜스포머와 순환형 아키텍처의 한계를 실증한 벤치마크다. 프론티어 모델조차 참조 할당 추적에서 13% 이하로 무너지는 취약점을 짚어낸다 !

# 개요
- 무엇 : 앨런 인공지능 연구소(Allen Institute for AI)가 2026.11.03 공개
- 한 줄 정의 : StateBench는 크론-로드 대수학 이론을 바탕으로 언어 모델의 긴 문서 상태 추적 능력을 4단계 난이도로 검증하는 벤치마크다.
- 원문 : [StateBench: Testing how language models track state changes over long documents](https://huggingface.co/blog/allenai/statebench)

# 그래서 도대체 뭔데 ?
- 변수 값 갱신이나 인물 간 소유권 이전 같은 상태 추적은 코드 분석과 에이전트 구동의 밑바탕임.
- 기존 평가는 가장 난도 높은 순열 문제 하나에만 치중해 아키텍처별 실제 지원 범위를 명확히 가르지 못했음.
- 수학적 모노이드 분해 이론을 차용해 난이도를 4단계로 쪼개고 모델의 한계 도달 지점을 측정함.
- 프론티어 모델도 단순 갱신은 처리하지만 변수 간 상호 참조가 얽힌 긴 시퀀스에서는 추적 능력을 상실함.
	- 💡 크론-로드 이론 (Krohn-Rhodes Theory) : 유한 상태 시스템의 변환 과정을 기본 대수 단위로 분해하는 수학 이론.
	- 💡 Gated DeltaNet : 이전 상태 메모리를 앞으로 누적 전달하여 긴 의존성을 다루는 순환형(recurrent) 아키텍처.

# 어떻게 동작하나 ?
1. 4단계 대수학 난이도 설계
	- r-trivial : 불변 할당 단계로 최초 선언된 값을 유지함 (`let x = 4`).
	- aperiodic : 값에 의한 단순 재할당 단계로 이전 이력을 잊고 최신 값만 확인하면 됨 (`x = 4` 뒤에 `x = 2`).
	- soluble : 자기 참조 갱신 단계로 누적 연산을 기억해야 함 (`x = x + 5`).
	- general finite : 참조에 의한 할당 단계로 다른 변수의 현재 값을 읽어오거나 맞바꿈 (`x = y`, 컵 5개 순열).
	→ 난이도에 따라 모델이 메모리에 유지해야 하는 연산 복잡도가 달라짐.

2. 원본 시퀀스 기반 파생 생성
	- 가장 복잡한 순열 시퀀스(general finite) 하나를 원본으로 생성함.
	- 변수 개수와 값 범위, 할당 위치를 동일하게 고정한 채 할당 연산 규칙만 3가지 하위 단계로 변환함.
	→ 어휘나 길이 차이 없이 순수하게 상태 추적 알고리즘 복잡도만 비교하게 됨.

3. 표면 형식 다각화 검증
	- 동일한 상태 전이 논리를 정수 코드(integer-code), 스프레드시트 셀 편집, 상태 표시등 등 여러 표면 형태로 렌더링함.
	→ 특정 프롬프트 형식에 따른 과적합을 배제하고 순수 추론 능력을 평가함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 가장 풀기 어려운 S_5 대칭군 순열 문제 같은 극단적 테스트에만 치중했음.
- 이번 방식 : 불변 할당부터 자기 참조, 참조 교환까지 4단계 계층으로 세분화함.
→ 트랜스포머와 순환형 모델이 각각 어느 수준의 복잡도까지 소화할 수 있는지 경계선이 명확해짐.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 직접 학습 275M 시퀀스 길이 (할당 수) | 256개 할당 (훈련 길이) | 최대 64,000개 할당 (250배 일반화 테스트) | [HF 블로그](https://huggingface.co/blog/allenai/statebench) |
| 직접 학습 275M general finite 일반화 | 트랜스포머 (0% 수준, 학습 불가) | Gated DeltaNet (10배 길이까지 유지) | [HF 블로그](https://huggingface.co/blog/allenai/statebench) |
| 사전학습 오픈 모델 (7B) 컨텍스트 한계 | 최대 64,000 토큰 훈련 | 64,000 토큰 초과 평가 (general finite chance 수준) | [HF 블로그](https://huggingface.co/blog/allenai/statebench) |
| 프론티어 모델 4개 모델 general finite | r-trivial 및 aperiodic 우수 | 최장 시퀀스 13% 이하로 급락 | [HF 블로그](https://huggingface.co/blog/allenai/statebench) |

# 주의할 점 / 한계
- 고정된 변수 가정 : 상태 추적 대상 변수가 2 ~ 16개로 고정되어 있음. 실제 대화나 소프트웨어 환경처럼 시간이 지나며 새로운 객체나 인물이 계속 등장하는 동적 환경은 다루지 못함.
- 표면 형식에 따른 성능 편차 : 275M 하이브리드 모델이 RULER 형식에서는 만점에 근접했으나 스프레드시트 셀 편집 형식에서는 chance 수준으로 추락하는 등 표현 양식에 취약함.
- 이론적 증명의 미완성 : Gated DeltaNet의 비음수 고유값 제약에서 모든 soluble 과제를 풀 수 있는지, 부동소수점 정밀도와 어텐션 레이어 결합이 미치는 영향은 아직 원문에 규명되지 않음.
- 하드웨어 조건 : 모델 훈련 및 평가에 사용된 구체적인 GPU 사양과 실행 시간은 원문에 없음.

# 정리
- 긴 문서 상태 추적의 수학적 한계를 4단계 계층으로 깔끔하게 정리한 벤치마크임.
- 트랜스포머의 이론적 한계와 Gated DeltaNet 등 순환형 아키텍처의 장단점이 뚜렷하게 드러남.
- 긴 호흡의 코드 분석기나 자율 에이전트 백본을 설계하는 개발자라면 꼭 살펴볼 만한 결과임.

# 참고
- [StateBench: Testing how language models track state changes over long documents](https://huggingface.co/blog/allenai/statebench) — Hugging Face Blog
- [A Fine-Grained Hierarchy and Benchmark for State Tracking in Language Models](https://arxiv.org/abs/2611.03094) — arXiv:2611.03094
- [allenai/state-bench](https://github.com/allenai/state-bench) — GitHub Repository
- [allenai/state-bench](https://huggingface.co/datasets/allenai/state-bench) — Hugging Face Datasets
