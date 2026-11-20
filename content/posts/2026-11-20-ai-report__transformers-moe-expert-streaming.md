---
weight: 203
title: "Transformers MoE 전문가 스트리밍 — 32GB 램에서 180B 모델을 SSD로 돌린다"
date: 2026-11-20T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 180B MoE 모델을 32GB 맥북에서 Transformers 기반으로 돌리며, 짧은 디코드 기준 전용 엔진 Strata와 약 6% 차이까지 격차를 좁힌 SSD 전문가 스트리밍 실험이다 !

# 개요
- 무엇 : Hugging Face의 Tarek Ziade가 2026.11.18 Transformers SSD 전문가 스트리밍(`experts_offload`, PR `#50717`은 2026.11.13 오픈)으로 `Qwen3.8-Flash-Next`(180B)를 32GB MacBook Pro M5에서 돌린 실험을 공개함.
- 한 줄 정의 : `experts_offload`는 메모리에 못 들어가는 MoE 전문가를 SSD에 두고, 제한된 캐시 풀로 필요한 것만 스트리밍해 기존 커널로 연산하는 기능이다.
- 원문 : [180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit with Transformers](https://huggingface.co/blog/moe-expert-streaming)

# 그래서 도대체 뭔데 ?
- MoE 가중치의 90% 이상은 전문가지만 토큰당 활성 비율은 작다 (`Qwen3.8-Flash-Next`는 레이어당 512개 중 10개).
- 기존 Transformers + Accelerate는 오프로드된 레이어 전체 전문가를 매 토큰 복사해 무너짐(`Qwen3.6-35B-A3B` · A10G 기준 0.16 tok/s).
- 이번 구현은 선택된 전문가만 SSD에서 읽어 **슬롯 풀**에 꽂고, ID를 슬롯 번호로 리매핑해 기존 전문가 커널(`grouped_mm` · `gather_qmm` · `mul_mat_id`)을 그대로 씀.
  - 💡 슬롯 풀(Slot Pool) : 디바이스 캐시 공간을 미리 잡아 두고 `expert_id → slot` 표로 번호만 바꿔 끼워 기존 커널에 넘기는 구조다.

# 어떻게 동작하나 ?
1. 가중치 분리 로드
   - `device_map={"": "mps", "experts.*": "disk"}`로 전문가는 건너뛰고 밀집 레이어 등 나머지만 올림.
   - 121GB(FP8) 전문가는 3-bit MLX(49GB)로 변환하거나 Strata GGUF IQ3_XXS(약 43GB · 평균 1.75MB)를 가져다 SSD에 두고, 51GB n-gram 테이블도 SSD에서 행 단위로 읽음.
   → 로드 후 약 18GiB(12GiB 캐시 포함), 4K 프리필 · 6K 문서 피크 20 ~ 22.5GiB(GGUF 기준)로 32GB 안에 들어감.
2. 레이어별 스트리밍 루프
   - 라우터가 고른 10개 인덱스를 호스트로 복사(레이어당 동기화 1회)해 적중(예: 8개)은 재사용하고 미스(예: 2개)만 8개 I/O 스레드로 빈 슬롯에 읽음. 유휴 SSD로 다음 레이어 추정 1개를 미리 읽고 쓰일 때만 캐시에 넣음.
   → 필요한 전문가만 옮겨 기존 커널로 연산함(전부 캐시된 `OLMoE-1B-7B`에서도 파이썬 루프 10.1 → 슬롯 풀 + `grouped_mm` 34.6 tok/s, 바닐라 38.1 tok/s).
3. 병목 제거
   - MPS 커널 지연 커밋을 서브블록 · 전문가 커널 뒤 이벤트 기록으로 풀어 디코드 +10.3%(8.52 → 9.40 tok/s) 확보.
   - C++ 없이 `torch.mps.compile_shader`로 커널 교체(레이어당) : Gated DeltaNet 프리필(2K토큰 67 → 28ms) · GGUF 타일 GEMM 프리필(2,048토큰 336 → 47ms) · 6K 키 희소 어텐션 디코드(0.95 → 0.12ms).
     - 💡 Gated DeltaNet : 선형 어텐션 토큰 믹서로 48개 중 36개 레이어를 차지함(나머지 12개는 최대 2,048토큰만 보는 희소 전체 어텐션).
   - Strata GGUF 교체로 밀집 5.4 → 3.9GB · 전문가 2.15 → 1.75MB로 줄여 디코드 +12 ~ 14%(읽기 30 ~ 40% 절감).
   - 4K 프리필 청크를 1K → 2K로 키워 SSD 읽기를 145GB → 86GB로 줄이고, 리드어헤드로 I/O를 겹치며 512토큰 이상은 콜드 LRU로 캐시 오염을 막음.
   → 초기 10.0 tok/s(프리필 68 tok/s)에서 최종 13.9 tok/s(프리필 228 tok/s)로 끌어올림.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 :
  - `Transformers + Accelerate` : 모듈 단위 복사라 8 ~ 10개만 쓰려고 오프로드된 레이어 전체 전문가를 매 토큰 옮김.
  - `llama.cpp` : RAM에 들어가면 빠르지만 넘치면 페이지 캐시가 스래싱됨. GPU 캐시는 토큰당 2 → 50분할돼 다 들어가도 약 10% 손실.
  - `vLLM` : 고정 RAM에 두고 캐시 · 디스크 계층 없이 매 토큰 PCIe로 읽음.
  - `vllm-metal` : 전문가만 스트리밍해 `Qwen3.8-Flash-Next`(Hub MLX)의 32GB n-gram 테이블이 남아 32GB Mac 실행 불가.
- 이번 방식 :
  - Transformers(`#50717`)의 라우팅 인지 · 슬롯 풀 · SSD 스트리밍 위에 전용 패키지(`moe-expert-streaming`)로 디스크 n-gram · Metal 커널 · Strata GGUF를 결합함.
→ 범용 프레임워크 기반으로 Strata 0.1.60 대비 짧은 디코드 약 6% 차이(6K 문서 후 1.1x), 4K 프리필 소폭 앞섬.

# 숫자로 보면

A10G(24GB VRAM · 충분한 RAM) `Qwen3.6-35B-A3B` 디코드 비교 :

| 엔진 / 조건 | 디코드 (tok/s) | 출처 |
|---|---|---|
| Strata (Q8_0) | 82 ~ 88 | HF Blog |
| llama.cpp (Q8_0, `--fit on`) | 63 ~ 64 | HF Blog |
| vLLM (FP8, `--cpu-offload-gb 16 --cpu-offload-params experts`) | 20.1 | HF Blog |
| vLLM (FP8, `--cpu-offload-gb 16`) | 9.7 | HF Blog |
| Transformers + Accelerate | 0.16 | HF Blog |

동일 M5 MacBook Pro(32GB · 153GB/s · SSD 7.1GB/s) `Qwen3.8-Flash-Next`(180B) 비교 (greedy 디코딩, thinking · MTP 오프 / 짧은 디코드 200토큰 4프롬프트 중앙값 / 프리필 초기 · Strata 1K, 최종 2K 청크) :

| 항목 | 초기 Transformers | 최종 Transformers (GGUF) | Strata 0.1.60 (IQ3_XXS) | 출처 |
|---|---|---|---|---|
| 짧은 디코드 (200토큰) | 10.0 tok/s | 13.9 tok/s | 14.8 tok/s | HF Blog · details.html · README |
| 4K 프리필 (4,059토큰) | 68 tok/s | 228 tok/s | 220 tok/s | HF Blog · details.html · README |
| 6K 문서 후 디코드 (6,062토큰) | 7.3 tok/s | 12.4 tok/s | 13.7 tok/s | HF Blog · details.html · README |

# 주의할 점 / 한계
- **PyTorch MPS 동기화 한계** : 48개 레이어 호스트 왕복(회당 약 210 ~ 250µs)이 토큰당 약 10ms를 먹음. Strata의 Metal shared event 대기를 PyTorch MPS는 노출하지 않음.
- **속도 · 메모리** : 약 14 tok/s는 저자 기준 코딩 에이전트엔 여전히 느림. 브라우저 실행 시 약 0.7 tok/s 하락 · 스왑이 생기며, 초기 3-bit는 6K 피크 25.4GiB이고 로드 직후 첫 6K 프리필(12GiB 캐시)이 메모리 워치독에 2회 종료된 적 있음.
- **POC · 변환 비용** : `transformers#50717`은 AI 작성 draft POC라 병합 전 재작성이 필요하고, FP8 원본(약 130GB) 변환에 약 5시간 걸림.
- **하드웨어 · 플랫폼** : M5(153GB/s · SSD 7.1GB/s) 자체 실측(M4 Mac mini 120GB/s · 2.97GB/s). CUDA A10G 프리뷰는 4.1(페이지 캐시) ~ 5.8 tok/s(호스트 사전 로드) · 4K 프리필 17 tok/s에 그치고, MLX v2 M5 bf16/fp16 다중 행 버그([kernels-community#1332](https://github.com/huggingface/kernels-community/issues/1332))로 해당 프리필은 fp32 우회 필요.
- **아직 확인 안 된 것** : 3-bit MLX와 원본 FP8 / 8-bit 전문가 간 perplexity 비교(원본 삭제로 미측정), M5 외 Apple Silicon · 다중 사용자 배치 성능은 원문에 없음.

# 정리
- M5 32GB Transformers에서 초기 10.0 → 13.9 tok/s(Strata 14.8 tok/s와 약 6% 차이), 4K 프리필 68 → 228 tok/s까지 끌어올린 실험이다.
- 저자 기준 코딩 에이전트엔 여전히 느리지만, 라우팅 희소성 · 전문가 캐시 · 메모리 대역폭 · 호스트-GPU 대기를 모듈 단위로 살펴보려는 엔지니어에게 참고가 됨.

# 참고
- [180B Parameters, 32GB of RAM: Pushing MoE Inference to the Limit with Transformers](https://huggingface.co/blog/moe-expert-streaming) — Hugging Face Blog
- [MoE expert streaming in Transformers (Details)](https://tarekziade-moe-expert-streaming.static.hf.space/details.html) — Hugging Face Space
- [tarekziade/moe-expert-streaming (Space)](https://huggingface.co/spaces/tarekziade/moe-expert-streaming) — Hugging Face Space
- [POC: Experts offload (#50717)](https://github.com/huggingface/transformers/pull/50717) — huggingface/transformers GitHub PR
- [tarekziade/moe-expert-streaming](https://github.com/tarekziade/moe-expert-streaming) — GitHub Repository
