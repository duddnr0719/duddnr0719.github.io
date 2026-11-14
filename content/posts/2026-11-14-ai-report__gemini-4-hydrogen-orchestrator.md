---
weight: 188
title: "Gemini 4 Hydrogen — 2.5배 빨라진 에이전트 실행과 동적 멀티 모델 전환을 결합한다"
date: 2026-11-14T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> Artificial Analysis 지능 지수에서 Gemini 4 Argon을 앞지르고 Gemini 3.8 Flash보다 작업을 2.5배 빨리 끝내며, 단일 세션 안에서 상위 모델과 역할을 주고받는 실행 모델 Gemini 4 Hydrogen이 공개됨 !

# 개요
- 무엇 : Google DeepMind가 2026.11.12(업데이트 2026.11.13)에 코딩 · 에이전트 실행에 맞춘 Gemini 4 Hydrogen과 멀티 모델 전환 기능 Orchestrator를 발표함.
- 한 줄 정의 : Gemini 4 Hydrogen은 Gemini 4 Carbon에서 파생되어 1M 컨텍스트와 4단계 추론 조절을 지원하고, 단독으로 또는 상위 모델과 짝을 이뤄 코드 작성 · 테스트 · 검증을 빠르게 처리하는 실행 모델이다.
- 원문 : [Introducing Gemini 4 Hydrogen](https://deepmind.google/blog/introducing-gemini-4-hydrogen/)

# 그래서 도대체 뭔데 ?
- 시스템 설계나 까다로운 버그 추적에는 Gemini 4 Carbon · Argon 같은 프론티어 모델이 유리하지만, 코드 수정 · 테스트 반복까지 전부 프론티어 모델로 돌리면 루프가 느려지고 쿼터가 소모됨.
- Gemini 4 Hydrogen은 단독으로 Gemini 3.8 Flash를 대체하는 실행 모델로 작동하며, 멀티 모델 워크플로에서는 Orchestrator를 통해 상위 모델이 세운 계획을 받아 빠르게 실행 · 검증하는 역할을 맡음.
- 입출력 통합 최대 1M 토큰 컨텍스트를 단일 요금(입력 1M 토큰당 $1.50, 출력 1M 토큰당 $7.50)으로 제공하며, 기본 동기 출력 64K와 백그라운드 롱 디코드(Background long decode) 최대 1M 출력 토큰을 지원해 시각 · 문서 기반의 멀티모달 지식 작업(MKA 53.4%)도 처리함.
	- 💡 Orchestrator : Google Antigravity에서 단일 세션 안에 Carbon(또는 Argon)과 Hydrogen을 묶어 단계마다 양방향으로 자동 전환하는 기능.
	- 💡 Background long decode : 기본 동기 출력(최대 64K 토큰) 외에 백그라운드 디코딩으로 최대 1M 토큰까지 출력하는 방식.
	- 💡 MKA (Multimodal Knowledge Agent) : Google DeepMind와 Artificial Analysis가 10개 산업군 · 83개 직종 전문가와 만든 200개 과제의 시각 · 문서 에이전트 벤치마크.

# 어떻게 동작하나 ?
1. 단일 세션 내 양방향 동적 전환 (Orchestrator)
	- Carbon이 읽기 전용 단계로 진입해 의존성을 탐색하고 모호성을 해결하며 재계획 트리거가 담긴 구체적 계획을 세움.
	- 이어서 Hydrogen이 제어권을 넘겨받아 코드 편집 · 패키지 업데이트 · 테스트 실행을 수행함.
	- 실행 중 막힘이 생기면 다시 Carbon으로 돌아가 상태를 점검하고 계획을 수선한 뒤 실행을 재개함.
	→ Carbon 단독에 근접한 과제 성공률을 유지하면서 평균 완료 시간을 19% 줄이고 쿼터 소모를 24% 아끼게 됨.

2. 격리 워크스페이스 병렬 분업과 SDK 파이프라인
	- 병렬 에이전트 작업 시 Carbon이 코디네이터를 맡고, Hydrogen이 격리된 워크스페이스에서 워커 · 검증자로 동시에 빌드와 테스트를 돌림.
	- Antigravity SDK로 역할별 파이프라인을 직접 구성할 수도 있어(오픈소스 이슈 분류 시스템 데모 기준), Hydrogen이 이슈 분류 · 코딩 · 코드 검색 · 명확화 질문 · PR 코멘트 기반 UI 반복 수정을 맡고 Carbon이 대규모 리팩토링 · 신규 기능 · 보안 점검을 분담함.
	→ 토큰 비용을 키우지 않으면서 병렬 빌드 · 테스트로 복잡한 프로젝트 처리 속도를 높임.

3. 네이티브 병렬 배칭 탐색과 4단계 추론 깊이 조절
	- 대규모 리포지토리 탐색 시 파일을 하나씩 열지 않고 파일 읽기 · 검색 호출을 네이티브로 병렬 배칭해 처리하며, 무관한 파일을 다시 쓰지 않고 필요한 위치만 고치는 외과적 편집을 수행함.
	- 추론 깊이를 `low` · `medium` · `high`(기본값) · `xhigh`(신규 최고 단계) 4단계로 두어 과제가 요구하는 추론 깊이만큼만 대기 시간과 비용을 지불하도록 조절함.
	→ 엔터프라이즈 파트너의 복잡한 그래프 · SQL · 데이터 워크플로 초기 테스트에서 Gemini 3.8 Flash 대비 실행 속도는 2배 ~ 2.8배 빨라지고 토큰 사용량은 12% ~ 23% 줄어듦.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : Gemini 3.8 Flash는 터미널 과제(Terminal-Bench 4.1 18.2%)에서 성공률이 낮았고, 정적 모델 라우터는 첫 프롬프트만 보고 난이도를 추측해 작업 전체를 단일 저가 모델로 고정 라우팅했음.
- 이번 방식 : Hydrogen 단독 성능을 57%로 3배 이상 높였고, Orchestrator가 단일 작업 궤적 안에서 계획 · 실행 · 복구 단계마다 Carbon과 Hydrogen을 양방향으로 오가며 처리함.
→ 긴 에이전트 작업은 진행 도중 요구 복잡도가 달라져 정적 라우터가 깨지기 쉬운데, 양방향 동적 전환으로 이를 해결하고 Hydrogen 자체의 도구 사용 · 코딩 평가에서도 Gemini 3.8 Flash 대비 부정합 행동과 편법 단축을 12배 줄임.

# 숫자로 보면
| 항목 | 이전 / 비교 대상 | 이번 (Gemini 4 Hydrogen) | 출처 |
|---|---|---|---|
| Artificial Analysis Intelligence Index | 50점 (Gemini 4 Argon) | 51점 (기본 `high`) / 54점 (`xhigh`) | DeepMind Blog · Antigravity Blog |
| Terminal-Bench 4.1 | 18.2% (Gemini 3.8 Flash) | 57% (3배 이상 향상) | DeepMind Blog · Antigravity Blog |
| 단독 작업 속도 및 허위 주장 | Gemini 3.8 Flash 기준 | 기본 `high` 설정에서 완료 속도 2.5배 · 허위 주장 5배 이상 감소 | DeepMind Blog |
| 엔터프라이즈 그래프 · SQL · 데이터 워크플로 | Gemini 3.8 Flash 기준 | 실행 속도 2배 ~ 2.8배 · 토큰 12% ~ 23% 절감 | DeepMind Blog |
| Orchestrator 쿼터 · 소요 시간 | Gemini 4 Carbon 단독 기준 | 평균 쿼터 24% 절감 · 완료 시간 19% 단축 | DeepMind Blog(4.0) · Antigravity Blog(4.1) |
| 전문 도메인 · 멀티모달 벤치마크 | 동급 및 전체 비교 | HLE-Diamond 58.8%(동급 선두) · Vals Tax Agent Bench 52.3%(전체 1위) · Vals Legal Research Bench 55.8%(공동 1위) · MKA 53.4% · Agents' Last Exam v1.1 71.6% | DeepMind Blog |
| 에이전트 정합성 및 오거절 | Gemini 3.8 Flash 기준 | 권한 과잉 최대 81% 감소 · 과소 수행 최대 79% 감소 · 내부 정직성 평가 94% · HealthBench Pro 오거절 0.4% 미만 | DeepMind Blog |
| 내부 자동 안전성 평가 (vs 3.8 Flash) | Gemini 3.8 Flash 기준 | 텍스트 안전성 +0.80pp · 다국어 안전성 +1.10pp · 이미지-텍스트 안전성 +7.00pp · 거절 어조(Tone) -0.65pp · 부당 과잉 거절(Unjustified-refusals) +5.57pp | Model Card |

# 주의할 점 / 한계
- 모델 카드에 명시된 한계로 환각, 간헐적 지연 · 타임아웃이 발생할 수 있으며, 높은 추론 단계에서는 성능을 높이려다 토큰 소모가 늘어날 수 있음 (지식 컷오프 2026.03, 일부 도메인은 최신성이 떨어질 수 있음).
- 내부 자동 안전성 평가에서 이미지-텍스트 안전성은 +7.00pp 올랐으나, 부당 과잉 거절도 +5.57pp 늘어나 멀티모달 프롬프트에서 과잉 거절 회귀가 나타남.
- CBRN(생물학) 및 사이버보안 평가에서 임계 역량 수준(CCL)에는 도달하지 않았으나 두 영역 모두 CCL 경보 임계치에는 도달했으며, 상세 Safety & Security Report는 미공개 상태임.
- Orchestrator의 쿼터 24% 절감 · 시간 19% 단축 기준이 DeepMind 블로그에는 Terminal-Bench 4.0, Antigravity 블로그에는 Terminal-Bench 4.1로 다르게 표기됨.
- 아직 확인 안 된 것 : 모델 파라미터 크기, 세부 아키텍처 구조, SWE-sweep 및 AutomationBench-AA 점수는 원문에 없음.

# 정리
- Gemini 4 Hydrogen은 1M 컨텍스트와 4단계 추론 조절을 지원하며, 기본 `high` 설정에서 지능 지수로 Gemini 4 Argon을 앞지르고(51점 vs 50점) Gemini 3.8 Flash 대비 완료 속도를 2.5배, Terminal-Bench 4.1 점수를 57%(vs 18.2%)로 높인 실행 모델임.
- Gemini 3.8 Flash에서 전환하는 코딩 · 데이터 워크플로 팀이나, Google Antigravity의 Orchestrator · SDK로 상위 모델(Carbon · Argon)에 설계 · 계획을 맡기고 코드 수정 · 테스트는 Hydrogen으로 돌려 쿼터와 시간을 아끼려는 환경에서 써먹을 만함.

# 참고
- [Introducing Gemini 4 Hydrogen](https://deepmind.google/blog/introducing-gemini-4-hydrogen/) — Google DeepMind Blog
- [Gemini 4 Hydrogen Model Card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Hydrogen-Model-Card.pdf) — Google DeepMind
- [Gemini 4 Hydrogen and Orchestrator](https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity) — Google Antigravity Blog
- [Introducing the Multimodal Knowledge Agent benchmark](https://blog.google/innovation-and-ai/models-and-research/gemini-models/multimodal-knowledge-agent-benchmark/) — Google DeepMind Blog
