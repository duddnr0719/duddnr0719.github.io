---
weight: 140
title: "GPT-6.1 Sol — Astra급 엔지니어링 지능을 5분의 1 가격으로 쓰는 에이전트 모델"
date: 2026-10-15T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 플래그십 모델의 소프트웨어 엔지니어링 능력을 5분의 1 토큰 비용으로 제공해 상시 실행 에이전트의 실용성을 끌어올린 업데이트 !

# 개요
- 무엇 : OpenAI가 2026.09.30에 에이전트 작업 특화 모델 GPT-6.1 Sol을 공개함.
- 한 줄 정의 : GPT-6.1 Sol은 상위 모델 GPT-6 Astra에 근접하는 코딩 · 컴퓨터 제어 지능을 5분의 1 가격으로 제공하는 실전 워크플로용 모델이다.
- 원문 : [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol)

# 그래서 도대체 뭔데 ?
- 코드 작성 · 디버깅 · 문서 분석 · 애플리케이션 제어를 장시간 수행하는 에이전트에 맞춘 비용 최적화 모델임.
- 고난도 엔지니어링 벤치마크에서 플래그십인 GPT-6 Astra와 동등한 수준의 작업 성공률을 달성함.
- 프롬프트 캐싱 비용을 100만 토큰당 $0.10까지 낮춰 컨텍스트를 반복 참조하는 에이전트의 실행 부담을 줄임.
- 💡 프롬프트 캐싱 : 자주 바뀌지 않는 지침 · 도구 명세 · 코드를 메모리에 올려두고 재사용해 입력 토큰 비용과 지연 시간을 줄이는 기술
- 💡 컴퓨터 사용 (Computer Use) : 모델이 화면을 보고 브라우저나 데스크톱 프로그램을 직접 조작하며 작업을 완수하는 기능
- 💡 추론 강도 (Reasoning Effort) : 모델이 문제 해결에 투입하는 사고 단계의 깊이를 작업 난이도에 맞춰 조절하는 옵션

# 어떻게 동작하나 ?
1. 컨텍스트 재사용 중심의 프롬프트 캐싱
	- 반복 참조하는 시스템 지침과 저장소 정보를 캐시로 처리해 입력 비용을 100만 토큰당 $0.10까지 낮춤.
	- 표준 입력 대비 95%, 이전 GPT-6 Sol 캐시 가격 대비 50% 저렴한 단가로 대규모 컨텍스트를 유지함.
	→ 반복적인 도구 호출 환경에서도 비용 누적 없이 컨텍스트를 재사용하게 됨.

2. 작업 난이도별 추론 강도 (Reasoning Effort) 분기
	- 간단한 사실 확인이나 코드 수정은 낮은 강도로 빠르게 처리해 오류율을 낮춤.
	- 복잡한 디버깅이나 다단계 과학 워크플로는 최대 강도로 깊게 탐색함.
	→ 지능 수준과 연산 비용의 균형을 작업 단위로 맞추게 됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 복잡한 소프트웨어 엔지니어링 작업에는 단가가 비싼 최상위 모델(GPT-6 Astra)을 써야만 했고, 이전 세대인 GPT-6 Sol은 고난도 코딩과 컴퓨터 조작에서 성능 격차가 존재했음.
- 이번 방식 : DeepSWE v1.1 등 주요 벤치마크에서 상위 모델과 동등한 해결 능력을 유지하면서 토큰 단가와 태스크당 비용을 약 5분의 1 수준으로 낮춤.
→ 캐싱 구조와 추론 효율을 개선해 Astra급 성능을 유지하면서 서빙 비용을 낮췄기 때문임.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| DeepSWE v1.1 성능 | GPT-6 Sol 최고 점수 | GPT-6 Astra와 일치 (GPT-6 Sol 대비 6.4%p 높음) | OpenAI 블로그 |
| DeepSWE v1.1 태스크 비용 | GPT-6 Astra 기준 | GPT-6 Astra 대비 약 5분의 1 | OpenAI 블로그 |
| GDP.pdf 복잡 문서 질의 | 타사 플래그십 (fallbacks 포함) | 타사 플래그십 상회 (비용 50% 미만), Astra 근접 (비용 약 5분의 1) | OpenAI 블로그 |
| AutomationBench (medium) | GPT-6 Sol / 타사 플래그십 | 타사 플래그십 대비 2.2%p 높음 (비용 약 3분의 1, GPT-6 Sol 대비 4.8%p 향상) | OpenAI 블로그 |
| OSWorld 2.0 (max) | GPT-6 Sol / GPT-6 Astra | GPT-6 Sol 대비 7%p 높음 (비용 절반 미만), Astra와 2.1%p 차이 (비용 약 7분의 1) | OpenAI 블로그 |
| Terminal-Bench Science 0.1 태스크 비용 | GPT-6 Astra $23.80 / 타사 플래그십 $23.21 | GPT-6.1 Sol $5.47 (두 모델 대비 75% 이상 절감) | OpenAI 블로그 |
| 사실성 오류율 (low) | GPT-6 Sol 11.4% | GPT-6.1 Sol 7.7% (약 32% 감소, Astra와 1.9%p 이내) | OpenAI 블로그 |
| 표준 토큰 가격 (입력 / 출력) | GPT-6 Astra 기준 (Sol의 5배) | 100만 토큰당 $2 / $10 (Astra 대비 약 5분의 1) | OpenAI 블로그 |
| 캐시 입력 토큰 가격 | GPT-6 Sol 캐시 기준 | 100만 토큰당 $0.10 (표준 대비 95% 할인, GPT-6 Sol 대비 50% 할인) | OpenAI 블로그 |
| Ultrafast 생성 속도 | Codex 내 표준 속도 | Codex 내 표준 속도 대비 최대 8배 | OpenAI 블로그 |

# 주의할 점 / 한계
- 과학 연구 최고난도 한계 : Terminal-Bench Science 0.1에서는 68.1%를 기록한 GPT-6 Astra가 최고 점수이며, 가장 어려운 과학 연구 태스크에는 Astra가 필요함.
- 벤치마크 평가 환경의 차이 : 공식 수치는 연구 환경 및 API 기반 평가 결과이므로 시스템 프롬프트 · 도구 · effort 설정에 따라 실제 상용 ChatGPT 출력과 차이가 있을 수 있음.
- 사실성 오류율 평가 데이터의 특성 : 사실 오류 감소 평가는 사용자가 이전 모델의 오류를 지적했던 까다로운 대화셋 기준이며, 일반적인 사용 환경의 실패율을 반영하지 않음.
- 제공 환경 제한 : 출시 시점에는 ChatGPT Work 및 Codex에서만 사용 가능하며 일반 Chat에는 아직 제공되지 않음.
- 아직 확인 안 된 것 : 총 파라미터 수 · 학습 데이터셋 규모는 원문에 없음.

# 정리
- 플래그십 수준의 코딩 · 업무 자동화 지능을 약 5분의 1 비용과 100만 토큰당 $0.10의 캐시 단가로 제공하는 실전형 모델임.
- 파일 읽기 · 테스트 실행 · GUI 조작을 반복하는 자율 에이전트 파이프라인에 적합함.

# 참고
- [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol) — OpenAI 공식 블로그
- [Addendum to GPT-6 Astra System Card: GPT-6.1 Sol](https://deploymentsafety.openai.com/gpt-6-1-sol) — OpenAI 배포 안전 허브
- [DevDay 2026 Recap](https://openai.com/index/devday-2026-recap/) — OpenAI 공식 블로그
- [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna) — OpenAI 공식 블로그
