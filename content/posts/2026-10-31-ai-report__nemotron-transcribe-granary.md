---
weight: 173
title: "NVIDIA Nemotron 3.5 Transcribe와 Granary v2 — 프롬프트로 제어하는 다국어 음성 전사와 데이터 파이프라인"
date: 2026-10-31T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 프롬프트 한 줄로 전사 스타일과 화자 분리를 제어하고 4B 활성 파라미터로 상용 API급 정확도를 뽑아내는 오픈 음성 모델과 데이터 파이프라인 !

# 개요
- 무엇 : NVIDIA가 2026.10.28에 오픈 음성 파운데이션 모델 Nemotron 3.5 Transcribe와 데이터 큐레이션 파이프라인 Granary v2를 공개함.
- 한 줄 정의 : Nemotron 3.5 Transcribe는 자연어 프롬프트로 전사 스타일과 화자 분리, 번역을 제어하는 하이브리드 MoE 음성-언어 모델이다.
- 원문 : [NVIDIA Nemotron 3.5 Transcribe and Granary v2: Intelligent Multilingual Transcription You Can Prompt and Adapt](https://huggingface.co/blog/nvidia/nemotron-transcribe-granary)

# 그래서 도대체 뭔데 ?
- 녹음된 음성을 텍스트로 바꿀 때 단순 받아쓰기를 넘어 발화자 구분, 전문 용어 표기, 추임새 제거 여부를 자연어 명령으로 제어하는 모델임.
- 40개 언어 전사와 31개 언어 영-외 양방향 번역, 13개 언어 화자 분리를 단일 체크포인트로 처리함.
- 34B 전체 파라미터 중 토큰당 약 4.3B(언어 백본 3.5B + 오디오 인코더 약 800M)만 활성화되는 MoE 구조로 연산 부담을 낮춤.
- 학습 데이터 구축에 쓰인 463,062시간 규모의 4단계 큐레이션 파이프라인 Granary v2와 도메인 파인튜닝 레시피까지 함께 공개함.
	- 💡 MTP (Multi-Token Prediction) : 한 번의 순전파에서 미래의 여러 토큰을 동시에 예측해 추론 속도를 높이는 기법.
	- 💡 Sortformer : 음향 특성과 화자 특징을 동시에 추적해 겹쳐 말하는 구간에서도 발화자를 분리하는 트랜스포머 아키텍처.
	- 💡 cpWER (concatenated minimum-permutation WER) : 다중 화자 음성에서 화자 라벨 순열 매칭 후 단어 오류율을 계산하는 평가 지표.

# 어떻게 동작하나 ?
1. 오디오 병렬 인코딩 (Parallel Expert Encoder)
	- 입력 음성이 들어오면 600M ASR 인코더와 99M Sortformer 화자 인코더가 병렬로 음향 특징과 화자 신호를 추출함.
	- CTC 타임스탬프 헤드가 단어 단위 타임스탬프 정렬을 담당함.
	- 1,280차원 커넥터를 거쳐 2,688차원 투영 레이어로 언어 백본 공간에 맞춤.
	→ 음향 특징과 화자 신호가 분리되지 않고 언어 백본으로 함께 전달됨.

2. 하이브리드 MoE 언어 백본 디코딩
	- Nemotron-3.5 Lightning 30B-A3B 백본이 오디오 임베딩과 자연어 프롬프트를 함께 입력받음.
	- Mamba-2와 트랜스포머 어텐션이 결합되어 긴 컨텍스트(최대 65,536 토큰, 1시간 녹음)를 처리함.
	- 토큰 디코딩 시 전체 30B 언어 백본 중 3.5B만 활성화되어 연산량을 줄임.
	→ 긴 오디오(최대 1시간)를 처리하면서도 적은 활성 파라미터로 연산량과 메모리를 크게 아낌.

3. 프롬프트 기반 출력 제어
	- 사용자가 지시문에 스타일을 적으면 모델이 그에 맞춰 형식을 결정함.
	- 필러를 포함하는 축어적 전사와 필러를 제거한 정제 전사를 프롬프트로 전환함.
	- 도메인 전문 용어 목록을 컨텍스트로 전달하면 문맥에 맞춰 해당 철자를 우선 반영함.
	→ 별도 전처리나 후처리 파이프라인 없이 단일 패스로 최종 텍스트가 완성됨.

4. Granary v2 4단계 데이터 큐레이션
	- Audio Prep 단계에서 VAD와 화자 추적으로 음성을 분할함.
	- ASR 단계에서 주 모델과 대체 모델을 배치하고 환각 검증을 거쳐 전사본을 확보함.
	- Text 단계에서 축어형(tn_raw), 비정제 역정규화(itn_raw), 정제 역정규화(itn_clean) 3개 타겟을 동시 생성함.
	- HiFi 단계에서 잡음과 클리핑을 걸러 고품질 서브셋을 추려냄.
	→ 모델이 프롬프트 지시를 따를 수 있도록 포맷별 명시적 정답 쌍을 대량 구축함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : ASR 모델로 텍스트를 뽑고, 별도 화자 분리 모델을 돌린 뒤, LLM으로 텍스트를 후처리하거나 번역하는 파편화된 파이프라인이었음.
- 이번 방식 : 단일 체크포인트 안에서 ASR, 화자 태깅(`<spk:0>` ~ `<spk:7>`), 번역, 질의응답을 자연어 프롬프트 한 번으로 끝냄.
→ 이전에는 단계마다 오류가 누적되고 파이프라인 지연이 컸으나, 음향과 화자 신호를 언어 모델이 직접 받아 한 번에 디코딩하므로 누락과 왜곡이 줄어듦.

- 이전 방식 : 전문 도메인(의료 등) 전사 시 해당 분야의 실제 음성 녹음과 전사 라벨이 필수적이었음 (학습 데이터가 없으면 미세조정 불가).
- 이번 방식 : 오픈 LLM과 텍스트 카탈로그로 구어체 텍스트를 만들고, TTS로 153시간 합성 음성을 생성해 실제 음성 92시간과 결합함.
→ 실제 의사 녹음 학습 데이터가 전혀 없는 상태에서도 14 GPU 시간 튜닝으로 전문 모델을 넘어서는 정확도를 얻게 됨.

# 숫자로 보면
| 항목 | 이전 / 기준 | 이번 (Nemotron 3.5) | 출처 |
|---|---|---|---|
| HF Open ASR 영어 WER | 4.94% (Qwen3-ASR-1.7B) | 4.71% (9개 셋 평균 1위) | Hugging Face 모델 카드 |
| HF Open ASR 다국어 WER | 6.49% (Qwen3-ASR-1.7B) | 4.62% (7개 언어 평균 1위) | Hugging Face 모델 카드 |
| HF Open ASR 장문 WER | 13.37% (Parakeet-TDT-0.6B-v3) | 10.98% (1위) | Hugging Face 모델 카드 |
| Artificial Analysis AA-WER | 2.80% (24B 활성 파라미터 모델) | 2.80% (4B 활성 파라미터, 1위 타이) | Artificial Analysis 리더보드 |
| AA-AgentTalk 보이스 에이전트 WER | 2.3% (차순위 오픈 모델) | 1.8% | Artificial Analysis 리더보드 |
| David AI 21개 언어 화자 분리 에러율(DER) | 18.38% (Nemotron 3 Diarization) | 18.26% (14개 시스템 중 전체 1위) | David AI 리더보드 |
| VoiceArena cpWER (다중 화자 중복 발화) | 34.2% (Parakeet + Nemotron 3) | 32.4% (14개 시스템 중 1위) | VoiceArena 리더보드 |
| VoiceArena 단어 누락률 (Deletions) | 약 31% (비교 시스템 중앙값) | 8.32% | VoiceArena 리더보드 |
| Eka Care 의료 ASR 전체 WER (인도 악센트) | 30.8% (기본 프롬프트) | 11.8% (합성 음성 파인튜닝 후, 62% 감소) | NVIDIA NeMo Speech 가이드 |
| Eka Care 미학습 화자 WER | 22.44% (프롬프트 베이스라인) | 12.17% (의료 전문 오픈 모델 13.79% 능가) | NVIDIA NeMo Speech 가이드 |
| RTX PRO 6000 전사 처리량 (NVFP4 + DFlash2) | vLLM 초기 통합본 (약 2배 느림) | 100시간 오디오를 3분 미만으로 처리 (2,238초/초) | Hugging Face 모델 카드 |

# 주의할 점 / 한계
- 실시간 스트리밍 미지원 : 내부 오디오 청킹 구조를 갖췄으나 오프라인 녹음 처리용으로 설계되어 실시간 라이브 스트리밍 ASR로는 바로 쓸 수 없음.
- 작업별 언어 편차 : 전사는 40개 언어, 번역은 31개 언어지만, 화자 분리는 13개 언어로 제한되며 오디오 질문 답변과 추론 모드는 영어로만 학습됨.
- 오픈소스 서빙 속도 차이 : 100시간 오디오를 3분 미만으로 끝내는 처리량은 미공개 최적화 NIM 기준이며, 공개된 초기 vLLM 코드는 약 2배 느림.
- 도메인 튜닝 시 일반 성능 변화 : 의료 튜닝 시 미학습 화자 WER은 45.8% 상대적으로 줄었으나, 일반 영어(LibriSpeech test-clean) WER은 1.54%에서 1.69%로 소폭 상승함.

# 정리
- 음향 인코더와 화자 분리 인코더를 Mamba-Transformer 하이브리드 MoE 언어 백본에 직결해, 프롬프트 지시와 화자 인식을 한 번에 끝내는 오픈 음성 모델이다.
- 463,062시간 규모의 Granary v2 파이프라인과 합성 데이터 기반 도메인 튜닝 기법은 음성 AI를 자체 도메인에 이식하려는 엔지니어에게 실용적인 레퍼런스가 됨.

# 참고
- [NVIDIA Nemotron 3.5 Transcribe and Granary v2: Intelligent Multilingual Transcription You Can Prompt and Adapt](https://huggingface.co/blog/nvidia/nemotron-transcribe-granary) — Hugging Face Blog
- [nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) — Hugging Face Model Card
- [nvidia/Granary-v2](https://huggingface.co/datasets/nvidia/Granary-v2) — Hugging Face Datasets
- [Medical ASR from a test-only benchmark, with synthetic data](https://github.com/NVIDIA-NeMo/Speech/blob/main/examples/speechlm2/finetuning/docs/medical-asr-synthetic-data.md) — NVIDIA-NeMo/Speech GitHub
- [Nemotron 3.5 Transcribe Technical Report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3.5-Transcribe-Technical-Report.pdf) — NVIDIA Research
- [Granary v2 Technical Report](https://research.nvidia.com/labs/nemotron/files/granary-v2.pdf) — NVIDIA Research
- [NeMo Curator Granary v2 Pipeline](https://github.com/NVIDIA-NeMo/Curator/tree/main/tutorials/audio/granary_v2) — NVIDIA-NeMo/Curator GitHub
