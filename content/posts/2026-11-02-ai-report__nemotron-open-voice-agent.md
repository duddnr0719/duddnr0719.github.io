---
weight: 176
title: "NVIDIA Nemotron 오픈 모델 스택 — 워크스테이션 한 대로 음성 대화부터 표정까지 실시간 구동한다"
date: 2026-11-02T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 클라우드 API 없이 로컬 워크스테이션 한 대에서 음성 인식부터 4B 소형 언어 모델 추론, 제로샷 음성 합성, 3D 입모양 애니메이션까지 실시간으로 묶어낸 오프그리드 에이전트 파이프라인이다 !

# 개요
- 무엇 : NVIDIA가 2026.10.30 공개한 오픈 모델 기반 음성 인터랙티브 에이전트 데모 (MonsterHouse)
- 한 줄 정의 : MonsterHouse는 스트리밍 ASR, 소형 언어 모델, 제로샷 TTS, 3D 표정 애니메이션을 단일 워크스테이션에서 결합한 실시간 음성 대화 시스템이다.
- 원문 : [Building a Haunted House with NVIDIA Nemotron Open Models](https://huggingface.co/blog/nvidia/nemotron-halloween)

# 그래서 도대체 뭔데 ?
- 외부 클라우드 통신 없이 로컬 워크스테이션 1대에서 실시간 대화와 3D 표정 렌더링을 끝내는 자립형 음성 에이전트 구축 사례임.
- 방문객 말을 듣고 투덜거리는 해적선 페르소나로 대거리하다가, 예의를 갖추면 태도를 누그러뜨리는 대화 인터랙션을 구현함.
- Nemotron Voice Agent 프레임워크를 기반으로 스트리밍 ASR, 4B급 소형 언어 모델(SLM), 제로샷 음성 합성, 오디오 기반 3D 페이셜 애니메이션을 결합함.
	- 💡 캐시 기반 스트리밍 ASR : 이전 오디오 프레임 연산 결과를 캐시해 중복 계산 없이 새 음성 조각만 처리하는 음성 인식 방식
	- 💡 제로샷 TTS : 별도 화자 훈련 없이 3 ~ 10초 분량 음성 샘플만으로 목소리와 감정 톤을 복제하는 음성 합성 기술
	- 💡 Audio2Face-3D : 음성 파형을 분석해 3D 캐릭터 얼굴 메쉬의 입모양과 표정 블렌드셰이프로 자동 변환하는 신경망

# 어떻게 동작하나 ?
1. 듣기 (Listening)
	- NVIDIA Nemotron 3 ASR (600M) 모델이 방문객의 마이크 입력을 실시간 텍스트로 변환함.
	- Cache-Aware FastConformer-RNNT 구조로 중복 계산을 없애고 80ms, 160ms 단위 청크로 빠르게 전사함.
	→ 방문객 발화가 끝나는 즉시 텍스트 입력이 생성됨.

2. 생각하기 (Thinking)
	- NVIDIA Nemotron 3.5 Bolt E4B 4GB 소형 언어 모델이 대화 흐름을 판단하고 답변을 생성함.
	- 5000개 이상의 멀티턴 대화로 훈련한 LoRA 어댑터를 올려 투덜거리는 해적선 페르소나를 유지함.
	- 방문객이 예의를 갖췄는지 여부 등 상호작용 상태는 모델 내부 메모리가 아니라 외부 애플리케이션 로직에서 추적함.
	→ 답변 문장이 전부 완성될 때까지 기다리지 않고, 말할 수 있는 앞부분 텍스트 조각부터 즉시 음성 합성으로 넘김.

3. 말하기 (Speaking)
	- NVIDIA Magpie TTS Zeroshot 모델이 텍스트를 음성으로 합성함.
	- 3 ~ 10초 분량 레퍼런스 음성으로 거친 해적 목소리를 입히고, 언어 모델이 지정한 7개 감정 태그에 맞춰 연기 톤을 바꿈.
	→ 감정에 맞는 음성 오디오 스트림이 생성됨.

4. 표정 짓기 (Animating)
	- NVIDIA Audio2Face-3D가 잡음 없는 깨끗한 음성 신호를 분석해 Unreal Engine 5 캐릭터의 입모양 애니메이션을 생성함.
	- 스피커로 나가는 소리에는 실시간 에코 음향 효과를 더하고, 입모양 구동용 오디오는 깨끗한 상태를 유지해 애니메이션 정확도를 지킴.
	→ 말하는 타이밍과 입모양이 일치하는 3D 인터랙티브 캐릭터가 완성됨.

5. 눈으로 보기 (Seeing, 보조 기능)
	- NVIDIA Nemotron 3 Nano Omni (30B-A3B) VLM이 카메라 영상을 분석해 방문객 의상을 인식함.
	- YOLO와 ByteTrack이 사람 수를 세고 추적해 대화 시작 트리거를 켬.
	→ 카메라에 사람이 감지되면 자동으로 인사 대화가 시작되는 트리거를 구현함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 클라우드 거대 모델 API에 의존해 네트워크 지연이 길고, 오프라인 독립 환경에서 실시간 3D 표정까지 연동하기 어려웠음.
- 이번 방식 : 스트리밍 ASR, 4B급 소형 언어 모델, 제로샷 음성 합성, 3D 표정 엔진을 로컬 워크스테이션 1대에 올려 네트워크 없이 동작시킴.
- 이전 방식 : 답변 텍스트 생성이 끝날 때까지 기다렸다가 음성 합성을 시작해 응답 지연이 늘어남.
- 이번 방식 : 문장이 완성되기 전에 스트리밍 텍스트를 오디오로 넘기고, 자주 쓰는 인사말과 대사는 오디오 캐시로 건너뜀.
→ 중복 연산을 걷어낸 캐시 기반 음성 파이프라인과 경량 모델 조합으로 단일 머신에서 0.72 ~ 1.70초 수준의 체감 응답 속도를 확보함.

# 숫자로 보면
| 항목 | 이전 / 베이스라인 | 이번 (Bolt E4B Q4 / 파이프라인) | 출처 |
|---|---|---|---|
| 발화 종료 후 오디오 출력 (실시간 생성, 중앙값) | - | 1.70초 (Bolt Q4 & TTS) | [원문 블로그](https://huggingface.co/blog/nvidia/nemotron-halloween) |
| 발화 종료 후 오디오 출력 (사전 캐시, 중앙값) | - | 0.72초 | [원문 블로그](https://huggingface.co/blog/nvidia/nemotron-halloween) |
| 발화 종료 감지 무음 대기 | - | 300ms | [원문 블로그](https://huggingface.co/blog/nvidia/nemotron-halloween) |
| 오디오 립싱크 버퍼 보정 | - | 100ms | [원문 블로그](https://huggingface.co/blog/nvidia/nemotron-halloween) |
| MultiChallenge (복합 벤치) | 39.36 (Gemma-4-E4B-it Q4) | 55.60 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| RoleBench (역할 수행) | 60.51 (Gemma-4-E4B-it Q4) | 71.21 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| RoleMRC (역할 맥락 이해) | 75.24 (Gemma-4-E4B-it Q4) | 79.12 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| ToolSandbox (도구 사용) | 68.31 (Gemma-4-E4B-it Q4) | 74.13 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| Tau2-Bench (에이전트 벤치) | 38.72 (Gemma-4-E4B-it Q4) | 52.32 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| IHEval (지시 준수) | 66.61 (Gemma-4-E4B-it Q4) | 82.40 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| IFBench (지시문 추종) | 42.67 (Gemma-4-E4B-it Q4) | 64.00 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| RelyToolBench (도구 신뢰도) | 67.15 (Gemma-4-E4B-it Q4) | 69.29 | [모델 카드](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) |
| LibriSpeech test-clean WER | - | 2.32% (1.12초 청크) | [ASR 모델 카드](https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b) |
| LibriSpeech test-other WER | - | 4.84% (1.12초 청크) | [ASR 모델 카드](https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b) |

# 주의할 점 / 한계
- 데모 전체 패키징 코드 미공개 : MonsterHouse 애플리케이션 자체의 통합 소스 코드는 공개되지 않았음. 단, 기반 프레임워크인 Nemotron Voice Agent 블루프린트와 사용된 가중치 모델들은 오픈소스로 제공됨.
- 하드웨어 요구 사양 : 언어 · 음성 파이프라인(RTX PRO 6000 Blackwell Max-Q 1장)과 그래픽 · 애니메이션(RTX PRO 4000 Blackwell 1장)으로 총 2장의 고성능 GPU가 들어감. 연산 자원이 부족할 경우 오프라인으로 응답을 미리 대량 생성해 두고 오디오 캐시 위주로 구동하는 구성이 대안으로 제시됨.
- 시각 인식 실전 검증 부족 : 의상 인식 기능은 양 5마리가 등장하는 합성 비디오로 테스트된 단계임. 실제 야간 야외 환경의 조명 변화나 진입로 군중, 실제 의상 인식에 대한 실전 검증이 더 필요함.
- 물리적 하드웨어 미완성 : 사탕을 자동으로 나눠주는 기계 제어 부분은 원문에 구현되지 않았음.

# 정리
- 오픈 모델들을 연결해 외부 통신 없이 로컬 워크스테이션 1대에서 실시간 대화와 표정 애니메이션을 구동할 수 있음을 검증함.
- 대기 시간을 줄이기 위한 스트리밍 텍스트 전달, 오디오 캐시 분기, 클린 오디오 기반 립싱크 분리 같은 실전 엔지니어링 패턴은 로컬 음성 에이전트 구축에 유용함.
- 로컬 환경에서 음성 어시스턴트나 인터랙티브 캐릭터 페르소나를 독립형으로 구축하려는 개발자에게 유용한 참조 구현임.

# 참고
- [Building a Haunted House with NVIDIA Nemotron Open Models](https://huggingface.co/blog/nvidia/nemotron-halloween) — Hugging Face Blog
- [NVIDIA-AI-Blueprints/nemotron-voice-agent](https://github.com/NVIDIA-AI-Blueprints/nemotron-voice-agent) — GitHub
- [NVIDIA-Nemotron-3.5-Bolt-E4B-4GB](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB) — Hugging Face
- [nemotron-speech-streaming-en-0.6b](https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b) — Hugging Face
- [NVIDIA Magpie TTS Zeroshot](https://build.nvidia.com/nvidia/magpie-tts-zeroshot) — NVIDIA NIM
- [Audio2Face-3D](https://github.com/NVIDIA/Audio2Face-3D) — GitHub
- [NVIDIA Nemotron 3 Nano Omni](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16) — Hugging Face
