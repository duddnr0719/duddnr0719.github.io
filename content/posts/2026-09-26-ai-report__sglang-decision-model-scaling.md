---
weight: 134
title: "SGLang 의사결정 모델 서빙 — Score API와 연산 공유(MIS)로 빠른 스케일링"
date: 2026-09-26T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

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

# 직접 써보기 — 연구실 L40에 띄운 OpenJev
- OpenJev : Jev를 오픈 모델로 흉내 낸 구현 (화면 부제부터 "open approximation of Jev"). 연구실 L40에 띄워둔 qwen3.8-27b를 뒤에 붙여서 돌림.
- 질문을 3가지 타입으로 정의함.
	- choice : 보기 중 하나 고르기 (department : billing / technical / account / other)
	- score : 단계 점수 (urgency : 0 Low ~ 3 Critical)
	- noul : 참 / 거짓 확률 (angry : 고객이 화났나 ?)
- 입력은 기본 예제 그대로 : "두 달 연속 Pro 요금이 두 번 결제됐다, 빨리 고쳐라" 라는 고객 문의.

## parallel 모드 — 보기마다 따로 점수
![OpenJev parallel 모드 실행 결과 (department · urgency)](/images/openjev-parallel-1.png)
- 9번 호출, 3,966ms.
- department : billing 73% (confidence 91.4%)
- urgency : 2.38 / 3 → High 61% · Critical 38%
- angry : 95%

![OpenJev parallel 모드 실행 결과 (angry · 호출 정보)](/images/openjev-parallel-2.png)
- 입력 1,339 토큰 / 출력 85 토큰 → 보기마다 따로 물어보니 입력은 늘지만, 글을 안 쓰니까 출력은 거의 없음.

## oneshot 모드 — JSON 한 번에
![OpenJev oneshot 모드 실행 결과](/images/openjev-oneshot.png)
- 1번 호출, 3,195ms.
- billing 98%, urgency 2.00 (High 100%), angry 90%.
- 입력 320 토큰 / 출력 714 토큰 → 대신 답을 JSON으로 '써야' 해서 출력이 약 8배.
→ 분포가 한쪽으로 확 쏠림. parallel은 'High냐 Critical이냐' 애매한 정도가 숫자로 남는데, oneshot은 하나로 찍어버림. 판단 근거를 확률로 쓰고 싶으면 parallel 쪽이 더 쓸모 있음.

## API로 질문 하나만 보내면
- noul 질문 1개를 API(`POST /api/evaluate`)로 3번 보냈더니 86 ~ 121ms.
- 연구실에서는 이걸 에이전트 허브의 라우팅 판단에 쓰는 중 → '이 작업을 어느 에이전트한테 넘길까 ?'를 확률 하나로 받음 (문서 읽기 · 요약 → agy, 코드 구현 → claude).
- 써보면서 걸린 것 : 질문을 평문 문자열로 보내면 (`"is_simple": "판단해줘"`) 판별 없이 고정값(0.0 / 0.5)만 돌아옴 → 반드시 `type` + `instructions` 구조로 보내야 함.

→ 원문의 핵심 '생성하지 않고 점수만 받으면 빨라진다'를 작게나마 체감함. 다만 qwen 27B 하나, L40 한 장, 몇 번 돌려본 수준이라 원문 벤치마크(H200, SGLang)와 직접 비교할 수는 없음.

# 정리
- 긴 생성 대신 점수만 필요한 의사결정 모델의 서빙을 Score API와 연산 공유(MIS)로 최적화함 (Qwen3-8B 기준 54.1ms → 20.6ms).
- 후보 개수가 많고 높은 부하가 예상되는 상황에서 유리함.

# 참고
- [Scaling JEV-like Decision Models with SGLang](https://lmsys.org/blog/2026-09-25-sglang-decision-models) — LMSYS Org
