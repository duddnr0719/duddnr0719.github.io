---
weight: 134
title: "SGLang 의사결정 모델 서빙 — Score API와 연산 공유(MIS)로 빠른 스케일링"
date: 2026-09-26T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

SGLang 의사결정 모델 스케일링 — Score API와 MIS로 서빙 최적화

> 긴 텍스트 생성 대신 점수만 반환하는 의사결정 모델에서 연산 공유를 통해 서빙 속도를 단축하는 방법을 소개함.

# 개요
- 무엇 : LMSYS Org가 2026.09.25 SGLang 기반 의사결정 모델 스케일링 방안을 발표함.
- 한 줄 정의 : JEV-like 의사결정 모델은 긴 텍스트 대신 카테고리나 점수를 반환하는 모델이다.
- 원문 : [Scaling JEV-like Decision Models with SGLang](https://lmsys.org/blog/2026-09-25-sglang-decision-models)

# 그래서 도대체 뭔데 ?
- 모델이 행동을 결정할 때 불필요한 설명을 생성하는 대신 선택지의 점수만 추출함.
- 동일한 질문(컨텍스트)을 여러 선택지가 공유할 때 연산을 최적화함.
	- 💡 MIS (Multi-item scoring) : 동일한 요청 내에서 공통 Query(컨텍스트) 연산을 공유하고 각 후보가 독립적으로 처리되게 하는 방식.

# 어떻게 동작하나 ?
1. 의사결정 방식 선택
	- Pointwise 방식 : 하나의 후보만 보여주고 Yes/No를 판단함.
	- Setwise 방식 : 모든 후보를 한 번에 보여주고 평가함.
2. Score API 호출 (`/v1/score`)
	- 텍스트를 생성하는 대신 특정 토큰(Yes/No 등)의 점수만 명시적으로 요청함.
3. MIS 실행
	- Pointwise 평가 시 각 후보가 공유하는 질문의 연산을 재사용함.
	→ 후보가 많아질수록 연산 비용이 절감됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : Generate API를 사용해 답변 텍스트 생성을 기다리거나 각 후보를 독립적인 시퀀스로 처리함 (SIS).
- 이번 방식 : 명시적인 Score API와 MIS를 활용해 공통 컨텍스트 연산을 공유함.
→ 토큰 샘플링을 생략하고 반복되는 컨텍스트 연산을 줄여 속도가 빨라짐.

# 숫자로 보면
| 항목 | 이전 (Generate) | 이번 (MIS) | 출처 |
|---|---|---|---|
| Qwen3-0.6B (16개 선택지 p95 latency) | 39.6ms | 18.7ms | [LMSYS](https://lmsys.org/blog/2026-09-25-sglang-decision-models) |
| Qwen3-8B (16개 선택지 p95 latency) | 54.1ms | 20.6ms | [LMSYS](https://lmsys.org/blog/2026-09-25-sglang-decision-models) |
| Qwen3.5-4B (16개 선택지 p95 latency) | 84.8ms | 55.7ms | [LMSYS](https://lmsys.org/blog/2026-09-25-sglang-decision-models) |

# 주의할 점 / 한계
- MIS는 높은 부하 상태나 후보 개수가 많을 때 유리하며, 옵션이 2개일 때는 Qwen3-0.6B 기준 SIS가 더 빠름.
- 위 결과는 1x NVIDIA H200 GPU, SGLang on CUDA 13.0, Open-Jev 데이터셋 환경에서 측정한 값임.
- 벤치마크는 서빙 성능만 측정한 것이며 결정 품질(정확도)을 보장하지는 않음.

# 정리
- 긴 생성 대신 점수만 필요한 의사결정 모델의 서빙을 Score API와 연산 공유(MIS)로 최적화함 (Qwen3-8B 기준 54.1ms → 20.6ms).
- 후보 개수가 많고 높은 부하가 예상되는 상황에서 유리함.

# 참고
- [Scaling JEV-like Decision Models with SGLang](https://lmsys.org/blog/2026-09-25-sglang-decision-models) — LMSYS Org
