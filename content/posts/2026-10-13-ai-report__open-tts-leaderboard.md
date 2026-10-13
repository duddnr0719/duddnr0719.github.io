---
weight: 138
title: "Open TTS Leaderboard — 투표 대신 자동 채점으로 오픈소스 TTS를 9개 언어에서 줄 세운다"
date: 2026-10-13T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 투표 대신 ASR · 화자 임베딩 같은 객관 지표로 오픈소스 TTS를 9개 언어에서 줄 세우는 리더보드다. 모델 1개 평가가 몇 주에서 몇 시간으로 줄어든다 !

# 개요
- 무엇 : Hugging Face가 2026.09.30 블로그로 공개한 TTS(텍스트 → 음성) 평가 리더보드. 평가 스크립트 레포는 2026.10.09 공개됨.
- 한 줄 정의 : Open TTS Leaderboard는 오픈소스 · 다국어 TTS 모델을 명료도 · 속도 · 화자 유사도 3가지 객관 지표로 비교하는 Hugging Face Space다.
- 원문 : [Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and Voice Cloning](https://huggingface.co/blog/open-tts-leaderboard)

# 그래서 도대체 뭔데 ?
- Hub에 올라온 TTS 모델은 8K개를 넘었는데 평가는 기준이 제각각임.
- 지금까지 기준점 역할을 한 건 TTS Arena v2 · Artificial Analysis · Voice Arena 같은 아레나형 리더보드였음.
	- 💡 아레나형 : 두 모델 음성을 들려주고 더 나은 쪽을 고르게 한 뒤, 투표로 Elo 점수를 매기는 방식
- 문제는 투표가 모이는 속도가 출시 속도를 못 따라간다는 것. 그리고 오픈 모델이 잘 안 올라감.
	- Artificial Analysis 92개 모델 중 오픈 웨이트는 16개뿐 (2026.09.30 기준)
	- 원문이 짐작한 이유 : 오픈 모델은 아레나 쪽에서 직접 띄워 서빙하는 부담이 있음 (API 모델은 키만 받으면 끝)
- 그래서 사람 투표를 기계 채점으로 바꾸고, 오픈소스와 다국어에 초점을 맞춘 게 이번 리더보드임.
	- 💡 WER / CER : 단어 / 글자 오류율. 생성 음성을 ASR로 다시 받아 적고 원래 텍스트와 비교함
	- 💡 RTFx : 오디오 길이 ÷ 생성 시간. 클수록 빠름
	- 💡 TTFA : 요청 후 재생 가능한 첫 오디오가 나올 때까지 걸리는 시간

# 어떻게 동작하나 ?
1. 데이터셋 준비
	- Seed TTS Eval(영어 · 중국어)과 CV3 Eval 제로샷(9개 언어, 언어당 500 샘플)을 씀.
	- 두 데이터셋 모두 라이선스상 재배포가 안 돼서 개인 비공개 사본을 만드는 스크립트를 따로 줌.
	→ HF 계정과 Jobs 크레딧이 있으면 같은 입력으로 다시 돌려볼 수 있음.
2. 음성 생성 — H200 1장
	- 백엔드별 run_eval.py가 모든 샘플을 합성하고 wav와 JSONL manifest를 버킷에 저장함.
	- warm-up 배치는 빼고 생성 구간만 시간을 재서 RTFx를 계산함.
	→ 모든 모델이 같은 GPU에서 생성되니 속도 비교가 공정해짐.
3. 전사 — L4 1장
	- Qwen3-ASR-1.7B로 생성 음성을 받아 적음. 스플릿 언어를 힌트로 넘김.
4. 화자 유사도 — L4 1장 (보이스 클론 모델만)
	- WavLM-large + ECAPA-TDNN 화자 검증 모델로 생성 음성과 참조 음성의 임베딩 코사인 유사도를 구함.
5. 채점 — 로컬
	- manifest만 내려받아 언어별 WER · RTFx · SIM을 계산함. WER은 텍스트 정규화 후 계산하고, 중국어 · 일본어 · 한국어는 CER로 채점함.
- 단계를 HF Job 여러 개로 쪼갠 이유 : TTS · ASR · 화자 검증 모델끼리 의존성이 충돌하기 때문임.
- 스트리밍 평가는 별도로 돎. batch size 1로 기본 목소리만 쓰고, 앞 3개를 warm-up으로 버린 뒤 p50 · p95 TTFA를 보여줌.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 아레나에서 사람이 들어보고 투표 → Elo 순위. 투표 수집에 몇 주가 걸리고 상업 API 모델 위주로 채워짐.
- 이번 방식 : 고정된 데이터셋 + ASR · 화자 임베딩 기반 자동 채점. 모델 1개를 몇 시간 안에 평가함.
→ 투표를 모을 필요가 없으니 출시 속도를 따라갈 수 있다는 게 원문 주장. 오픈소스에 초점을 둔 것도 아레나에서 묻힌 모델을 꺼내 보이려는 목적이라고 밝힘.
- 원본 벤치마크와도 다름 : 원래 Seed TTS Eval · CV3 Eval은 ASR로 Whisper-large-v3와 Paraformer를 썼는데, 리더보드는 Qwen3-ASR-1.7B 하나로 통일함.
- 보는 방법도 늘어남 : WER · RTFx · 모델 크기 파레토 플롯, 실제 출력을 듣고 투표하는 Listen 탭, TTFA 순 Streaming 탭.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 모델 1개 평가 시간 | 몇 주 (투표 수집) | 몇 시간 | [HF 블로그](https://huggingface.co/blog/open-tts-leaderboard) |
| 오픈 웨이트 비중 (Artificial Analysis) | 92개 중 16개 | 오픈소스 중심 | [HF 블로그](https://huggingface.co/blog/open-tts-leaderboard) |
| 평가 언어 | Seed TTS Eval 원본 : 영어 · 중국어 | 9개 언어 (CV3 Eval) | [레포 README](https://github.com/huggingface/open-tts-leaderboard) |
| Seed TTS Eval 규모 | - | Common Voice 1,000 + DiDiSpeech-2 2,000 샘플 | [seed-tts-eval](https://github.com/BytedanceSpeech/seed-tts-eval) |
| 생성 / 전사 하드웨어 | - | H200 141GB / L4 24GB | [레포 README](https://github.com/huggingface/open-tts-leaderboard) |
| TTFA 하드웨어 | - | A100 80GB, CPU 8 vCPU · 32GB | [레포 README](https://github.com/huggingface/open-tts-leaderboard) |
| 스모크 테스트 예시 (seamless-m4t-v2-large, 영어 8 샘플) | - | 종합 WER 2.27%, RTFx 21.19 | [레포 README](https://github.com/huggingface/open-tts-leaderboard) |

- 원문은 모델별 점수를 숫자로 적지 않고 순위만 언급함.
	- 영어 WER 상위 : Kokoro-82M · supertonic-3 · s2-pro
	- 다국어 강세 : OmniVoice · s2-pro · Fun-CosyVoice3-0.5B-2512
	- 보이스 클론을 켜면 WER이 좋아지는 모델 : higgs-tts-3-4b · VoxCPM2
	- GPU · CPU 스트리밍 둘 다 좋은 모델 : pocket-tts

# 주의할 점 / 한계
- 사람 선호 순위를 대신하는 게 아니라고 원문이 직접 밝힘.
	- WER은 알아듣기 쉬운지를 간접적으로 볼 뿐이고, SIM도 목소리가 얼마나 닮았는지 어림한 값임
	- 자연스러움 · 표현력 · 청취자 취향은 어느 지표도 직접 재지 않음
- 다국어 점수 중 영어 · 중국어 외 언어는 CV3 Eval 하나로만 계산됨.
- 스모크 테스트 수치는 8 샘플짜리 동작 확인용이라 순위로 읽으면 안 됨.
- 문서끼리 TTFA 조건이 다름.
	- 블로그 : H200 GPU, 영어 프롬프트 50개, 중앙값
	- 레포 README : A100 GPU, 500 샘플 전체, p50 · p90 · p95
	→ 이 글은 실행 스크립트 문서인 레포 쪽을 따름.
- CPU TTFA 결과는 아직 소수 모델만 있음.

# 정리
- 사람 투표 대신 고정 데이터셋 + 자동 채점으로 바꿔서 오픈소스 TTS를 9개 언어에서 빠르게 비교할 수 있게 됨.
- 평가 파이프라인이 HF Jobs 스크립트로 공개돼 있어서 새 모델을 직접 넣어보고 PR로 올릴 수 있음.
- 음성 에이전트처럼 첫 응답 지연이 중요한 쪽이면 Streaming 탭의 TTFA를 같이 보는 게 좋음.

# 참고
- [Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and Voice Cloning](https://huggingface.co/blog/open-tts-leaderboard) — Hugging Face 블로그
- [huggingface/open-tts-leaderboard](https://github.com/huggingface/open-tts-leaderboard) — GitHub 레포 (평가 스크립트)
- [BytedanceSpeech/seed-tts-eval](https://github.com/BytedanceSpeech/seed-tts-eval) — GitHub 레포 (Seed TTS Eval)
- [QwenAudio/CV3-Eval](https://github.com/QwenAudio/CV3-Eval) — GitHub 레포 (CV3 Eval)
