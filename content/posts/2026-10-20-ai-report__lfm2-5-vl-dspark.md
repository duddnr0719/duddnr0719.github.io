---
weight: 160
title: "LFM2.5-VL-DSpark — 280M 드래프터로 VLM 디코딩 속도를 3배 끌어올린다"
date: 2026-10-20T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 3.1B 비전-언어 모델에 279.5M 드래프터를 붙여 출력 품질 저하 없이 디코딩 속도를 최대 3.13배 끌어올리는 오픈 가속 구현체다 !

# 개요
- 무엇 : Liquid AI가 2026.09.24에 LFM2.5-VL-3B 모델을 위한 투기적 디코딩 드래프트 모델 LFM2.5-VL-3B-DSpark를 공개함.
- 한 줄 정의 : LFM2.5-VL-3B-DSpark는 3.1B 파라미터 VLM의 추론 지연을 줄이기 위해 279.5M 크기의 경량 모델로 토큰을 미리 제안하고 검증받는 오픈 가속 드래프터다.
- 원문 : [Accelerating vision-language models with LFM2.5-VL-DSpark](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark)

# 그래서 도대체 뭔데 ?
- 3.1B 비전-언어 모델(VLM)에 279.5M(약 280M) 파라미터 드래프터를 결합해 파라미터 수는 8.9%만 늘리면서 메모리 증가는 최소화하고 추론 속도를 높이는 기술임.
- 그리디 디코딩 환경에서 타깃 모델이 제안된 모든 토큰을 직접 검증하므로 원본 타깃 모델과 완전히 동일한 출력을 보장함.
- SGLang, llama.cpp, MLX-VLM에 당일 지원 코드가 반영되어 클라우드 H100 GPU부터 Apple silicon 기기까지 바로 실행 가능함.
	- 💡 투기적 디코딩(Speculative Decoding) : 작은 보조 모델이 후보 토큰 여러 개를 먼저 제안하고 본 모델이 한 번의 연산으로 병렬 검증하여 디코딩 시간을 줄이는 기법
	- 💡 드래프터(Drafter) : 본 모델의 중간 은닉 상태를 받아 미래 토큰 블록을 미리 예측하는 가벼운 보조 모델

# 어떻게 동작하나 ?
1. 멀티모달 입력 투영 및 공유 표현 구축
	- 이미지는 SigLIP2 비전 인코더를 거쳐 512x512 패치 단위로 처리되고 텍스트 토큰과 함께 모델에 들어감
	- 고정 계층(tapped layers) 앞단에서 이미지 패치와 텍스트를 단일 공유 벡터 공간으로 투영함
	→ 입력 모달리티에 관계없이 드래프터가 동일한 차원의 은닉 상태 벡터만 받아 처리하게 됨

2. 4계층 어텐션 백본과 마르코프 헤드의 토큰 블록 생성
	- 드래프터는 4개 어텐션 계층과 rank 256 마르코프 헤드를 기반으로 설계됨
	- 본 모델의 은닉 상태를 조건 삼아 한 번에 8개 또는 9개 후보 토큰 블록을 연속해서 찍어냄
	→ 거대한 타깃 모델을 매 토큰마다 돌리지 않고 경량 드래프터 연산으로 미래 토큰들을 묶음 생성함

3. 타깃 모델의 병렬 검증과 토큰 확정
	- 타깃 모델인 LFM2.5-VL-3B가 제안된 토큰 블록을 단 한 번의 순전파 패스로 병렬 검증함
	- 본 모델 기준과 일치하는 토큰은 그대로 수락되고 불일치 시점부터 다시 정상 생성을 이어감
	→ 품질 손실 없이 검증 통과 수만큼 디코딩 단계의 지연 시간이 줄어듦

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : VLM 추론 시 수백 개 비전 패치 토큰이 포함된 시퀀스 전체를 대상으로 매 토큰마다 3.1B 타깃 모델 전체를 반복 실행(Autoregressive)해야 하므로 디코딩 지연이 큼.
- 이번 방식 : 이미지와 텍스트가 단일 공유 차원으로 맞춰진 뒤의 계층을 탭하여 은닉 상태를 추출함. 기존 텍스트 DSpark 추론 알고리즘을 구조 변경 없이 VLM에 그대로 투입함.
→ 별도 모달리티 분기 없이 단일 4계층 경량 디코더로 멀티모달 토큰 시퀀스를 가속하게 됨.

# 숫자로 보면
| 하드웨어 및 런타임 | 벤치마크 | 단독 추론 (기준) | DSpark 적용 (디코드 / 종단간) | 패스당 수락 토큰 | 출처 |
|---|---|---|---|---|---|
| Apple M5 Max (MLX-VLM) | COCO | 1.00x | 3.13x / 2.59x | 4.21 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| Apple M5 Max (MLX-VLM) | MMMU-Pro | 1.00x | 2.93x / 2.62x | 4.07 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| Apple M5 Max (MLX-VLM) | CharXiv | 1.00x | 2.94x / 1.71x | 4.34 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| Apple M5 Max (MLX-VLM) | TextVQA | 1.00x | 2.69x / 1.56x | 4.08 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| 1xH100 80GB (SGLang) | COCO | 1.00x | 2.66x / 2.27x | 4.57 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| 1xH100 80GB (SGLang) | MMMU-Pro | 1.00x | 2.43x / 1.97x | 4.11 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| 1xH100 80GB (SGLang) | CharXiv | 1.00x | 2.39x / 1.97x | 4.11 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| Apple M3 Ultra (llama.cpp) | COCO | 1.00x | 2.14x / 1.77x | 4.50 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| Apple M3 Ultra (llama.cpp) | MMMU-Pro | 1.00x | 2.03x / 1.74x | 4.19 | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |

드래프터 구성 요소 및 파라미터:
| 구성 요소 | 타깃 단독 | 드래프터 추가 | 증가율 | 출처 |
|---|---|---|---|---|
| 파라미터 수 | 3.1B | 3.1B + 279.5M | 8.9% | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| 디코더 스택 (4 layers) | - | 193.0M | - | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| 마르코프 헤드 | - | 65.5M | - | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| 은닉 투영 계층 | - | 21.0M | - | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |
| Norms + confidence head | - | 6.4k | - | [HF 블로그](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) |

# 주의할 점 / 한계
- 원문 한계 : 투기적 디코딩은 디코드 단계만 가속하며 비전 인코딩과 프리필 시간은 줄이지 못함 (암달의 법칙에 따라 프리필 비중이 크면 종단간 가속비는 1.56배 수준으로 제한됨)
- 엣지 디바이스 제약 : 데이터센터 GPU 대비 연산 능력이 낮아 전체 소요 시간 중 프리필 비중이 큼 (Apple M5의 GPU 신경망 가속기로 격차를 일부 좁힘)
- 수치 조건 : 배치 크기 1, temperature 0, MMSpec 벤치마크 기준 측정값
- 아직 확인 안 된 것 : 고동시성 다중 요청 환경에서의 벤치마크 결과는 원문에 없음

# 정리
- 3.1B 급 소형 VLM에 279.5M 경량 드래프터를 붙여 파라미터 수는 8.9%만 늘리면서 디코딩 속도를 최대 3.13배 끌어올림.
- SGLang, llama.cpp, MLX-VLM 지원 코드가 동시에 공개되어 Apple silicon 기기부터 단일 H100 GPU 환경까지 바로 쓸 수 있음.
- 엣지 디바이스나 단일 GPU에서 VLM 추론 지연을 줄이고 동일 출력을 유지해야 하는 환경에 적합함.

# 참고
- [Accelerating vision-language models with LFM2.5-VL-DSpark](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-dspark) — Hugging Face Blog
- [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](https://huggingface.co/papers/2607.05147) — arXiv 2607.05147
- [MMSpec: Benchmarking Speculative Decoding for Multimodal Large Language Models](https://huggingface.co/papers/2603.14989) — arXiv 2603.14989
- [LiquidAI/LFM2.5-VL-3B-DSpark](https://huggingface.co/LiquidAI/LFM2.5-VL-3B-DSpark) — Hugging Face Model Card
- [LiquidAI/LFM2.5-VL-3B](https://huggingface.co/LiquidAI/LFM2.5-VL-3B) — Hugging Face Model Card
