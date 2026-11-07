---
weight: 181
title: "Phonon TTS — 64MB 가중치와 5ms 첫 오디오 지연으로 기기에서 바로 말하는 온디바이스 음성 합성"
date: 2026-11-07T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 64MB 크기와 5ms 첫 오디오 지연으로 노트북 · 스마트폰 · 브라우저에서 서버 없이 돌아가는 오픈 웨이트 온디바이스 TTS 모델 !

# 개요
- 무엇 : Gradium이 2026.04.03 최초 발표 후 2026.10.20 오픈 웨이트로 정식 출시하고, 2026.11.05 Hugging Face 블로그를 통해 Open TTS 리더보드 성적과 Hugging Face 팀이 구축한 Transformers v5.21 통합 구조를 공개한 소형 온디바이스 음성 합성 모델 패밀리임.
- 한 줄 정의 : Phonon은 31M · 40M 파라미터 규모의 연속 오디오 언어 모델 구조와 단일 스텝 플로우 매칭을 결합해 네트워크 없이 로컬 기기에서 음성을 합성하는 TTS 모델이다.
- 원문 : [A Closer Look at Phonon TTS. Launching High-Quality On-Device Speech That Tops the Benchmarks.](https://huggingface.co/blog/phonon-tts)

# 그래서 도대체 뭔데 ?
- 기존 음성 AI가 문장마다 클라우드 서버를 왕복해야 했던 것과 달리 텍스트와 음성 생성을 모두 사용자 기기 안에서 처리하는 로컬 우선 TTS임.
- Kyutai의 Pocket TTS 계보를 이어받아 80ms 프레임마다 잠재 벡터를 자기회귀로 예측하고 플로우 매칭 헤드로 연속 오디오 임베딩을 뽑아냄.
	- 💡 플로우 매칭 (Flow Matching) : 트랜스포머 백본이 출력한 은닉 상태 벡터와 가우시안 노이즈를 입력받아 연속 오디오 잠재 임베딩으로 변환하는 생성 기법임.
	- 💡 라그랑주 자기 증류 (LSD, Lagrangian Self-Distillation) : 플로우 스텝의 시작 · 종료 시점을 조건으로 받아 가우시안 노이즈에서 오일러(Euler) 스텝으로 잠재 벡터를 샘플링하도록 순간 플로우(대각 항)와 자기 증류 항을 결합한 플로우 헤드 학습 목적함수임.
- 영어 전용인 Phonon 31m(q8 GGUF 기준 64MB, Apache 2.0)과 영어 · 프랑스어 · 독일어 · 스페인어 · 포르투갈어 5개 언어를 언어별 개별 모델 또는 단일 가중치 다국어 모델로 지원하는 Phonon 40m · 40m multilingual(74.6MB, CC BY-NC 4.0)의 두 가지 크기로 배포됨.
- Rust 기반 전용 런타임 `ptts`로 CPU · GPU · NPU 등 10개 이상의 백엔드에서 단일 스트림 지연을 줄였고, Hugging Face Transformers에서는 배치 합성과 모델 연구를 지원함.

# 어떻게 동작하나 ?
1. 텍스트 · 화자 프리픽스 조건화 (Conditioning)
	- 입력 텍스트를 음소(phoneme) 변환 없이 4,000 토큰 어휘(패딩 포함 4,001) 크기의 SentencePiece 토크나이저로 직접 토큰화함.
	- 화자 음성은 원본 녹음 파일 대신 Mimi 인코더 기반 화자 코덱으로 사전 계산한 512차원 잠재 텐서(`(num_frames, 512)`)를 사용하며, 텍스트 임베딩과 이어 붙여 백본의 프리픽스로 넣음.
	→ 별도의 음소 변환기나 런타임 오디오 인코더 없이 새로운 언어로 쉽게 확장하고 사전 계산된 음성 텐서로 바로 조건화할 수 있음.
2. 인과적 트랜스포머 백본 (Causal Transformer Backbone)
	- 프리픽스와 오디오 시작 토큰(`BOS`) 뒤를 이어 80ms 프레임(초당 12.5프레임, 12.5Hz) 단위로 은닉 상태 벡터를 자기회귀 방식으로 출력함.
	- 각 오디오 잠재 위치에는 화자 수 조건(`num_speakers`)과 사인파 임베딩으로 변환된 발화 속도 조절값(`duration_delta`)이 더해짐.
	- 모든 모델은 더 큰 Phonon 교사(teacher) 모델에서 증류(distillation)되었으며, 폭(width) 512와 어텐션 헤드 8개를 유지한 채 31M은 6층, 40M은 9층만 쌓아 연산량을 줄임.
	→ 6층 · 9층의 작은 백본 크기로도 프레임 단위 스트리밍 생성과 발화 속도 제어가 가능함.
3. 단일 스텝 플로우 매칭 헤드 및 EOS 헤드
	- 백본이 내놓은 은닉 상태와 가우시안 노이즈를 플로우 매칭 헤드에 통과시켜 단 1스텝 만에 32차원 연속 오디오 잠재 프레임을 생성하고, 이를 다음 타임스텝의 백본 입력으로 다시 넣음.
	- 동시에 발화 종료(EOS) 헤드가 은닉 상태를 보고 음성 생성을 멈출 시점을 판정함.
	- 초기 학습의 수치적 불안정성을 해결하기 위해 여러 학습 기법을 적용했으며, 코드상에는 첫 1,000스텝 동안 타깃 잠재 벡터의 평균 · 표준편차 지수이동평균(EMA, 감쇠율 0.999)을 추적하는 정규화와 3층 32폭 MLP로 플로우 시간별 LSD 손실의 불확실성 가중치를 학습하는 구성이 포함됨.
	→ 작은 모델 크기에서도 플로우 매칭으로 음성 품질을 확보하고, 전체 문장이 완성되기를 기다리지 않고 프레임 단위로 바로 스트리밍할 수 있음.
4. 경량 Mimi 코덱 디코더 및 이원화된 추론 스택
	- 플로우 매칭 헤드와 모든 모델이 공유하는 경량 Mimi 디코더 변형이 32차원 잠재 벡터를 프레임당 80ms 분량의 24kHz 모노 PCM 오디오로 복원함.
	- 온디바이스용 `ptts`는 Rust 텐서 런타임(`xn`)으로 작성되어 PyTorch 없이 동작하며, GPU 처리량 중심인 Transformers 구현은 Pocket TTS 코드 위에 차이점만 정의한 약 200줄(실제 파일 202줄 · 180 LOC)의 모듈러 코드로 배치 생성과 `torch.compile`을 지원함.
	→ 애플 워치 · 라즈베리 파이 · 브라우저 탭 같은 온디바이스 단일 스트림 추론부터 대규모 음성 데이터셋 합성용 GPU 배치 처리까지 용도에 맞는 런타임으로 실행할 수 있음.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 클라우드 TTS는 문장마다 네트워크 왕복 지연과 사용량 비례 비용이 발생했고, Kokoro(82M) 같은 기존 소형 모델은 문장 전체를 다 만든 뒤에야 오디오를 반환해 첫 소리까지 수백 ms ~ 수 초가 걸리거나 전화번호 · 날짜 같은 구조화 텍스트에서 발음 오류가 잦았음.
- 이번 방식 : 텍스트 정규화 파이프라인을 결합한 31M · 40M 교사 증류 백본이 80ms 프레임을 스트리밍으로 생성하고, Arm KleidiAI · Apple Core ML · Snapdragon QNN 등 하드웨어 가속 백엔드를 네이티브로 붙임.
→ 네트워크 없이 기기 내부에서 동작하면서도 첫 오디오 지연(TTFA)을 5 ~ 9ms(노트북 · 스마트폰 기준, HF CPU 리더보드 95백분위수 28 ~ 38ms)로 낮추고, 전화번호 · 버전 번호 · 시간 같은 구조화 텍스트의 단어 오류율(WER)을 1.70 ~ 2.22%(Kokoro 3.50% · Magpie 27.51%)로 줄임.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 모델 크기 및 파라미터 | Pocket TTS 100M · 15.6M / Kokoro 82M | Phonon 31m 64MB (생성 모델 30,788,354 + 오디오 토크나이저 10,305,313) / 40m 74.6MB (q8 GGUF) | [HF 블로그](https://huggingface.co/blog/phonon-tts) · [Gradium 블로그](https://gradium.ai/blog/release-phonon-open-weight) |
| HF Open TTS 리더보드 CPU 스트리밍 TTFA (95백분위수) | Pocket TTS 165ms | Phonon 31m en 28ms (1위) · Phonon 40m en 38ms (2위) | [HF 블로그](https://huggingface.co/blog/phonon-tts) |
| 영어 자연스러움 (블라인드 쌍대비교 Elo, 1,189명 · 17,270표) | Pocket TTS 100m 2,056 · Kokoro 2,043 · NeuTTS 2,034 · Pocket TTS 15.6m 1,997 · Magpie 1,939 | Phonon 40m 2,117 · Phonon 31m 2,098 · 40m multi 2,097 | [Gradium 블로그](https://gradium.ai/blog/release-phonon-open-weight) |
| 다국어 자연스러움 (블라인드 쌍대비교 Elo) | Kokoro (FR 1,578 · ES 1,629 · PT 1,633) / Magpie (FR 1,608 · DE 1,640 · ES 1,870) | Phonon 31m · 40m · 40m multi (FR 2,060 · 2,072 · 2,011 / DE 2,113 · 2,097 · 2,046 / ES 2,106 · 2,103 · 2,076 / PT 2,104 · 2,144 · 2,048) | [Gradium 블로그](https://gradium.ai/blog/release-phonon-open-weight) |
| 구조화 텍스트 정확도 (WER, 언어당 500문장 하드케이스) | Kokoro 3.50% · Kitten TTS 7.40% · NeuTTS Nano 8.71% · Magpie 27.51% | Phonon 31m 1.70% (1위) · 40m multi 2.11% (2위) · 40m 2.22% (3위) | [Gradium 블로그](https://gradium.ai/blog/release-phonon-open-weight) |
| MacBook Air M5 추론 속도 및 TTFA (기본 CPU 4스레드) | Kokoro 10.9× · 517ms / Magpie 2.32× · 239ms | Phonon 31m 29.9× · 6.9ms · 40m 27.9× · 8.8ms (KleidiAI + Accelerate 적용 시 31m 1코어 26.0× · 5ms / 4스레드 46.7× · 5.4ms) | [Gradium 블로그](https://gradium.ai/blog/release-phonon-open-weight) |
| 모바일 · 엣지 기기 추론 성능 | Raspberry Pi 5에서 Kokoro 시작 7초 · 실시간 미만 | iPhone 16 Pro Neural Engine 31m 22× · 9ms (40m 20× · 12ms) / Snapdragon 8 Elite Gen 5 (Oryon CPU) 24× · 7.5ms / Raspberry Pi 5 31m 멀티스레드 3.7× · 38ms (1코어 2.3× · 68ms) | [Gradium 블로그](https://gradium.ai/blog/release-phonon-open-weight) · [xn-ptts 레포](https://github.com/gradium-ai/xn-ptts) |

# 주의할 점 / 한계
- 상업적 라이선스와 접근 제한이 모델 크기에 따라 나뉨 : 영어 전용인 Phonon 31m만 Apache 2.0으로 상업적 무료 사용이 가능하고, 5개 언어를 지원하는 Phonon 40m 및 40m multilingual은 비상업용 CC BY-NC 4.0 라이선스(상업 이용 시 음성 생성량 대신 사용자 수 기반 과금)에 Hugging Face 약관 동의와 토큰이 필요한 gated 모델이라 브라우저 패키지(`phonon-tts`)에서 Hugging Face 허브를 통해 직접 불러올 수 없음(파일을 직접 내려받아 앱에서 서빙해야 함).
- 모델 크기와 언어 · 플랫폼 제약 : 원문은 가장 작은 31M 모델이 크기를 줄이는 대신 표현력과 정확도 일부를 타협했다고 설명하며, 한국어 · 아랍어 · 일본어는 공개 가중치에 포함되지 않아 디자인 파트너 맞춤형 학습으로만 제공됨. 또한 Swift 패키지는 iOS 18+ · macOS 15+(Apple Silicon)와 별도 Core ML 모델 번들이 필요하고, Android Snapdragon NPU(QNN) 라이브러리는 Android 12+ · 휴대폰 SoC별 컴파일 번들이 필수이며 CPU 자동 폴백을 지원하지 않음.
- 벤치마크 조건을 볼 때 주의가 필요함 : 구조화 텍스트 WER 평가셋(`gradium/tts-hard-sentences-202610`, 언어당 500문장)은 개발자들이 제보한 실패 사례로 Gradium이 직접 구축해 `qwen3.8-omni-flash` 전사와 `gemma-4-31b-it`로 채점한 자체 벤치마크임. 영어 전용인 Phonon 31m(1.70%) · Kitten TTS(7.40%)와 달리 Phonon 40m 계열(2.11% · 2.22%)은 다국어에서 평가되었으며 Kokoro는 독일어 미지원 · NeuTTS는 포르투갈어 미지원 조건에서 측정됨. 속도 벤치마크에서도 Kokoro는 스트리밍 기능이 없어 전체 문장(약 5초 분량 영어 1문장) 생성 시간이 곧 첫 오디오 지연(517 ~ 776ms)으로 잡혔고 WebGPU 백엔드는 배치당 4프레임을 묶어 생성하므로 첫 오디오 지연이 CPU보다 높게 나옴.
- 아직 확인 안 된 것 : 증류에 사용된 교사(teacher) 모델의 정확한 파라미터 크기, 전체 학습 데이터 시간, 한국어 · 일본어 등 추가 언어의 오픈 웨이트 공개 일정은 원문에 없음.

# 정리
- 연속 오디오 잠재 공간과 1스텝 플로우 매칭, 교사 증류를 결합해 64 ~ 74.6MB 크기로도 자연스러움(Elo)과 숫자 · 코드 읽기 정확도(WER 1.70 ~ 2.22%)에서 기존 소형 TTS를 앞선 온디바이스 모델임.
- 네트워크 연결 없이 동작해야 하는 모바일 · 워치 앱, 브라우저 내 실시간 음성 인터페이스, 차량용 임베디드 보이스나 로컬 에이전트에 가벼운 TTS(영어 상업용 무료 31m 또는 다국어 비상업용 40m)를 붙이려는 개발자가 바로 써먹을 만함.

# 참고
- [A Closer Look at Phonon TTS. Launching High-Quality On-Device Speech That Tops the Benchmarks.](https://huggingface.co/blog/phonon-tts) — Hugging Face Blog
- [Open-Sourcing Phonon: A Suite of Frontier On-Device TTS Models](https://gradium.ai/blog/release-phonon-open-weight) — Gradium Blog
- [gradium-ai/xn-ptts: Phonon TTS inference using xn](https://github.com/gradium-ai/xn-ptts) — GitHub
- [transformers/src/transformers/models/gradium_phonon_tts/modular_gradium_phonon_tts.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/gradium_phonon_tts/modular_gradium_phonon_tts.py) — Hugging Face Transformers GitHub
