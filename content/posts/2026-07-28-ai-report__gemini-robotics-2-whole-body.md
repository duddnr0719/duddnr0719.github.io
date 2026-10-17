---
weight: 148
title: "Gemini Robotics 2 — 발부터 손끝까지 전신 지능과 도구 추론을 결합한다"
date: 2026-07-28T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 휴머노이드 로봇이 발부터 손끝까지 전신을 조율해 걷고, 쪼그려 앉고, 양손으로 지퍼백을 잠근다 ! 구글 딥마인드가 공개한 피지컬 AI의 두뇌와 운동 제어 모델을 뜯어보자.

# 개요
- 무엇 : Google DeepMind가 2026.07.30 발표한 차세대 피지컬 AI 모델군 (Gemini Robotics 2, Gemini Robotics ER 2, Gemini Robotics On-Device 2)
- 한 줄 정의 : Gemini Robotics 2는 고수준 시공간 추론과 전신 운동 제어를 결합해 휴머노이드와 이종 로봇을 조율하는 로보틱스 파운데이션 모델이다.
- 원문 : [Gemini Robotics 2 brings whole body intelligence to robots](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

# 그래서 도대체 뭔데 ?
- 기존 로봇 AI 모델은 주로 테이블 위에 고정된 로봇 팔 하나로 물건을 집는 상체 작업에 머물러 있었음.
- 이번 Gemini Robotics 2는 발 이동과 중심 유지부터 22 자유도 손가락 조작까지 전신을 제어하는 VLA 모델로 확장했음.
- 여기에 비디오 스트림을 보며 작업 진행도를 판단하고 다중 로봇 협업을 이끄는 추론 에이전트 ER 2를 결합했음.
	- 💡 VLA (Vision-Language-Action) : 카메라 영상과 언어 지시를 받아 관절 모터 제어 신호로 바로 변환하는 모델
	- 💡 Embodied Reasoning (체화 추론) : 로봇이 물리적 세계의 공간 · 시간 · 안전 제약을 이해하고 다단계 작업을 계획하는 고수준 두뇌

# 어떻게 동작하나 ?
1. 고수준 작업 계획 및 모니터링 (Gemini Robotics ER 2)
	- 실시간 비디오 피드와 사람의 자연어 지시를 입력받음
	- Gemini Live API 양방향 스트리밍을 통해 끊김 없이 작업 단계를 계획하고 도구를 호출함
	- 비디오 프레임 단위로 작업 진행 구간과 완료 순간을 감시하고, 사람이 접근하면 안전 정지 명령을 내림
	→ 실시간 환경 변화에 맞춰 작업을 재계획하고 안전을 통제함
2. 전신 운동 제어 실행 (Gemini Robotics 2 VLA)
	- 상위 두뇌가 내린 하위 목표를 받아 로봇의 전신 모터 제어 신호로 변환함
	- 휴머노이드 무게중심을 동적으로 계산해 보행 · 쪼그려 앉기 · 허리 굽히기를 조율함
	- 22 자유도 SharpaWave 손이나 그리퍼로 매듭 묶기, 정밀 부품 삽입 같은 세밀한 접촉 작업을 수행함
	→ 로봇이 넘어지지 않고 균형을 잡으며 이동과 조작을 함께 해냄
3. 온디바이스 로컬 실행 (Gemini Robotics On-Device 2)
	- 네트워크 지연을 없애기 위해 로봇 본체에서 직접 구동되도록 경량화하여 최적화함
	- 모션 트랜스퍼 기법으로 200개 미만 데이터만으로 새로운 로봇 관절 구조에 적응함
	→ 클라우드 연결이 불안정한 환경에서도 로컬 기기 자체 판단으로 기동함

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 상체 중심 제어 (테이블 위 고정형 로봇 팔 위주), 단일 로봇 대상 단기 작업, 고정된 규칙 기반 판단
- 이번 방식 : 전신 통합 제어 (발 이동 + 허리 굽힘 + 손가락 조작), 다중 로봇 협업, 비디오 기반 실시간 진행도 추적
→ 고수준 인지 두뇌(ER)와 저수준 모터 제어(VLA)의 분업 구조를 세우고 양방향 스트리밍을 적용해 멈칫거리는 지연 시간을 줄였기 때문

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 전신 조작 선반 물품 집기 (Apollo + Inspire 손) | - | 76.3% | VLA 모델 페이지 |
| 전신 조작 테이블 물품 집기 (Apollo + Inspire 손) | - | 68.4% | VLA 모델 페이지 |
| 전신 조작 바닥 물품 집기 (Apollo + Inspire 손) | - | 45.7% | VLA 모델 페이지 |
| 다지 정밀 조작 전구 풀기 (Apollo + Sharpa 손, 22 자유도) | - | 92% | VLA 모델 페이지 |
| 다지 정밀 조작 쓰레기봉투 묶기 (Apollo + Sharpa 손, 22 자유도) | - | 44% | VLA 모델 페이지 |
| 다지 정밀 조작 지퍼백 밀봉 (Apollo + Sharpa 손, 22 자유도) | - | 40% | VLA 모델 페이지 |
| 다지 정밀 조작 전구 끼우기 (Apollo + Sharpa 손, 22 자유도) | - | 36% | VLA 모델 페이지 |
| 다지 정밀 조작 쓰레받기 조작 (Apollo + Sharpa 손, 22 자유도) | - | 32% | VLA 모델 페이지 |
| 그리퍼 조작 정밀 부품 삽입 (Franka Duo) | - | 89.6% | VLA 모델 페이지 |
| 그리퍼 조작 공구 키팅 (Franka Duo) | - | 78.9% | VLA 모델 페이지 |
| 그리퍼 조작 일반 집기 및 놓기 (Franka Duo) | - | 74.2% | VLA 모델 페이지 |
| 작업 진행도 5단계 분류 정확도 (ER 2) | - | 57.4% | 개발자 블로그 |
| 작업 완료 순간 포착 정확도 (ER 2) | - | 91.3% (오차 0.96s) | 개발자 블로그 |
| 모델 실행 속도 및 지연 (ER 2) | 대형 비전 모델 대비 | 4x 속도 (sub-second 지연) | 개발자 블로그 |
| 온디바이스 신규 로봇 적응 데이터 | - | 200개 미만 예시 | 공식 블로그 |

# 주의할 점 / 한계
- 원문이 밝힌 이동 속도 한계 : 로봇의 이동 속도(movement speed)는 아직 더 발전해야 할 부분이 남아 있다고 원문에서 직접 밝힘
- 다지 정밀 조작 편차 : 전구 풀기는 92%로 높지만 지퍼백 밀봉(40%), 전구 끼우기(36%), 쓰레받기 조작(32%)처럼 세밀한 다지 손 조작 작업은 성공률이 절반 이하에 머무름
- 바닥 물품 집기의 난이도 : 선반(76.3%)이나 테이블(68.4%)에 비해 바닥 물품 집기는 45.7%로, 무게중심을 크게 낮추고 스쿼트 자세를 유지하는 제어 난도가 여전히 높음
- 배포 및 접근 권한 제한 : 고수준 추론 모델 ER 2는 Google AI Studio 등에서 프리뷰로 열렸으나, 전신 모터 제어를 맡는 VLA와 On-Device 모델은 비공개 파트너 프리뷰 상태임

# 정리
- 고수준 VLM 추론 두뇌(ER 2)와 저수준 전신 VLA 모터 제어를 분리하고 실시간 스트리밍 파이프라인으로 연결했음.
- 테이블 위 로봇 팔에 머물던 제어를 보행과 스쿼트를 결합한 휴머노이드 전신 협응으로 확장하고 태스크별 실측 성공률을 제시함.
- 로봇 하드웨어 제어나 다중 로봇 협업을 다루는 연구자라면 공개된 ER 2 API(Google AI Studio)와 ASIMOV-Agentic 안전 벤치마크를 활용할 수 있음.

# 참고
- [Gemini Robotics 2 brings whole body intelligence to robots](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) — Google DeepMind 공식 블로그
- [Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/) — Google 개발자 블로그
- [Gemini Robotics 2](https://deepmind.google/models/gemini-robotics/vla/) — Google DeepMind 모델 페이지
- [ASIMOV-Agentic Safety Evaluation](https://huggingface.co/datasets/google/asimov_agentic/blob/main/README.md) — Hugging Face 데이터셋
