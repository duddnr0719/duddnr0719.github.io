---
weight: 133
title: "LiquidAI의 오픈 d1 멀티모달 결정 모델 — 생성 없이 바로 판단한다"
date: 2026-10-10T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> LiquidAI가 텍스트 생성 과정 없이 초고속으로 판단을 내리는 엣지용 멀티모달 결정 모델 d1 시리즈를 공개함 !

# 개요
- 무엇 : LiquidAI가 2026.10.07에 멀티모달 오픈 결정 모델 d1-3B와 d1-omni-600M을 공개함.
- 한 줄 정의 : d1은 텍스트를 한 글자씩 생성하지 않고 단 한 번의 추론으로 선택 및 분류를 수행하는 결정 모델(decision model)임.
- 원문 : [Multimodal open d1 decision models for the edge](https://huggingface.co/blog/LiquidAI/open-d1)

# 그래서 도대체 뭔데 ?
- 보통 LLM은 라우팅이나 분류 같은 단순 판단을 할 때도 텍스트 토큰을 생성함.
- 반면 d1 모델은 텍스트 생성 과정(zero output tokens)을 아예 없애고, 주어진 옵션에서 정답을 바로 읽어냄.
- 챗봇처럼 글을 써주는 게 아니라 모더레이션, 의도 분류, 채점, 라우팅 같은 자동화 파이프라인의 중간 평가자로 쓰기 위해 만듦.
	- 💡 결정 모델 : 텍스트 생성 없이, 단일 포워드 패스로 분류, 라우팅, 채점 등의 결정만 내리는 전용 모델.

# 어떻게 동작하나 ?
1. 모달리티 결합
	- 텍스트, 이미지, 음성 데이터를 하나의 컨텍스트로 받음.
	- 일례로 d1-omni-600M(587M)은 공통 뼈대(381M)에 시각(94M)과 청각(112M) 모듈을 각각 연결해 구성함.
	→ 여러 모달리티를 동시에 처리함.
2. 단일 포워드 패스 (Single Forward Pass)
	- 생성형 언어 모델의 디코딩 단계를 거치지 않음.
	→ 정답 텍스트를 파싱하다가 나는 오류가 사라지고 추론 시간이 줄어듦(RTX 4090 기준 8 ms).

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : LLM에게 분류를 맡기면 불필요한 텍스트를 만들거나, 출력 형식이 꼬여서 다시 파싱해야 했음.
- 이번 방식 : 텍스트 생성을 빼버리고 모델의 확률 분포에서 바로 정답 옵션을 뽑음.
→ 구조적으로 출력 오류가 발생하지 않고, 자원이 부족한 엣지 기기에서도 실시간 처리가 가능해짐.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| Decision Index 0.2.1 | 47.11 (Decider 35B-A3B) | 48.57 (d1-3B) | [Liquid AI](https://huggingface.co/blog/LiquidAI/open-d1) |
| 평균 점수 (7개 벤치) | 81.1 (Decider 4B) | 82.9 (d1-3B) | [Liquid AI](https://huggingface.co/blog/LiquidAI/open-d1) |
| Jetson Orin Nano 응답 | - | 50 ms (1 질문) | [Liquid AI](https://huggingface.co/blog/LiquidAI/open-d1) |

- 참고로 d1-omni-600M은 587M 파라미터로 평균 78.4점을 받아, 파라미터가 훨씬 큰 Decider 2B(77.1점)를 이김.
- NVIDIA RTX 4090에서는 질문 1개당 8 ms 만에 결정을 내림.

# 주의할 점 / 한계
- 대화형 챗봇이 아님 : 글이나 코드를 대신 작성해주지 않음.
- 벤치마크 부재 : 비전 평가(Decision Index)는 비공개 상태이고 오디오는 벤치마크가 마땅치 않아 점수를 보고하지 않음.
- 오디오 제약 : d1-omni-600M의 오디오 기능은 아직 초기 연구 단계라 최대 30초의 영어 음성에 대해서만 학습됨.

# 정리
- 무거운 LLM 대신 실시간 에이전트 라우팅이나 모더레이션을 엣지 단에서 처리하려는 개발자가 바로 써볼 만함.

# 참고
- [Multimodal open d1 decision models for the edge](https://huggingface.co/blog/LiquidAI/open-d1) — Liquid AI Blog
- [LiquidAI/d1-3B](https://huggingface.co/LiquidAI/d1-3B) — Hugging Face
- [LiquidAI/d1-omni-600M](https://huggingface.co/LiquidAI/d1-omni-600M) — Hugging Face
