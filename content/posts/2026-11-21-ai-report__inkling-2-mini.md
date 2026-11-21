---
weight: 204
title: "Inkling 2 Mini — 중간 12개 레이어를 3번 돌려 20GB로 로컬 추론을 끌어올린다"
date: 2026-11-21T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 물리 24층 중 중간 12층을 3번 돌려 48층처럼 추론하는 26.4B 오픈 멀티모달 MoE — NVFP4 · MXFP8 약 20GB로 32GB+ 로컬에서 바로 돌릴 수 있음 !

# 개요
- 무엇 : Thinking Machines Lab이 2026.11.20 Apache 2.0으로 공개한 멀티모달 루프드 트랜스포머 Inkling 2 Mini (가변 루프 `TML-d24-varloop-research` 동시 공개).
- 한 줄 정의 : Inkling 2 Mini는 물리 24층(약 20GB) 중 중간 12층을 3회 반복해 48층 깊이로 추론하는 오픈 MoE다.
- 원문 : [Welcome Inkling 2 Mini, Cutting-edge Performance for your Local Setup](https://huggingface.co/blog/inkling2mini)

# 그래서 도대체 뭔데 ?
- 표준 비루프 트랜스포머는 고정 층만 통과해 추론력을 높이려면 파라미터나 CoT를 늘려야 했음.
- 중간 12층을 3번 돌려 직렬 깊이를 키우고, 사전학습 ~ RL을 NVFP4 · MXFP8로 직접 학습해 양자화 손실 없이 약 20GB로 배포함.
	- 💡 루프드 트랜스포머 : 추가 가중치 없이 일부 레이어를 토큰마다 반복해 직렬 깊이를 늘리는 구조.
	- 💡 크로스-패스 메시지 : 직전 패스 출력을 학습 게이트로 다음 패스에 섞어 계산을 정제하는 경로.

# 어떻게 동작하나 ?
1. 24 물리 레이어 → 48회 논리 실행
	- 6레이어 4블록 중 앞 6개 1회 · 중간 12개 3회 · 뒤 6개 1회 실행(방문마다 독립 KV 캐시 · short-convolution 유지).
	- 블록당 슬라이딩 윈도우(최대 1,024토큰) 5개 + 풀 어텐션 1개 하이브리드(쿼리 24 · KV 8헤드), 텍스트 디코더 폭 2,304 · 1M 컨텍스트 · 이미지 입력 지원.
	→ 기본 활성 3.4B에 추가 패스당 약 1.0B 더해 3패스 유효 활성 5.4B 연산 수행.
2. Attention Residuals와 메시지 게이트
	- 매 루프는 프렐류드(앞 6개)에서 시작, 2 · 3패스는 직전 잔차 블록 2개 출력을 랭크 64 게이트 4개로 쿼리 · 키 · 값 · MoE에 섞음.
	- 초반엔 메시지를 막아 비루프처럼 시작해 점차 비중을 높임.
	→ 패스마다 계산을 다듬어 CoT 백트래킹 감소.
3. 프루닝 · 네이티브 저비트 · 런타임
	- 미드트레이닝에서 전문가를 384 → 128개(중간 폭 1,152 · 토큰당 8개)로 줄인 뒤 1T 토큰 증류 복구(healing) · SFT · 2.2T 토큰(2,000스텝) RL 수행.
	- 앞 20층 전문가는 NVFP4 · 뒤 4층은 MXFP8 · 나머지는 BF16으로 학습해 그대로 배포. 32GB+ Mac(`mlx-lm` 네이티브 · Ollama) · DGX Spark · 32GB+ GPU, `llama.cpp` GGUF(`IQ4_NL` · `Q8_0`), SGLang(Day 0 · DSpark 3층 투기적 디코딩) 지원.
	- 1 ~ 5패스로 학습해 추론 시 패스 수를 바꾸는 연구용 `TML-d24-varloop-research` 공개.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 비루프 모델은 고정 층만 통과해 크기나 CoT를 키워야 했고 로컬 배포 시 양자화 손실이 생길 수 있었음.
- 이번 방식 : 스케일링 래더(비프루닝)에서 비루프는 학습 연산이 7.5% 적었지만 512K 토큰 에이전트 트레이스 손실을 맞추려면 추론 연산이 140% 더 들었음. 중간(7 ~ 18층) 루프가 뒤(13 ~ 24층)보다 28개 중 27개 평가에서 앞섰고 2,000스텝 비루프 대비 연산 절감 배수도 컸음(1.51 ~ 1.91배 vs 1.24 ~ 1.36배).
→ 약 20GB로 27B ~ 31B급 비교 모델 수준 에이전트 · 코딩 성능을 내고 루프 반복으로 추론 토큰도 줄임.

# 숫자로 보면
| 항목 | 이전 (비교군) | 이번 (Inkling 2 Mini / 가변 루프) | 출처 |
|---|---|---|---|
| 파라미터 (유효 활성 / 전체) | Qwen3.8-27B 27.0B / 27.0B | 5.4B (3.4B 활성, 3패스) / 26.4B (MoE) | TML 블로그 · 모델 카드 |
| AA Index v5.0 (종합) | Qwen3.8-27B 20.1 / Nemotron 3.5 Super VL 13.6 / Gemma 4 31B 4.4 | 20.1 (비교군 동률 1위) | TML 블로그 |
| DeepSWE v1.1 (`mini-swe-agent v2.4.6`) | Qwen3.8-27B 42.2% / Nemotron 3.5 Super VL 24.7% | 48.2% (100B 미만 오픈 1위) | TML 블로그 |
| SWEBench Pro v2 Hard (`mini-swe-agent v2.4.6`) | Qwen3.8-27B 73.8% / Muse Glimmer 44.3% | 77.9% | TML 블로그 |
| SWEBench Verified (`bash only`) | Qwen3.8-27B 77.8% / Muse Glimmer 76.0% | 79.2% | TML 블로그 |
| BrowseComp (Inkling은 compaction 적용) | Nemotron 3.5 Super VL 78.9% / Qwen3.8-27B 61.6% | 79.0% | TML 블로그 |
| LongBench v2 / MRCR v2 8-needle (256K ~ 512K) | Nemotron 3.5 Super VL 62.1% / 5.7%, Qwen3.8-27B 52.3% / 38.0% | 66.9% / 46.4% | TML 블로그 |
| Intelligence per Watt (DGX Spark, Stanford) | Qwen3.6-35B-A3B 0.430 (NVFP4) / Gemma-4-26B-A4B 0.159 (NVFP4) / Qwen3.5-27B 0.036 (INT4) | 0.703 (MXFP8, low effort) | TML 블로그 |
| CoT 길이 · 불확실 표현 (GPQA Diamond 공통 정답, 가변 루프) | 1패스 3,703토큰 (9.7회) | 3패스 1,731토큰 (3.9회) / 5패스 1,661토큰 (3.6회) | TML 블로그 |
| No-CoT 시간 지평 (Think Fast 50%, 가변 루프) | 1패스 16초 | 3패스 37초 | TML 블로그 |
| AA-Omniscience v1.1 점수 / 비환각률 | Nemotron 3.5 Super VL -2.9 / 69.5%, Qwen3.8-27B -6.4 / 71.4% | -8.6 / 63.4% | TML 블로그 |

- 4개 비교군 대비 48개 중 32개 1위. 가변 루프 1 → 5패스에서 CoT가 절반 이하로 줄어도 영어 사전 단어 비율(94.6% → 94.4%) 유지.
- CoT-Control-QA(750 ~ 1,250토큰) 제어율 0.1% 이하(Qwen3.8-27B 1.3%), LinuxArena(184쌍 · 약한 모니터)도 루프 수에 따른 은밀 공격 증가 없음.

# 주의할 점 / 한계
- **지식 한계** : 루프는 사실 저장량을 못 늘려 AA-Omniscience v1.1(-8.6)에서 Qwen3.8-27B(-6.4) · Nemotron(-2.9)에 뒤지고, 가변 루프(1 → 5패스) SimpleQA Verified(6.3% → 6.7%) · WorldVQA(11.3% → 13.5%)도 정체.
- **다중 턴 · 비영어 · 신뢰성** : MultiChallenge(50.0%)에서 Qwen3.8-27B에 뒤지고 중국어 문장 잘림 · 언어 혼용 확인됨. 반복 루프 · 무단 파일 삭제 가능성으로 턴 제한 · 샌드박스 필요.
- **연산 · 런타임 · 배포** : 3회 루프로 기본 활성(3.4B)보다 연산이 크고(유효 5.4B) `reasoning_effort` 0.0에도 추론이 완전히 꺼지지 않음. 로컬 지원은 초기라 속도 편차가 크며 SGLang은 `SM103` 필요 · 가변 루프는 프로덕션 비권장.
- **수치 조건** : 모델별 하네스(BrowseComp compaction · Terminal Bench v2.1 `pi v0.83.0`)와 Intelligence per Watt(0.703) 정밀도 조건이 다름.
- **아직 확인 안 된 것** : 사전학습 총 토큰 수 · 로컬 실측 `tok/s` · SGLang DSpark 정확 수치(그래프만)는 원문에 없음.

# 정리
- 중간 12층 3회 루프 · 네이티브 NVFP4 · MXFP8로 약 20GB에 27B ~ 31B급 비교 모델 수준 에이전트 · 코딩 성능을 담은 Apache 2.0 모델임.
- 32GB+ 로컬에서 오프라인 코딩 에이전트를 돌릴 개발자, 가변 루프 · CoT 모니터링 연구자에게 써먹을 만함.

# 참고
- [Welcome Inkling 2 Mini, Cutting-edge Performance for your Local Setup](https://huggingface.co/blog/inkling2mini) — Hugging Face Blog
- [Introducing Inkling 2 Mini](https://thinkingmachines.ai/news/inkling-2-mini/) — Thinking Machines Lab
- [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) — Hugging Face Model Card
- [thinkingmachines/TML-d24-varloop-research](https://huggingface.co/thinkingmachines/TML-d24-varloop-research) — Hugging Face Model Card
