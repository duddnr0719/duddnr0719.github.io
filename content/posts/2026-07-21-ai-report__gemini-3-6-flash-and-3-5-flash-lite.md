---
weight: 147
title: "Gemini 3.6 Flash & 3.5 Flash-Lite — 출력 토큰은 17% 줄이고 350 tok/s 속도로 에이전트를 확장한다"
date: 2026-07-21T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 에이전트 다단계 루프에서 토큰 소모를 최대 65% 줄인 3.6 Flash와 초당 350 토큰 속도로 밀어붙이는 3.5 Flash-Lite의 출시 !

# 개요
- 무엇 : Google DeepMind가 2026.07.21 공개한 Gemini 3.6 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber 모델 라인업
- 한 줄 정의 : Gemini 3.6 Flash와 3.5 Flash-Lite는 불필요한 출력 토큰을 깎아내고 호출 속도를 끌어올려 대규모 에이전트 워크플로우를 지탱하도록 설계된 경량 모델이다.
- 원문 : [Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://deepmind.google/blog/introducing-gemini-3-6-flash-3-5-flash-lite-and-3-5-flash-cyber/)

# 그래서 도대체 뭔데 ?
- 실무에서 에이전트를 프로덕션에 올릴 때 가장 큰 걸림돌은 긴 지연시간과 누적되는 토큰 비용임.
- 단발 질의응답과 달리 에이전트는 코드 작성 · 도구 호출 · 결과 확인 단계를 계속 반복하기 때문임.
- 3.6 Flash는 3.5 Flash 대비 출력 토큰 사용량을 17% 줄이고, DeepSWE 같은 작업에서는 최대 65%까지 절감함.
- 3.5 Flash-Lite는 초당 350 토큰의 빠른 속도를 앞세워 검색과 대량 문서 처리를 소화하는 고처리량 모델임.
- 보안 영역에서는 3.5 Flash Cyber 모델이 취약점 탐지 에이전트 시스템인 CodeMender와 결합되어 공개됨.
	- 💡 워크호스 모델 (Workhorse Model) : 최상위 플래그십의 비싼 가격 대신 실무 파이프라인에서 대량 트래픽을 감당하는 실전 주력 모델.
	- 💡 에이전틱 워크플로우 (Agentic Workflow) : 모델이 단순 답변 생성을 넘어 도구 호출과 환경 피드백을 주고받으며 자율 루프를 도는 방식.

# 어떻게 동작하나 ?
1. 출력 토큰 최적화와 장황함 축소
	- 3.6 Flash는 다단계 워크플로우에서 불필요한 추론 단계와 도구 호출 횟수를 줄임.
	- 코드 편집 시 불필요한 코드 수정과 반복 실행 루프를 줄임.
	→ 동일한 작업을 완수하면서 토큰 소모량과 응답 대기 시간을 단축함.
2. 클라이언트 사이드 컴퓨터 사용(Computer Use) 도구 내장
	- 화면을 인식하고 마우스와 키보드로 시스템을 제어하는 Computer Use 도구를 API 레벨에서 기본 지원함.
	- OSWorld-Verified 벤치마크에서 3.6 Flash는 83.0%, 3.5 Flash-Lite는 74.0%를 기록함.
	→ API 및 엔터프라이즈 환경에서 내장 도구 형태로 화면 제어 에이전트를 연동할 수 있음.
3. 사고 수준(Thinking Levels) 제어로 워크로드 분기
	- 3.5 Flash-Lite는 minimal 및 low thinking 설정을 통해 단순 분류 · 대량 데이터 처리를 저지연 · 저비용으로 처리함.
	- 다단계 추론이나 복합 서브에이전트 조율이 필요할 때만 higher thinking 수준을 켜서 지능을 동적으로 배분함.
	→ 작업 유형에 맞춰 가벼운 대량 처리와 다단계 추론 작업을 유연하게 분기함.
4. 다중 에이전트 보안 오케스트레이션 (CodeMender)
	- 3.5 Flash Cyber 모델 복수 개가 협업하여 코드베이스의 취약점을 분석하고 수정 패치를 생성함.
	- 정적 분석, 동적 퍼징, LLM 비평 도구를 엮어 회귀 버그 없는 패치를 검증하고 종합 보고서를 작성함.
	→ 취약점 벤치마크인 CyberGym에서 프런티어급의 경쟁력 있는 성능을 달성함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 3.5 Flash는 다단계 에이전트 워크플로우에서 불필요한 추론 단계와 도구 호출이 발생했고, 원치 않는 코드 수정과 실행 루프가 반복됨. 출력 단가도 1M 토큰당 $9.00 수준이었음.
- 이번 방식 : 3.6 Flash는 불필요한 출력을 줄이고 단가를 1M 토큰당 $9.00에서 $7.50으로 낮춤. 3.5 Flash-Lite는 SWE-Bench Pro 54.2%(이전 38.3%)로 코딩 성능을 높이면서 350 tok/s 속도를 제공함.
→ 출력 토큰과 불필요한 호출 단계를 줄여 에이전트 루프의 지연시간과 운영 비용을 낮춤.

# 숫자로 보면
| 항목 | 이전 (3.5 Flash / 3.1 Flash-Lite) | 이번 (3.6 Flash / 3.5 Flash-Lite) | 출처 |
|---|---|---|---|
| 3.6 Flash 출력 토큰 절감률 | 기준선 (0%) | 17% 감소 (DeepSWE 최대 65% 절감) | Artificial Analysis / Datacurve |
| 3.6 Flash 출력 단가 ($/1M 토큰) | $9.00 | $7.50 | 공식 모델 카드 |
| 3.6 Flash SWE-Bench Pro (Public) | 55.1% | 58.7% | 공식 모델 카드 |
| 3.6 Flash DeepSWE v1.1 | 37% | 49% | 공식 모델 카드 |
| 3.6 Flash MLE-Bench | 49.7% | 63.9% | 공식 모델 카드 |
| 3.6 Flash OSWorld-Verified | 78.4% | 83.0% | 공식 모델 카드 |
| 3.6 Flash GDPVal-AA v2 (Elo) | 1349 | 1421 | 공식 모델 카드 |
| 3.5 Flash-Lite 출력 속도 | - | 350 output tokens/s | Artificial Analysis |
| 3.5 Flash-Lite SWE-Bench Pro | 38.3% (3.1 Flash-Lite) | 54.2% | 공식 모델 카드 |
| 3.5 Flash-Lite Terminal-bench 2.1 | 31.0% (3.1 Flash-Lite) | 54.0% | 공식 모델 카드 |
| 3.5 Flash-Lite OSWorld-Verified | 54.3% (3.1 Flash-Lite) | 74.0% | 공식 모델 카드 |

# 주의할 점 / 한계
- 지식 컷오프는 2026.03 기준이며 일부 도메인은 2025.01 수준에 머무름.
- 파운데이션 모델의 일반적 한계인 환각(hallucination) 위험이 있고, 일시적인 지연이나 타임아웃이 발생할 수 있음.
- 3.5 Flash Cyber는 오용 방지를 위해 일반 공개되지 않고 정부 및 신뢰 파트너 대상 CodeMender 파일럿 프로그램으로만 제한 제공됨.

# 정리
- 출력 토큰 낭비를 17% 줄인 3.6 Flash와 350 tok/s 속도로 밀어붙이는 3.5 Flash-Lite의 실속형 조합.
- 수백 번의 에이전트 루프 호출 비용이 부담스럽거나 고처리량 문서 검색 파이프라인을 굴리는 팀에 적합함.

# 참고
- [Introducing Gemini 3.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://deepmind.google/blog/introducing-gemini-3-6-flash-3-5-flash-lite-and-3-5-flash-cyber/) — Google DeepMind 공식 블로그
- [Gemini 3.6 Flash Model Card](https://deepmind.google/models/model-cards/gemini-3-6-flash/) — Google DeepMind 모델 카드
- [Gemini 3.5 Flash-Lite Model Card](https://deepmind.google/models/model-cards/gemini-3-5-flash-lite/) — Google DeepMind 모델 카드
- [Introducing CodeMender: an AI agent for code security](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/) — Google DeepMind 공식 블로그
