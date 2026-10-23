---
weight: 163
title: "Granite Speech 5.0 — 2B 음성 LLM부터 19,870 RTFx 초고속 CTC까지 오픈 웨이트로 공개"
date: 2026-10-23T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 고정밀 음성 LLM부터 19,870 RTFx를 기록하는 온디바이스 초고속 모델까지, 엔터프라이즈 음성 파이프라인 3종을 오픈소스로 공개함 !

# 개요
- 무엇 : IBM이 2026.10.21에 오픈 웨이트 음성 모델 패키지 'Granite Speech 5.0' 컬렉션을 공개함.
- 한 줄 정의 : Granite Speech 5.0은 고정밀 전사 · 번역용 2B 음성 LLM, 온디바이스 초고속 전사용 470M CTC 모델, 회의 녹음용 화자 분리 · 타임스탬프 2B 모델 3종으로 구성된 오픈소스 음성 패키지다.
- 원문 : [Granite Speech 5.0: Transcribe, Translate, and Attribute more Accurately and Faster](https://huggingface.co/blog/ibm-granite/granite-speech-5)

# 그래서 도대체 뭔데 ?
- 단일 거대 모델 하나 대신 작업 성격에 맞춘 3개 특화 모델을 묶어서 배포함.
- 플래그십 `granite-speech-5.0-2b`는 텍스트 LLM 기반으로 음성 인식(ASR)과 양방향 번역(AST), 최대 2,000개 전문 용어 바이어싱을 지원함.
- 경량 모델 `granite-speech-5.0-470m-turboctc`는 비자기회귀 디코딩으로 단말기에서 19,870 RTFx 속도로 구두점 포함 전사를 끝냄.
- 회의록 전용 `granite-speech-4.1-2b-plus`는 화자 분리 오류율을 4.10%로 낮추고 타임스탬프 오차(AAS)를 98.54ms 수준으로 줄여 발화자와 발화 시점을 정밀하게 식별함.
- 💡 ASR (Automatic Speech Recognition) : 사람의 음성 신호를 텍스트로 변환하는 자동 음성 인식 기술.
- 💡 AST (Automatic Speech Translation) : 음성을 인식함과 동시에 타 언어 텍스트로 번역하는 음성 번역 기술.
- 💡 RTFx (Real-Time Factor Reciprocal) : 오디오 1초를 처리하는 배속 배율. 수치가 클수록 빠름.
- 💡 Conformer : 국소 특징용 합성곱(CNN)과 전역 문맥용 트랜스포머 어텐션을 결합한 음성 신경망 구조.
- 💡 CTC (Connectionist Temporal Classification) : 음향 프레임과 텍스트 토큰 간 직접 정렬 라벨 없이도 시퀀스를 학습하는 손실 함수 및 디코딩 기법.

# 어떻게 동작하나 ?
1. 음성 인코더 및 어텐션 블록
	- 16개 Conformer 블록으로 음성을 처리하고 4초 블록-어텐션을 적용함.
	- 중간 계층 self-conditioned CTC와 윈도우 크기 4의 posterior-weighted pooling으로 음향 프레임을 압축함.
	→ 텍스트 정렬과 무관한 음향 연산을 인코더 단계에서 먼저 걸러냄.

2. Q-Former 프로젝터와 시계열 다운샘플링
	- 2계층 window query transformer (Q-Former)가 15개 1024차원 임베딩 블록을 받아 레이어당 3개 쿼리로 5배 다운샘플링함.
	- 인코더 2배 압축과 합쳐 총 10배 다운샘플링을 거쳐 LLM에 10Hz 레이트로 음향 임베딩을 넘김.
	→ LLM이 과도하게 긴 음향 토큰 시퀀스를 처리하느라 발생하는 속도 저하를 차단함.

3. 텍스트 LLM 결합 디코딩
	- 16k 컨텍스트로 확장된 `granite-4.0-1b-base` 체크포인트에 어쿠스틱 임베딩을 주입함.
	- 프롬프트에 대상 언어(Language ID)나 최대 2,000개 키워드 목록을 넣어 전사와 번역을 제어함.
	→ 별도 파이프라인 없이 단일 디코딩으로 서식이 갖춰진 다국어 전사와 번역 결과를 산출함.

4. TurboCTC의 비자기회귀 디코딩
	- 470M 모델은 LLM 생성 루프 대신 16,384개 BPE 헤드에서 단일 패스 greedy 디코딩을 수행함.
	- 단일 Conformer 블록을 컴파일해 그래프를 재사용함으로써 웜업 시간을 단축함.
	→ 온디바이스 환경에서 지연 없이 실시간 전사를 완성함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 이전 세대 모델은 긴 회의 녹음에서 타임스탬프가 밀리고 고유명사 인식 오류가 잦았음. 온디바이스 모델은 영어에 한정되거나 구두점 복원을 위해 별도 후처리 모델을 붙여야 했음.
- 이번 방식 : 5.0 2B는 최대 2,000개 단어까지 키워드 바이어싱을 받아 도메인 용어를 정확히 잡고 노이즈 내성을 보강함. 470M TurboCTC는 7개 언어로 확장되면서 대소문자와 구두점을 기본 출력하고 19,870 RTFx를 기록함. 4.1 2B Plus는 타임스탬프 평균 오차(AAS)를 210.86ms에서 98.54ms로 53% 단축함.
→ 음향 압축과 특화 프롬프트 설계를 분리하고 각 모델의 구조를 작업 목적에 맞춰 최적화했기 때문임.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 5.0 2B 영어 단문 WER (Open ASR Leaderboard) | - | 5.06% (오픈 웨이트 2위) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 5.0 2B 키워드 바이어싱 지원 단어 수 | - | 최대 2,000개 | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 5.0 2B 학습 오디오 데이터 | - | 390,000시간 | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 470M TurboCTC 추론 속도 (Open ASR Leaderboard) | 약 12,600 RTFx | 19,870 RTFx (1.6배 향상) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 470M TurboCTC 영어 단문 WER (Open ASR Leaderboard) | 5.78% (영어 전용) | 5.51% (7개 다국어 지원) | [Hugging Face 모델 카드](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) |
| 4.1 2B Plus 타임스탬프 전체 음성 오차 (AAS) | 210.86ms | 98.54ms (53% 단축) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 4.1 2B Plus 20단어 키워드 바이어싱 WER | 11.79% | 6.48% (오류 45% 감소) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 4.1 2B Plus 장문 음성 전사 WER | 13.53% | 10.22% (오류 24% 감소) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 4.1 2B Plus 화자 분리 오류율 (WDER) | 4.40% | 4.10% (7% 개선) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |
| 4.1 2B Plus 화자 포함 전사 오류율 (cpWER) | 30.50% | 28.48% (7% 개선) | [Hugging Face 블로그](https://huggingface.co/blog/ibm-granite/granite-speech-5) |

# 주의할 점 / 한계
- 5.0 2B 음성 LLM의 권장 입력 길이는 세그먼트당 약 2분 (120초) 단위이며, 긴 음성은 VAD 등으로 분할 디코딩해야 함.
- 4.1 2B Plus 모델은 화자 태그와 타임스탬프 추출에 집중되어 구두점 및 대소문자 서식 출력은 지원하지 않음.
- llama.cpp 양자화 시 Q8_0은 무손실에 가깝지만, 더 낮은 비트 양자화는 1분 이상의 음성에서 정확도 저하가 발생함.
- 수치 환경 : 5.0 2B는 IBM Blue Vela 클러스터의 8개 NVIDIA H100 GPU에서 40일 (인코더 26일 + 프로젝터 14일) 동안 학습됨. 470M 모델도 동일 클러스터 8개 H100 GPU에서 24일간 학습됨.
- 아직 확인 안 된 것 : 브라우저 WebGPU 스트리밍 데모의 실제 지연 시간과 Apple M시리즈별 실측 속도는 원문에 없음.

# 정리
- 고정밀 전사 · 번역부터 엣지 기기 초고속 처리, 회의록 화자 라벨링까지 엔터프라이즈 환경에서 요구되는 3개 작업군을 명확히 겨냥한 구성임.
- Apache 2.0 라이선스로 오픈되어 온프레미스 음성 파이프라인이나 온디바이스 음성 비서를 구축하려는 엔지니어에게 실질적인 선택지가 됨.

# 참고
- [Granite Speech 5.0: Transcribe, Translate, and Attribute more Accurately and Faster](https://huggingface.co/blog/ibm-granite/granite-speech-5) — Hugging Face Blog
- [ibm-granite/granite-speech-5.0-2b](https://huggingface.co/ibm-granite/granite-speech-5.0-2b) — Hugging Face Model Card
- [ibm-granite/granite-speech-5.0-470m-turboctc](https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc) — Hugging Face Model Card
- [ibm-granite/granite-speech-4.1-2b-plus](https://huggingface.co/ibm-granite/granite-speech-4.1-2b-plus) — Hugging Face Model Card
