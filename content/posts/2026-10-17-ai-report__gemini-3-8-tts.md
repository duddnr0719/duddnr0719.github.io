---
weight: 141
title: "Gemini 3.8 TTS — 프롬프트로 목소리를 디자인하고 대사마다 연기를 디렉팅한다"
date: 2026-10-17T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 정해진 프리셋 목소리를 고르는 대신 자연어 프롬프트로 새 캐릭터 음성을 만들고 대사 한 줄마다 연기 톤과 맞장구까지 지시하는 Google DeepMind의 음성 합성 모델 !

# 개요
- 무엇 : Google DeepMind(Gemini Audio Team)가 2026.09.23 발표한 음성 합성 모델 `Gemini 3.8 Flash TTS` 및 `Gemini 3.8 Flash-Lite TTS`
- 한 줄 정의 : `Gemini 3.8 TTS`는 자연어 프롬프트 기반 보이스 생성과 대사 단위 연기 디렉팅을 지원하는 `Gemini 3 Pro` 기반 텍스트-음성 변환(TTS) 모델 제품군이다.
- 원문 : [Gemini 3.8 text-to-speech says hello](https://deepmind.google/blog/say-hello-to-gemini-38-text-to-speech/)

# 그래서 도대체 뭔데 ?
- 기존 TTS가 고정된 프리셋 음성에 텍스트를 읽히는 방식이었다면, 이번 `Gemini 3.8 TTS`는 목소리 자체를 프롬프트로 설계하고 대본의 연기 지시문까지 반영하는 오디오 제작 도구에 가까움.
- 제품군은 용도에 따라 두 가지로 나뉨.
	- `Gemini 3.8 Flash TTS` : 캐릭터 보이스 디자인과 세밀한 연기 연출에 초점을 맞춘 상위 모델임. 게임 · 오디오북 · 팟캐스트 · 인터랙티브 미디어에서 연기 큐 · 호흡(pacing) · 방언 전환(dialect shifts) · 맞장구(backchanneling)를 대사 단위로 제어하는 작업에 쓰임.
	- `Gemini 3.8 Flash-Lite TTS` : 대량 생성과 비용 절감에 초점을 맞춘 경량 모델임. 대규모 더빙 · 오디오 콘텐츠 제작 · 표현력 있는 음성 에이전트 환경에서 톤 · 속도 · 표현 뉘앙스를 제어하는 데 맞춰 설계됨.
- 앞서 2026.09.15 공개된 실시간 대화 모델(`Gemini 3.8 Live`, `Gemini 3.8 Live Extended Thinking`)과 함께 `Gemini 3.8 Audio` 4종 라인업을 구성하며, 기반 아키텍처는 모두 `Gemini 3 Pro`를 공유함.
	- 💡 생성형 보이스 디자인 (Generative voice design) : 역할 · 억양 · 목소리 특성을 자연어 프롬프트로 지정해 세상에 없던 맞춤형 음성을 처음부터 합성해 내는 기능.
	- 💡 맞장구 (Backchanneling) : 대화 도중 상대방의 말을 경청하고 있음을 나타내는 짧은 추임새(`|mhm|`, `|yeah|` 등)를 대본에 넣어 대화의 현장감을 살리는 기능.
	- 💡 화자 흔들림 (Speaker drift) : 긴 오디오를 연속으로 생성할 때 시간이 지나면서 목소리 톤이나 음색이 처음 설정과 달라지는 현상.

# 어떻게 동작하나 ?
1. 보이스 선택 및 생성 (Voice Creation & Replication)
	- 기본 제공되는 보이스 라이브러리는 멕시코 스페인어 · 퀘벡 프랑스어 · 스코틀랜드 영어 등 지역 방언을 포함해 2,000개 이상의 프로덕션용 음성을 지원함.
	- 원하는 목소리가 없으면 `Gemini 3.8 Flash TTS`에서 100개 이상의 언어와 방언을 바탕으로 자연어 프롬프트로 새 보이스를 생성하고, 여러 프로젝트에 걸쳐 저장 · 관리하며 일관된 음성을 재사용할 수 있음.
	- 본인 목소리나 사용 권한이 있는 음성을 쓰고 싶다면 30초 분량의 오디오 샘플만으로 음색 프로필을 복제(Voice replication)함. 이때 무단 도용을 막기 위해 음성 소유자의 구두 동의 녹음(verbal consent recording)이 레퍼런스 화자와 일치하는지 시스템이 먼저 검증함.
	→ 고정된 30개 기본 보이스에 묶이지 않고 캐릭터 맞춤형 음성을 즉시 조달함.

2. 대사 단위 디렉팅 및 다중 화자 연출 (Line-by-Line Direction)
	- 텍스트 입력은 최대 8K 토큰까지 받으며, 대사마다 무대 지시문(stage directions)을 직접 적거나 대본 맥락에 맞춰 모델이 발화 톤을 유도하게 해 한 줄씩 연기 스타일을 지정함.
	- 대본 안에 `<laughs>`, `<sigh>`, `<gasp>` 같은 비언어적 호흡(vocal bursts) 태그와 `|mhm|`, `|yeah|` 같은 맞장구 큐를 삽입해 발화 호흡과 반응 타이밍을 세밀하게 맞춤.
	- 단일 스크립트 안에서 2인 대화(two-speaker scene staging)를 네이티브로 처리해 두 화자의 음색이 섞이지 않게 분리하고 화자 간 대화 주고받기(turn-taking)를 자연스럽게 이어감.
	→ 별도의 오디오 편집 없이 대본 작성만으로 2인 팟캐스트나 드라마 장면을 한 번에 뽑아냄.

3. 장문 오디오 출력 및 워터마킹 (Long-Form Output & Safeguards)
	- 한 번에 최대 64K 토큰 분량의 오디오를 출력하며, 수 시간 분량의 연속 오디오를 생성할 때도 화자 흔들림(speaker drift)을 억제해 일정한 음색과 호흡을 유지함.
	- 생성된 모든 오디오 클립에는 비가청 워터마크인 `SynthID`가 오디오 출력에 직접 삽입되며, 보이스 복제 시에는 `C2PA` 자격 증명 메타데이터가 함께 적용됨.
	→ 장편 오디오북이나 팟캐스트 제작이 가능하면서도 AI 합성 음성 여부를 사후에 판별할 수 있음.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 기존에는 30개 기본 보이스(고정 프리셋) 안에서만 음성을 골라야 했고, 장문 콘텐츠 생성과 2인 각본 제어 성능도 이전 세대인 `Gemini 3.1 Flash TTS` 수준에 머물렀음.
- 이번 방식 : `Gemini 3 Pro` 기반의 `Gemini 3.8 Flash TTS`와 `Gemini 3.8 Flash-Lite TTS`는 2,000개 이상의 보이스 라이브러리와 자연어 보이스 디자인을 결합하고, 대사별 무대 지시문 · 비언어 태그 · 2인 각본 제어를 모델 수준에서 직접 처리함.
→ 단순 텍스트 낭독기에서 벗어나 프롬프트 기반 캐릭터 디자인과 대본 연출이 결합된 음성 스튜디오 방식으로 전환됨.

# 숫자로 보면
| 항목 | 이전 | 이번 (`Gemini 3.8 TTS` 및 동반 `3.8 Audio`) | 출처 |
|---|---|---|---|
| 기본 제공 보이스 수 | 기존 30개 기본 보이스 | 2,000개 이상 라이브러리 + 프롬프트 무한 생성 | DeepMind 공식 블로그 |
| 지원 언어 및 방언 | 원문에 없음 | TTS 100개 이상 언어 · 방언 (동반 `3.8 Live` 자동 전환 97개 언어) | DeepMind 공식 블로그 · Live 블로그 |
| 보이스 복제 최소 샘플 | 원문에 없음 | 30초 오디오 샘플 + 구두 동의 녹음 | DeepMind 공식 블로그 |
| 입출력 토큰 한도 | 원문에 없음 | TTS 입력 8K / 출력 64K (동반 `3.8 Live` 입력 128K / 출력 64K, 아바타 출력 24K) | Gemini 3.8 Audio 모델 카드 |
| Hume AI Voice Design Benchmark | 원문에 없음 (타 모델 수치 미기재) | `Gemini 3.8 Flash TTS` 전체 1위 (71.4점) · 억양 모델링 1위 (60.8점) | DeepMind 공식 블로그 |
| Hume AI Overall Quality Index | `Gemini 3.1 Flash TTS` (세부 점수 원문에 없음) | `Gemini 3.8 Flash TTS` 1위 · `Gemini 3.8 Flash-Lite TTS` 2위 | DeepMind 공식 블로그 |
| 동반 `3.8 Live Extended Thinking` 성능 | 원문에 없음 (타 모델 수치 미기재) | `Artificial Analysis` Speech to Speech Quality Index 1위 (82.6점) · `τ-Voice` 1위 (68.6%) · `Sierra τ-Voice-banking` 1위 (35.1%) · `Big Bench Audio` 97.7% | Gemini 3.8 Live 공식 블로그 |

# 주의할 점 / 한계
- 원문이 밝힌 모델 한계 : 공식 모델 카드(`Gemini 3.8 Audio`)에 따르면 파운데이션 모델 특유의 환각(hallucinations) 가능성이 남아 있으며, 간헐적인 응답 지연(slowness)이나 타임아웃(timeout) 이슈가 발생할 수 있음. 또한 모델의 지식 컷오프는 2025.01 기준임.
- 출시 예정 기능의 시차 : 기존 라이브러리 보이스를 골라 프롬프트로 음색 · 피치 · 속도 · 억양만 살짝 바꾸는 보이스 리믹싱(Voice remixing) 기능과 `Gemini Enterprise` API 지원은 발표일(2026.09.23) 기준 아직 출시 예정(Coming soon) 상태임.
- 평가 벤치마크의 조건 : 1위를 기록한 `Hume AI`의 `Real World VoiceEQ`는 4개 모달리티에 걸친 100만 건 이상의 인간 판단과 객관적 지표(정확도 · 타이밍 · 음향) 및 자동 채점기를 결합한 외부 평가 체계이나, 블로그 본문에는 `Overall Quality Index`의 세부 점수와 `Voice Arena`의 언어별 세부 점수가 그래프 이미지로만 제시되고 텍스트 수치로는 적혀 있지 않음.
- 아직 확인 안 된 것 : 모델 파라미터 크기, 토큰당 API 과금 단가, 평균 응답 지연 시간(ms / RTF), 학습 데이터셋의 상세 시간 분량은 원문에 없음.

# 정리
- 자연어 프롬프트로 새 목소리를 디자인하거나 30초 샘플로 음성을 복제한 뒤, `<laughs>`나 `|mhm|` 같은 큐를 넣어 2인 대화까지 한 번에 연출할 수 있는 음성 합성 모델임.
- 현재 `Google AI Studio`(보이스 디자인 워크스페이스 · 2인 각본 에디터)와 `Gemini API`, `Gemini Notebook`, `Google Vids`에 적용되었고 `Agora` · `LiveKit` · `Pipecat` · `Vercel` 연동도 지원하므로, 게임 · 오디오북 · 팟캐스트 제작이나 대규모 다국어 더빙 · 음성 에이전트를 구축하는 환경에서 활용할 수 있음.

# 참고
- [Gemini 3.8 text-to-speech says hello](https://deepmind.google/blog/say-hello-to-gemini-38-text-to-speech/) — Google DeepMind Blog (2026.09.23)
- [Gemini 3.8 Audio - Model Card](https://deepmind.google/models/model-cards/gemini-3-8-audio/) — Google DeepMind Model Cards (2026.09.15)
- [Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/) — Google Blog (2026.09.15)
- [Real World VoiceEQ](https://www.hume.ai/rw-voice-eq) — Hume AI
