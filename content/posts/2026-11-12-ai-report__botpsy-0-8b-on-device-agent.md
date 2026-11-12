---
weight: 187
title: "BotPsy — 0.8B 파라미터와 4단계 후학습으로 2B 모델을 앞서는 온디바이스 에이전트"
date: 2026-11-12T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 0.8B 파라미터와 0.81GB GGUF 가중치만으로 자기보다 2.5배 큰 2B 모델을 도구 호출에서 이기는 온디바이스 에이전트 언어 모델이 공개됨 !

# 개요
- 무엇 : Tether AI Research가 2026.11.11 공개한 0.8B 규모의 온디바이스 개인 비서용 에이전트 언어 모델
- 한 줄 정의 : BotPsy는 Qwen3.5-0.8B를 4단계 후학습으로 정제해 기기 내부에서 함수 호출과 멀티턴 에이전트 작업을 처리하는 초소형 오픈 웨이트 언어 모델이다.
- 원문 : [BotPsy: On-Device Personal Assistant with a Sub-Billion-Parameter Agentic Language Model](https://huggingface.co/blog/qvac/botpsy)

# 그래서 도대체 뭔데 ?
- 클라우드 프런티어 LLM은 호출 비용이 비싸고 외부 제공자의 정책 변경이나 데이터 유출 위험이 따르지만, 일정 등록 · 기기 제어 · 메일 발송 같은 일상적인 저 · 중난이도 작업은 굳이 거대 모델을 쓸 필요가 없음.
- Tether AI Research는 Qwen3.5-0.8B(하이브리드 Gated DeltaNet + Gated Attention 구조)를 기반으로 도구 호출(function calling)과 멀티턴 상태 추적에 특화한 0.8B 모델인 BotPsy-0.8B를 개발함.
- 3개의 4B 전문 교사 모델을 활용한 토큰별 역방향 KL 발산 기반 온폴리시 증류(MOPD)와 세분화된 부분 보상 강화학습(RL)을 결합해, 에이전트 6대 벤치마크 평균 점수를 기반 모델 대비 24.7점에서 45.0점으로 약 2배 끌어올렸고 2.5배 크기인 Qwen3.5-2B-Think(38.8점)까지 앞지름.
- Apache 2.0 라이선스로 BF16 safetensors와 GGUF 3종(BF16 1.52GB, Q8_0 0.81GB, Q4_K_M imatrix 0.53GB)을 함께 배포해 llama.cpp와 QVAC SDK에서 바로 구동할 수 있음.
	- 💡 온폴리시 증류(On-Policy Distillation, OPD) : 고정된 정답 궤적만 모방하는 대신 학생 모델이 직접 응답을 생성하고, 교사 모델이 매 토큰마다 피드백을 주는 학습 기법.
	- 💡 토큰별 역방향 KL 발산(Per-token Reverse KL Divergence) : 학생 모델이 생성한 각 토큰의 확률 분포와 교사 모델의 토큰 분포 사이 차이를 계산해 증류 학습 신호로 쓰는 지표.
	- 💡 중요도 행렬(Importance Matrix, imatrix) : 4비트 양자화(Q4_K_M) 시 보류 텍스트 기준 BF16 원본 모델과의 KL 발산을 낮추는 보정 기법 (일반 Q4_K_M 0.048 → imatrix 적용 시 0.036).

# 어떻게 동작하나 ?
1. 1단계 — 도구 사용 궤적 모방 (전체 파라미터 SFT)
	- 시뮬레이션 환경에서 수집한 멀티턴 대화, 단일 · 병렬 · 다단계 함수 호출, 그리고 맞는 도구가 없을 때 호출을 거부하는 사례를 모아 전체 파라미터 지도 미세조정(SFT)을 수행함.
	- 이 단계를 거치면 도구 사용 점수는 크게 오르지만, 부작용으로 일반 지식과 지시 이행 능력이 기반 모델(Qwen3.5-0.8B) 아래로 떨어지는 현상이 발생함.
	→ 에이전트 동작의 기본 형식과 거부 패턴을 먼저 익히되, 무너진 기초 체력을 다음 단계에서 복구할 발판을 마련함.

2. 2단계 — 3인 전문 교사 기반 온폴리시 증류 (MOPD)
	- 학생보다 5배 큰 Qwen3.5-4B 모델 3개를 각각 도구 사용, 일반 추론, 지시 이행 한 가지 기술에만 특화되도록 강화학습(RL)으로 먼저 훈련해 전문 교사 집단을 구축함.
	- 학습 중 각 프롬프트를 성격에 맞는 전문 교사 1개에 라우팅하고, 학생(0.8B)이 직접 생성한 응답의 매 토큰에 대해 토큰별 역방향 KL 발산을 계산해 피드백을 줌.
	- 도구 사용 · 지식 · 지시 이행 데이터를 섞어 학습해, SFT에서 하락했던 일반 지식과 지시 이행 점수를 기반 모델 이상으로 되살리고 도구 호출 성능도 추가로 높임.
	→ 분야별 4B 전문 교사의 토큰 분포를 학습 신호로 삼아 SFT의 일반 역량 손실을 복구하고 도구 사용 점수를 함께 끌어올림.

3. 3단계 — 세분화된 부분 보상 1차 강화학습 (RL Round 1)
	- 도구 호출과 지시 이행 · STEM 객관식 문제를 대상으로, DAPO 알고리즘을 적용해 규칙과 검증기(verifier)로 계산된 보상만으로 학습함.
	- 도구 호출 보상을 줄 때 Tool-N1처럼 추론 과정과 도구 호출 형식을 먼저 검사하되, 맞고 틀림만 따지는 이진 보상 대신 ToolRL 방식을 도입해 예측한 함수 이름 · 인자 이름 · 인자 값을 정답과 각각 대조하여 세분화된 부분 점수를 부여함.
	→ 이진 정답 보상 대신 함수 · 인자 단위의 부분 점수를 피드백으로 받아 도구 사용 · 지시 이행 · 지식 점수를 추가로 높임.

4. 4단계 — 일반 도메인 확장 2차 강화학습 (RL Round 2)
	- 학습 데이터의 중심을 수학 · 코드 · 객관식 지식 · 지시 이행 · 구조화 출력과 시뮬레이션 업무 환경의 다단계 도구 사용으로 넓힘.
	- 2차 RL 데이터에는 멀티턴 대화가 전혀 들어가지 않았음에도 멀티턴 함수 호출 점수가 한 번 더 상승함.
	→ 4단계를 모두 마친 뒤 추론 루프에 빠지는 비율이 22.9%에서 1.4%로 줄고, 정답 도달에 필요한 추론 토큰 수도 1.4 ~ 3.1배 감소함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 1B 미만의 초소형 모델을 도구 호출용 SFT로 학습시키면 도구 사용 점수는 오르더라도 일반 지식과 지시 이행력이 기반 모델 아래로 떨어지고, 추론 모드(`thinking`)에서 같은 말을 반복하는 루프에 빠져 32,768 토큰 한도를 채우는 비율이 높았음.
- 이번 방식 : SFT 직후 3개의 4B 전문 교사를 라우팅하는 온폴리시 증류(MOPD)로 손실된 지식과 지시 이행력을 복구하고, 2단계의 검증기 기반 RL(부분 점수 보상 + 일반 도메인 확장)을 얹어 추론 길이를 압축함.
→ 그 결과 0.8B 크기이면서 1.2B 이하 비교 모델 전부를 6개 에이전트 벤치마크에서 모두 이기고, 자기보다 2.5배 큰 Qwen3.5-2B-Think까지 6개 중 5개 벤치마크에서 넘어섬.

# 숫자로 보면

| 항목 | 이전 (비교 모델) | 이번 (BotPsy-0.8B) | 출처 |
|---|---|---|---|
| 에이전트 6종 평균 (BFCL · ACEBench 등) | 24.7 (Qwen3.5-0.8B) / 38.8 (Qwen3.5-2B) | 45.0 (BF16 vLLM 기준) | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| BFCL v4 전체 / 멀티턴 / 환각 억제 | 23.4 / 7.5 / - (Qwen3.5-0.8B) | 44.0 / 46.1 / 86.1 | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| ACEBench 전체 / 특수 케이스(거부 · 오류) | 30.1 / 13.7 (Qwen3.5-0.8B) | 58.7 / 51.3 | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| τ-bench 평균 / τ²-telecom 멀티턴 | 23.2 / - (0.8B) · 46.5 / 69.3 (2B) | 51.5 / 82.5 | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| ToolSandbox (8개 설정 평균 유사도) | 30.5 (0.8B) / 45.7 (LFM2.5-1.2B) | 64.6 | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| 지시 이행 (IFEval / IFBench) | 59.7 / 22.0 (0.8B) · 80.0 / 40.9 (2B) | 90.8 / 55.9 | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| 일반 지식 (GPQA Diamond / MMLU-Pro) | 33.2 / 41.6 (0.8B) · 59.9 / 65.5 (2B) | 38.1 / 48.9 | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| 정답당 추론 토큰 (GPQA / MMLU-Pro) | 11,563 / 5,105 (Qwen3.5-0.8B) | 3,690 (3.1배 감소) / 1,912 (2.7배 감소) | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| IFBench 반복 루프 / 32k 토큰 한도 도달 | 22.9% / 28.3% (Qwen3.5-0.8B) | 1.4% / 0.2% | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| 레드티밍 유해 응답 / 프롬프트 인젝션 | 36% / 46% (Qwen3.5-0.8B) | 21% / 31% | [Tether Blog](https://huggingface.co/blog/qvac/botpsy) |
| GGUF 10종 평균 및 크기 (llama.cpp) | BF16 GGUF 50.4 (1.52GB) | Q8_0 50.7 (0.81GB) / Q4_K_M 48.9 (0.53GB) | [GGUF Card](https://huggingface.co/qvac/BotPsy-0.8B-GGUFs) |

- 비교 조건 : 모든 모델은 추론 모드(`enable_thinking=True`)와 동일한 평가 하네스에서 측정됨(외부 API 연동 벤치마크는 2026.11.03 실행). GGUF 비교는 2026.11.06 ~ 2026.11.07 기간 동안 NVIDIA H100 GPU 위에서 `llama-server`(CUDA 빌드 b12169)로 ToolSandbox를 제외한 10개 벤치마크를 측정한 값임.

# 주의할 점 / 한계
- 다단계 심층 검색과 고난도 금융 과제의 한계 : 단일 도구 호출은 앱 그룹 평균 75점을 기록하지만, 복합 다단계 과제는 평균 39.5점으로 낮아짐. 특히 개방형 심층 검색인 BrowseComp-Plus(4.5점)나 다단계 정보 검색 시나리오(15점), 그리고 τ³-banking(4.1점, 비교 모델 전부 5점 미만) 같은 고난도 영역에서는 절대 점수가 낮음 (원문에서도 저 · 중난이도 작업에 적합하며 금전 · 의료 · 민감 정보 등 고위험 의사결정용이 아니라고 명시함).
- 파라미터 규모에 비례하는 암기 지식과 누적 지시 하락 : 일반 지식(GPQA 38.1 vs 2B 모델 59.9)은 여전히 모델 크기에 좌우되므로, 사실을 직접 답하게 하기보다 검색 도구를 호출하게 설계해야 함. 또한 8개 언어 3턴 지시 이행을 보는 Multi-IF에서 1턴 점수는 84.3점으로 가장 높지만, 3턴째에는 51.0점으로 떨어져 조건이 누적될수록 성능 감소폭이 2B 모델(56.5점)보다 큼.
- 언어 편차와 실행 주의사항 : 영어 및 주요 유럽어 · 중국어에서는 Multi-IF 72 ~ 80점을 내지만 러시아어(57.6점)와 힌디어(24.5점) 같은 저자원 언어에서는 점수가 급감함. 기본 채팅 템플릿이 비추론 모드로 설정되어 있어 실행 시 반드시 `enable_thinking=True`와 최소 2,048 토큰 이상의 생성 예산을 줘야 제 성능이 나오며, 4비트 양자화(Q4_K_M) 시 지식 벤치마크에서 3.5 ~ 3.9점 손실이 발생하므로 메모리가 허용하면 0.81GB 크기의 Q8_0 포맷이 권장됨.
- 아직 확인 안 된 것 : 실제 스마트폰 · 노트북 NPU 및 모바일 CPU 위에서의 초당 토큰 생성 속도(tok/s)와 전력 소모량 실측치, 그리고 학습 코드 및 자체 합성 데이터셋 원본은 원문에 없음.

# 정리
- SFT로 도구 호출 형식을 입힌 뒤 3개의 4B 전문 교사 온폴리시 증류(MOPD)와 2단계 검증기 RL을 결합해, 0.8B 모델이 겪는 일반 역량 하락과 반복 추론 루프 문제를 동시에 줄인 학습 레시피가 핵심임.
- 0.81GB짜리 Q8_0 GGUF 파일 하나로 BF16 원본과 대등한 도구 호출 · 멀티턴 대응력을 내므로, 클라우드 API 없이 로컬 기기에서 캘린더 · 시스템 설정 · 커머스 등 저 · 중난이도 개인 비서 에이전트를 연구 · 구현할 때 활용할 수 있음.

# 참고
- [BotPsy: On-Device Personal Assistant with a Sub-Billion-Parameter Agentic Language Model](https://huggingface.co/blog/qvac/botpsy) — Hugging Face Blog (Tether AI Research)
- [qvac/BotPsy-0.8B Model Card](https://huggingface.co/qvac/BotPsy-0.8B) — Hugging Face
- [qvac/BotPsy-0.8B-GGUFs Model Card](https://huggingface.co/qvac/BotPsy-0.8B-GGUFs) — Hugging Face
