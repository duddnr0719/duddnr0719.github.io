---
weight: 137
title: "Falcon ASR — 1.6B 단일 가중치로 에미리트 방언과 영어를 인식한다"
date: 2026-10-12T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 아랍어 표준어와 에미리트 방언, 영어까지 1.6B 크기 단일 가중치로 인식하고 단어 단위 타임스탬프까지 뽑아낸다 !

# 개요
- 무엇 : TII(Technology Innovation Institute)가 2026.10.07 공개한 다국어 음성 인식 모델.
- 한 줄 정의 : Falcon-ASR는 표준 아랍어와 에미리트 방언을 포함해 5개 언어를 단일 가중치로 인식하는 1.6B 크기의 음성 인식 모델이다.
- 원문 : [Introducing Falcon ASR](https://huggingface.co/blog/tiiuae/falcon-asr)

# 그래서 도대체 뭔데 ?
- 아랍어는 표준어(MSA)와 지역 방언의 괴리가 크고, 에미리트 구어 같은 방언은 전사 데이터 자체가 부족함.
- 정제된 방송용 모델은 전화 통화나 일상 대화 음성 인식에서 한계가 큼.
- Falcon-ASR는 에미리트 구어 · 걸프 방언 · MSA · 영어를 함께 학습해 언어 전환이 잦은 일상 발화를 공략함.
- 언어 선택 플래그 없이 5개 언어 음성을 그대로 텍스트로 풀어내며 단어 단위 타임스탬프를 함께 출력함.
	- 💡 WER : 단어 오류율(Word Error Rate). 낮을수록 인식 정확도가 높음.
	- 💡 CER : 문자 단위 오류율(Character Error Rate). 글자 단위 정확도를 볼 때 씀.
	- 💡 단어 단위 타임스탬프 : 인식된 단어마다 음성 내 시작과 끝 위치를 함께 기록하는 기능.

# 어떻게 동작하나 ?
1. 음향 특징 추출과 Whisper 인코더
	- 여러 잡음 환경의 음성 입력을 Whisper 기반 인코더로 전달함.
	- 배경 소음 · 겹치는 음성 · 음악 · 전화선 왜곡 · 잔향 · 속도 및 음조 변화가 섞인 데이터를 처리함.
	→ 열악한 통화 음질에서도 음향 신호의 특징을 보존함.
2. 단일 단계 결합 아키텍처
	- Falcon3-Audio 설계를 바탕으로 인코더와 언어 모델을 결합함.
	- 복잡한 다중 인코더나 별도 커넥터 없이 단일 단계 학습 방식을 적용함.
	→ 별도 커넥터나 복잡한 다단계 파이프라인 없이 음성-언어 정렬을 마침.
3. 무지정 다국어 디코딩
	- 아랍어 · 영어 · 프랑스어 · 스페인어 · 포르투갈어 5개 언어를 단일 모델 가중치로 처리함.
	- 사전에 언어 코드를 넘겨주지 않아도 들리는 언어 그대로 문장을 생성함.
	→ 코드 스위칭이나 일상 대화에서도 언어 플래그 없이 발화된 언어 그대로 텍스트를 출력함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 표준 아랍어 위주라 일상 방언이나 전화 음성에서 인식 오류가 잦았음. 비교군 모델(Qwen3-Omni 30B 등) 대비 가중치 크기도 컸음.
- 이번 방식 : 1.6B의 비교적 작은 파라미터로 단일 가중치 안에 에미리트 방언과 영어를 포함한 5개 언어를 통합함.
→ 방언 음향 데이터와 복합 소음 조건을 함께 학습시켜 일상 발화 환경에 맞췄기 때문임.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| Open Universal Arabic ASR (평균 WER) | Audar-ASR-V1-Turbo : 23.17% | 20.92% (2.25%p 개선) | [ELM 리더보드 스냅샷](https://huggingface.co/blog/tiiuae/falcon-asr) |
| Open Universal Arabic ASR (평균 CER) | Audar-ASR-V1-Turbo : 9.23% | 8.79% | [ELM 리더보드 스냅샷](https://huggingface.co/blog/tiiuae/falcon-asr) |
| 에미리트 방언 내부 평가 (WER) | Qwen3-Omni-30B-A3B-Instruct : 26.80% | 22.73% (4.07%p 개선) | [TII 내부 평가](https://huggingface.co/blog/tiiuae/falcon-asr) |
| 에미리트 방언 내부 평가 (CER) | Qwen3-Omni-30B-A3B-Instruct : 12.72% | 10.19% | [TII 내부 평가](https://huggingface.co/blog/tiiuae/falcon-asr) |
| 영어 7개 테스트셋 평균 (WER) | - | 5.74% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| LibriSpeech clean (WER) | - | 1.75% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| LibriSpeech other (WER) | - | 4.21% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| SPGISpeech (WER) | - | 2.02% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| VoxPopuli (WER) | - | 3.87% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| GigaSpeech (WER) | - | 8.15% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| AMI (WER) | - | 8.33% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |
| Earnings-22 (WER) | - | 11.86% | [HF Open ASR 벤치마크](https://huggingface.co/blog/tiiuae/falcon-asr) |

# 주의할 점 / 한계
- 에미리트 방언 평가의 일부 수치는 비공개 데이터(TII 자체 내부 평가) 기준임. 공개 데이터셋인 Casablanca UAE 서브셋 외에 별도 수집본이 포함됨.
- 아랍어 리더보드 순위 비교는 2026.09.30 시점의 고정 스냅샷 기준임.
- 현재는 [Hugging Face 데모 스페이스](https://huggingface.co/spaces/tiiuae/falcon-asr-demo) 중심이며, API와 네이티브 앱은 계획 단계로 밝혀짐.

# 정리
- 표준 아랍어 대비 전사 데이터가 적었던 에미리트 구어와 방언을 1.6B 단일 가중치로 다국어와 함께 묶었음.
- 언어 플래그 지정 없이 회의나 통화 등 잡음이 섞인 일상 대화 음성을 가볍게 전사하려는 환경에서 활용할 만함.

# 참고
- [Introducing Falcon ASR](https://huggingface.co/blog/tiiuae/falcon-asr) — Hugging Face 블로그
- [Competitive Audio-Language Models with Data-Efficient Single-Stage Training on Public Data](https://arxiv.org/abs/2509.07526) — arXiv 논문
- [Falcon-Emirati: When an LLM Learns the Dialect, the Culture, and the Nuance](https://huggingface.co/blog/tiiuae/falcon-emirati) — Hugging Face 블로그
- [UBC-NLP/Casablanca](https://huggingface.co/datasets/UBC-NLP/Casablanca) — Hugging Face 데이터셋
- [Falcon ASR Demo Space](https://huggingface.co/spaces/tiiuae/falcon-asr-demo) — Hugging Face 데모 스페이스
