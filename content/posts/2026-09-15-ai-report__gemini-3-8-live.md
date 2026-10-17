---
weight: 154
title: "Gemini 3.8 Live — 백그라운드 추론과 동시 발화로 음성 에이전트를 완성한다"
date: 2026-09-15T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 백그라운드 다단계 추론과 실시간 음성 발화를 엮어 끊김 없는 음성 대화를 구현한다 !

# 개요
- 무엇 : Google DeepMind가 2026.09.15 Gemini 3.8 Live 및 3.8 Live Extended Thinking을 공개함.
- 한 줄 정의 : Gemini 3.8 Live 계열은 실시간 음성 스트리밍 환경에서 다단계 추론과 도구 호출을 대화 단절 없이 수행하는 멀티모달 음성 모델이다.
- 원문 : [Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking](https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/)

# 그래서 도대체 뭔데 ?
- 실시간 음성 대화 도중 복잡한 추론이나 도구 호출이 필요할 때 침묵하지 않고 즉시 반응함.
- 생각을 거치는 동안 "확인해 보겠습니다" 같은 초기 음성 신호를 던지고, 백그라운드 다단계 작업 과정을 실시간으로 말하면서 대화를 이어감.
- 빠른 응답과 비용 절감에 초점을 맞춘 Gemini 3.8 Live와 고난도 다단계 추론을 수행하는 Gemini 3.8 Live Extended Thinking 두 가지 모델로 나뉨.
	- 💡 Live Extended Thinking : 모델이 백그라운드에서 추론하고 도구를 실행하는 동시에 사용자에게 진행 과정을 음성으로 해설하는 동시 추론 · 발화 기능
	- 💡 Barge-in : 모델이 음성을 출력하는 중에도 사용자가 말을 끊고 끼어들 수 있는 양방향 음성 제어 메커니즘

# 어떻게 동작하나 ?
1. 실시간 멀티모달 스트림 수신
	- 클라이언트가 WebSocket(WSS) 연결을 통해 16kHz 16-bit PCM 오디오와 최대 1FPS 이미지, 텍스트를 모델로 스트리밍함.
	→ 음성과 시각 정보를 하나의 상태 유지 세션에서 즉시 결합함.

2. 실시간 언어 감지 및 사용자 끼어들기 처리
	- 대화 도중 사용자의 음성을 감지해 97개 언어 사이를 자동으로 인식하고 실시간으로 전환함.
	- 사용자가 모델 발화 도중 말을 시작하면 Barge-in 기능이 즉각 동작해 기존 출력을 중단함.
	→ 언어가 바뀌거나 대화 타이밍이 겹쳐도 대화 흐름이 끊기지 않음.

3. 백그라운드 추론과 음성 발화의 동시 실행
	- 고난도 질의나 도구 호출이 들어오면 모델이 침묵 상태로 멈추지 않고 초기 음성 신호를 먼저 발화함.
	- 백그라운드에서 다단계 추론과 API 호출을 처리하면서, 현재 무엇을 확인하고 있는지 실시간으로 해설함.
	→ 긴 지연 없이 모델과 직관적으로 협업할 수 있게 됨.

4. 24kHz 오디오 출력 및 워터마크 합성
	- 계산된 결과를 24kHz 16-bit PCM 오디오 스트림으로 실시간 변환해 전송함.
	- 생성된 모든 음성 신호에는 귀에 들리지 않는 SynthID 비가청 워터마크가 직접 내장됨.
	→ 음질 저하 없이 귀에 들리지 않는 방식으로 AI 생성 여부를 감지할 수 있게 됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 도구 실행이나 복잡한 추론 작업이 필요할 때 모델이 대화를 멈추고 침묵 상태에 머물렀음.
- 이번 방식 : 추론 연산과 음성 발화를 동시에 수행(Reason and speak simultaneously)하고, 백그라운드에서 도구와 API를 실행하는 동안에도 실시간 진행 과정을 음성으로 해설하며 대화를 지속함.
→ 백그라운드 다단계 추론과 음성 발화가 병렬로 처리되어 대화 흐름이 끊기지 않음.

# 숫자로 보면
| 항목 | 이전 | 이번 (Gemini 3.8 Live 계열) | 출처 |
|---|---|---|---|
| 음성 대화 품질 지수 (Speech to Speech Quality Index) | - | 82.6점 (Extended Thinking 종합 1위) | Artificial Analysis |
| 음성 에이전트 작업 완료율 (τ-Voice) | - | 68.6% (Extended Thinking 1위) | 공식 블로그 |
| 은행 도메인 에이전트 완료율 (Sierra τ-Voice-banking) | - | 35.1% (Extended Thinking) | Sierra |
| 음성 추론 벤치마크 (Big Bench Audio) | - | 97.7% (Extended Thinking) | 공식 블로그 |
| 음성 에이전트 선호도 (Speech Agent Arena) | - | 2위 (Gemini 3.8 Live) | Artificial Analysis |
| 입력 컨텍스트 창 | - | 최대 128K 토큰 | 공식 모델 카드 |
| 출력 토큰 한도 | - | 최대 64K 토큰 (Live Avatar 24K) | 공식 모델 카드 |
| 실시간 전환 지원 언어 | 70개 언어 (Live API 가이드) | 97개 언어 (대화 중 자동 감지) | 공식 블로그 · Live API 가이드 |

# 주의할 점 / 한계
- 지식 한계 : 지식 컷오프는 2025년 1월까지임.
- 파운데이션 모델 고유 한계 : 일반적인 파운데이션 모델처럼 환각(hallucination)이 발생할 수 있음.
- 지연 변동 : 간헐적인 속도 저하나 타임아웃이 발생할 수 있음.
- Live Avatar 제약 : 실시간 아바타 영상 합성 기능은 장시간 연속 대화가 아니라 몇 분 단위 상호작용으로 제한됨.
- 안전성 평가 : 프런티어 안전 평가는 Gemini 3.7 Flash 평가 결과를 준용함.

# 정리
- 실시간 음성 대화 중 발생하는 추론 지연과 침묵을 동시 추론 · 발화와 백그라운드 진행 해설로 줄임.
- 고객 지원 상담, 실시간 작업 안내, 차량 및 로보틱스 제어처럼 복잡한 업무를 실시간 음성으로 처리해야 하는 서비스에 도입할 만함.

# 참고
- [Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking](https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/) — Google DeepMind 공식 블로그
- [Gemini 3.8 Audio Model Card](https://deepmind.google/models/model-cards/gemini-3-8-audio/) — Google DeepMind 공식 모델 카드
- [Gemini Live API Overview](https://ai.google.dev/gemini-api/docs/live-api) — Google AI 문서
- [SynthID Overview](https://deepmind.google/models/synthid/) — Google DeepMind 공식 기술 소개
