---
weight: 172
title: "AnySpeechRecognizer와 AnyDecisionModel — 온디바이스 음성 인식과 결정 모델을 Swift로 묶는다"
date: 2026-10-30T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> LLM 텍스트 생성에 의존하던 음성 전사와 의사결정을 온디바이스 전용 모델로 분리해 Apple 생태계에서 타입 안전하게 처리하는 오픈 패키지 !

# 개요
- 무엇 : Hugging Face의 mattt가 2026.10.29에 Apple 플랫폼용 패키지 AnySpeechRecognizer와 AnyDecisionModel을 공개함.
- 한 줄 정의 : AnySpeechRecognizer와 AnyDecisionModel은 Apple 플랫폼에서 Core ML과 MLX를 통해 오픈 음성 모델과 결정 모델을 타입 안전한 Swift API로 실행하는 오픈소스 Swift 패키지다.
- 원문 : [Introducing AnySpeechRecognizer and AnyDecisionModel: Open Models for Speech and Decisions on Apple Platforms](https://huggingface.co/blog/anydecisionmodel)

# 그래서 도대체 뭔데 ?
- LLM에 음성 받아쓰기와 티켓 분류를 전부 넘기면 추론 비용과 지연 시간이 불필요하게 커짐.
- 음성 인식과 의사결정(분류 · 라우팅 · 채점)에 특화된 경량 모델을 기기 내부에서 직접 구동하는 방식임.
- AnySpeechRecognizer는 최신 Apple API 규격을 유지하면서 Parakeet이나 Qwen3-ASR 및 화자 분리 모델을 연동함.
- AnyDecisionModel은 텍스트 생성 없이 모델의 다음 토큰 확률과 결정 헤드로 예/아니오, 다지선다, 서열 척도를 판정함.
	- 💡 결정 모델(Decision Model) : 자유 텍스트를 생성하지 않고 상태와 질문에 대해 각 선택지의 확률값만 계산하는 모델.
	- 💡 화자 분리(Speaker Diarization) : 음성 스트림에서 여러 사람의 발화 구간을 나누고 누가 언제 말했는지 추적하는 기술.

# 어떻게 동작하나 ?
1. 음성 인식 및 화자 분리 연동
	- Apple의 최신 음성 API 규격을 유지한 채 `SpeechTranscriber`에 Parakeet v3나 Qwen3-ASR 백엔드를 지정함.
	- 동일한 분석기에 `SpeakerDiarizer` 모듈을 붙여 NVIDIA Streaming Sortformer로 최대 4명 화자를 동시 추적함.
	- 오디오 버퍼가 들어오면 `SpeakerTimeline`이 단어별 시간 정보와 화자를 매핑하여 발화록을 순차 전달함.
	→ Apple 기본 프레임워크 교체 없이 외부 음성 모델과 화자 분리를 동일 타임라인에서 다룸.

2. 상태 기반 결정 세션 구성
	- 판정 대상 텍스트나 JSON 형태의 불변 상태(state)를 담아 DecisionSession을 생성함.
	- Swift 열거형(`Choosable`)으로 선택지를 선언하고 `session.choice()`나 `session.score()`를 호출함.
	→ 복잡한 프롬프트 작성이나 JSON 파싱 실패 없이 타입이 검증된 결과 객체를 바로 얻음.

3. 백엔드별 추론 실행
	- MLX · Core AI · llama.cpp는 각 보기에 1개 토큰 레이블을 지정하고 단일 순방향 패스에서 다음 토큰 확률을 읽음.
	- Clef-Flash 같은 전용 결정 헤드 모델은 9B 백본과 Joint Schema Head로 다수 질문의 선택지 로짓을 한 번에 계산함.
	- Jev 및 Ollama 백엔드는 System One API 규격으로 외부 또는 로컬 결정 서버와 통신함.
	→ 자기회귀 텍스트 디코딩 루프를 거치지 않고 단일 순방향 연산만으로 확률 분포를 추출함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 :
	- 음성 인식은 Apple 독점 엔진에만 묶여 있었음.
	- Apple 기본 프레임워크에는 화자 분리 모듈이 아예 없었음.
	- 분류와 판단 작업도 언어 모델에 프롬프트를 전달하고 생성된 텍스트를 파싱했음.
- 이번 방식 :
	- Apple Speech API 규격을 유지하면서 `SpeechTranscriber`와 `SpeakerDiarizer`에 오픈 모델을 지정해 즉시 교체 구동함.
	- `SpeakerDiarizer`로 음성 전사와 화자 구분을 단일 파이프라인에서 통합 처리함.
	- 텍스트 생성을 건너뛰고 로짓 확률과 결정 헤드를 직접 읽어 선택지별 확률 분포와 신뢰도를 즉시 반환함.
→ 텍스트 디코딩 과정을 거치지 않고 온디바이스에서 확률과 결정 헤드를 직접 읽어 지연 시간과 비용을 줄임.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| LibriSpeech clean 파일 WER (3 ~ 8분) | 2.12% | 1.43% (Unified) / 1.55% (v3) / 1.66% (Ultra) | [원문 블로그](https://huggingface.co/blog/anydecisionmodel) |
| LibriSpeech other 파일 WER (3 ~ 8분) | 3.97% | 2.19% (Unified) / 2.55% (Ultra) / 2.78% (v3) | [원문 블로그](https://huggingface.co/blog/anydecisionmodel) |
| 1시간 오디오 전사 속도 (Parakeet 파일 모드) | 미기재 | 약 20 ~ 40초 | [원문 블로그](https://huggingface.co/blog/anydecisionmodel) |
| Parakeet 런타임 메모리 점유 | 미기재 | 약 100MB (Core ML 컴파일 후) | [원문 블로그](https://huggingface.co/blog/anydecisionmodel) |
| Emoji Magnet 343개 질문 지연 (MLX Qwen3-4B, M4 Max) | 미기재 | 16개 묶음당 약 0.45초 (전체 약 10초) | [원문 블로그](https://huggingface.co/blog/anydecisionmodel) |
| Clef-Flash 4비트 모델 크기 및 권장 메모리 | 미기재 | 크기 6.2GB / Mac 메모리 16GB 이상 권장 | [원문 블로그](https://huggingface.co/blog/anydecisionmodel) |

# 주의할 점 / 한계
- 원문이 스스로 밝힌 한계 :
	- 겹치는 회의 음성 취약 : 참석자들이 동시에 발화하는 AMI 회의 데이터셋에서는 모든 엔진의 단어 오류율이 23% 초과로 증가함.
	- 선택지 개수 제한 : 다음 토큰 백엔드(MLX, Core AI, llama.cpp)는 토큰 매핑 구조상 다지선다 최대 26개, 점수 척도 최대 10단계로 제한됨 (Clef 결정 헤드는 제한 없음).
	- 의존성 충돌 : AnyDecisionModel의 CoreAI 트레이트(coreai-kit 0.7.3)와 AnySpeechRecognizer는 swift-huggingface 버전 불일치로 동시에 사용하지 못함.
- 수치의 조건 :
	- 측정 하드웨어는 M4 Max Mac Studio, macOS 27.0.1 단일 기기 환경에서 계측됨.
	- 환경 요구 사양 : Swift 6.2 이상, macOS 26 또는 iOS 26 이상이 요구됨.
- 아직 확인 안 된 것 :
	- iPhone 실기기 환경에서의 성능 수치는 원문에 없음.

# 정리
- 음성과 판단이라는 에이전트의 입력과 출력을 경량 온디바이스 모델로 분리해 지연 시간과 비용을 줄인 설계임.
- Apple 생태계에서 로컬 AI 워크플로를 구현하거나 Swift 기반 온디바이스 에이전트를 개발할 때 유용함.

# 참고
- [Introducing AnySpeechRecognizer and AnyDecisionModel: Open Models for Speech and Decisions on Apple Platforms](https://huggingface.co/blog/anydecisionmodel) — Hugging Face 블로그
- [AnySpeechRecognizer GitHub 레포지토리](https://github.com/mattt/AnySpeechRecognizer) — GitHub
- [AnyDecisionModel GitHub 레포지토리](https://github.com/mattt/AnyDecisionModel) — GitHub
- [Cloudflare Clef-Flash 모델 카드](https://huggingface.co/Cloudflare/clef-flash) — Hugging Face
