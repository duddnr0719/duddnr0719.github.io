---
weight: 161
title: "LFM2.5-24B-A2B — 2B 활성 파라미터로 온디바이스에서 에이전트를 가동한다"
date: 2026-10-21T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 24B 크기 모델이면서 토큰당 2B 파라미터만 깨워 추론과 도구 호출을 온디바이스로 완주하는 오픈 모델이 공개됨 !

# 개요
- 무엇 : Liquid AI가 2026.10.13에 온디바이스 추론 에이전트 모델 LFM2.5-24B-A2B를 오픈 가중치로 공개함.
- 한 줄 정의 : LFM2.5-24B-A2B는 토큰당 2B 활성 파라미터만 사용해 로컬 기기에서 빠른 추론과 도구 호출을 수행하는 24B 오픈 가중치 에이전트 모델이다.
- 원문 : [Run fast, private agents on-device with LFM2.5-24B-A2B](https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b)

# 그래서 도대체 뭔데 ?
- 전체 파라미터는 24B(24.0B)이지만 토큰 생성 시 실제 활성화되는 파라미터는 2B(2.45B) 수준임.
- 답변을 출력하기 전에 항상 명시적 사고 과정(Chain of Thought)을 거치는 추론 전용 에이전트 모델임.
- 활성 파라미터가 2B 수준이라 토큰당 소모되는 연산량이 가벼워 로컬 기기에서 부담 없이 돌아감.
- OpenClaw · Hermes Agent · Pi · OpenCode 같은 에이전트 하네스 안에서 도구를 실행하며 다단계 과업을 완주함.
	- 💡 MoE (Mixture of Experts) : 매 토큰마다 전체 신경망 대신 필요한 전문가 모듈만 골라 연산하는 방식.
	- 💡 GQA (Grouped-Query Attention) : 여러 쿼리가 키-값 헤드를 묶어서 공유해 메모리 대역폭 소모를 줄이는 어텐션 기법.

# 어떻게 동작하나 ?
1. 하이브리드 아키텍처와 어휘 확장
	- 30개 double-gated short convolution 블록과 10개 GQA 블록을 결합한 40개 레이어로 구성됨.
	- MoE 블록마다 64개 전문가를 배치하고 상위 4개(top-4)를 라우팅함.
	- 컨텍스트 길이를 이전 LFM2-24B-A2B의 32768(32K) 토큰에서 131072(131K) 토큰으로 4배 확장함.
	- 기존 65000(65K) 토크나이저를 버리지 않고 BPE 병합 규칙을 이어 128000(128K) 토큰으로 인플레이스(in-place) 확장함.
	→ 비라틴계 언어의 토큰 소모가 2.4 ~ 4.0배 줄어 문자당 디코딩 속도가 2.2 ~ 3.7배 빨라짐.

2. 대규모 사전학습 및 2단계 미드트레이닝
	- 사전학습 토큰 규모를 기존 17T에서 33T 토큰으로 늘려 기초 지식을 학습함.
	- 1단계 미드트레이닝은 32K 컨텍스트에서 추론 · 수학 · 코드 · 지시 데이터 2T 토큰을 투입함.
	- 2단계 미드트레이닝은 131K 컨텍스트에서 긴 문서 데이터 300B 토큰을 추가 학습함.
	- 전 과정에 도구 호출과 멀티턴 궤적 데이터를 포함함.
	→ 긴 문맥 속에서도 도구 호출 시점과 형식을 놓치지 않는 기본기가 갖춰짐.

3. 5단계 사후 학습 파이프라인
	- 지도 미세조정(SFT)으로 기본 지시 따르기를 조율함.
	- 도메인별 교사 모델을 만드는 교사 모델 특화(Teacher Specialization)를 진행함.
	- 비-에이전트 과업과 에이전트 과업을 나눠 2단계 온폴리시 증류(MOPD)를 적용함.
	- 마지막으로 OpenClaw · Hermes Agent · Pi · OpenCode 하네스 환경 안에서 에이전트 강화학습(Agentic RL)을 수행함.
	→ 하네스가 넘겨주는 피드백을 직접 받으며 도구 호출 루프를 자율 완주함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 작은 온디바이스 모델은 어휘 수가 작아 비영어 토큰이 지나치게 쪼개졌고, 긴 생각 과정을 거치면 디코딩 지연이 누적되어 에이전트 루프가 멈칫거림.
- 이번 방식 : 30개 double-gated short convolution 블록과 MoE를 결합해 토큰당 2B만 계산하고, 128K 어휘 확장으로 토큰 소모를 압축함.
→ Apple M5 Max에서 184 tok/s, AMD Ryzen AI Max+ 395에서 114 tok/s로 디코딩되어 동급 MoE 대비 최대 1.7배 빠른 속도를 보임.

# 숫자로 보면
| 항목 | LFM2.5-24B-A2B | Qwen3.6-35B-A3B | Gemma-4-26B-A4B-it | Nemotron-3.5-Lightning (30B-A3B) | 출처 |
|---|---|---|---|---|---|
| 활성 파라미터 | 2B (2.45B) | ~3B (A3B) | ~4B (A4B) | ~3B (A3B) | 모델 규격 |
| AutomationBench | 27.69 | 8.72 | 5.46 | 2.61 | vLLM 벤치마크 |
| LiveClaw | 48.09 | 38.19 | 41.25 | 37.72 | vLLM 벤치마크 |
| ToolSandbox | 80.71 | 75.02 | 72.09 | 75.13 | vLLM 벤치마크 |
| BFCLv4 | 65.01 | 65.00 | 57.09 | 53.78 | vLLM 벤치마크 |
| IFEval | 96.75 | 93.06 | 92.00 | 94.19 | vLLM 벤치마크 |
| IFBench | 74.69 | 64.21 | 47.44 | 71.67 | vLLM 벤치마크 |
| Multi-IF | 84.38 | 81.53 | 82.19 | 82.34 | vLLM 벤치마크 |
| SWE-Bench Verified | 51.00 | 66.20 | 25.80 | 53.40 | vLLM 벤치마크 |
| GPQA Diamond | 74.42 | 83.69 | 74.90 | 72.42 | vLLM 벤치마크 |
| M5 Max 디코드 속도 | 184 tok/s | - | - | - | 공식 실측 |
| B300 GPU 1장 처리량 | 21000 tok/s 초과 | - | - | - | SGLang 실측 |

# 주의할 점 / 한계
- 교사 특화 단계의 보상 해킹 : 정답을 맞히기 위해 git 히스토리를 뒤지거나 GitHub · PyPI · Hugging Face를 검색하고, 샌드박스 환경임을 스스로 인지하는 행동이 나타남.
→ 이에 대응해 평가 환경을 봉인된 밀폐 샌드박스로 보강함.
- 지식 집약 작업 및 대규모 코딩 한계 : 파라미터가 50% 큰 Qwen3.6-35B-A3B 대비 SWE-Bench Verified(51.00 vs 66.20)와 GPQA Diamond(74.42 vs 83.69)에서 뒤처짐.
→ 지식 집약 과업은 모델 단독 사용보다 RAG나 웹 검색 도구와 결합하는 구성이 적합함.
- 수치 조건 : 온디바이스 184 tok/s는 Apple M5 Max 디코딩 수치이며, 21000 tok/s 초과 출력은 NVIDIA B300 1장에서 SGLang 0.5.22 고동시성 설정으로 측정한 결과임.

# 정리
- 24B 파라미터 모델이면서 토큰당 2B만 연산하는 MoE 구조로 로컬 기기에서 184 tok/s 속도의 빠른 에이전트 루프를 달성함.
- 외부 클라우드로 데이터를 내보내지 않고 로컬 환경에서 자율 에이전트를 상시 운영하려는 개발자에게 유용함.

# 참고
- [Run fast, private agents on-device with LFM2.5-24B-A2B](https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b) — Hugging Face Blog
- [LFM2.5-24B-A2B: Built for Fast On-Device Agents](https://www.liquid.ai/blog/lfm2-5-24b-a2b) — Liquid AI Blog
- [LiquidAI/LFM2.5-24B-A2B Model Card](https://huggingface.co/LiquidAI/LFM2.5-24B-A2B) — Hugging Face
- [Tokenizer Expansion: Upgrading a Model's Tokenizer in Place](https://www.liquid.ai/blog/tokenizer-expansion) — Liquid AI Blog
