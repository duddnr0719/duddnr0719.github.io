---
weight: 155
title: "Holo4 — GUI 조작부터 터미널 코드 실행까지 단일 가중치로 해치우는 컴퓨터 사용 에이전트"
date: 2026-09-28T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 화면 클릭과 셸 명령어 실행을 별개 도구로 나누지 않고 단일 모델 안에서 하나로 묶어 처리하는 오픈 가중치 컴퓨터 사용 에이전트 모델의 등장이다 !

# 개요
- 무엇 : H Company가 2026.09.28에 공개한 컴퓨터 조작 에이전트 모델 'Holo4'
- 한 줄 정의 : Holo4는 화면 조작(GUI), 코드 작성 및 실행, MCP 및 API 호출을 단일 모델로 수행하는 컴퓨터 사용 에이전트(computer-use agent) 모델이다.
- 원문 : [Holo4: powering generalist computer-use agents](https://huggingface.co/blog/Hcompany/holo4)

# 그래서 도대체 뭔데 ?
- 기존 컴퓨터 사용 에이전트 모델들은 화면 캡처만 보며 마우스 클릭 위주로 풀거나, API 및 함수 호출만 다루는 식으로 나뉘어 있었음.
- Holo4는 데스크톱 OS, 웹 브라우저, 안드로이드, 터미널 환경을 단일 모델로 오가며 작업 환경에 맞는 인터페이스를 골라 소프트웨어를 조작함.
- 화면에서 클릭해야 할 요소는 마우스로 누르고, 대량 반복 작업이나 파일 처리는 셸 스크립트를 짜서 바로 실행함.
- 💡 GUI 그라운딩 : 화면 스크린샷 안에서 버튼이나 입력창 같은 인터페이스 요소의 위치 좌표를 짚어내는 작업
- 💡 MCP(Model Context Protocol) : 애플리케이션과 외부 도구 사이의 상태와 호출 규격을 표준화한 연결 프로토콜

# 어떻게 동작하나 ?
1. Agentic Task Factory 기반 합성 환경 및 과제 생성
	- 실제 웹사이트 스크린샷, 제품 설명서, 오픈소스 소프트웨어 문서만으로 인터랙티브 환경을 자동 구성함.
	- 초기 상태에서는 실패하고, 정답 상태에서는 통과하며, 오답은 거절하도록 검증 게이트를 둠.
	- 웹 앱 4000개, MCP 서버 3000개, 데스크톱 OS 3000개 등 약 10000개 태스크를 1개 Docker 이미지로 빌드함.
	→ 모델 훈련에 필요한 10000개 태스크 규모의 인터랙션 궤적 데이터를 확보하게 됨.

2. 127B 토큰 SFT와 2개 전담 RL 전문가 학습
	- 수집한 데이터 중 75%는 Task Factory 성공 궤적(데스크톱 45%, 웹 14%, MCP 및 API 12%, 모바일 3%)으로 채우고 25%는 멀티모달 추론 및 코딩으로 구성해 127B 토큰을 지도 미세조정함.
	- 이후 비동기 온라인 강화학습(RL) 도구인 prime-rl을 써서 2개 전담 LoRA 전문가를 나눔.
	- 1번 전문가는 데스크톱과 웹 환경을 전담하고, 2번 전문가는 터미널과 MCP 및 API 도구 호출을 전담함.
	→ 서로 다른 인터페이스에 특화된 정책을 각각 학습함.

3. 동일 가중치 병합과 하네스 재설계
	- 2개 전문가 LoRA를 추가 학습 없이 동일 가중치로 베이스 SFT 모델에 1개로 병합함.
	- OSWorld 2.0 실행 루프에서 에이전트 실패 원인을 분석해 하네스를 개편함.
	- 데스크톱 머신 내부에서 직접 셸을 실행하고, 메모리 압축 중에도 컨텍스트가 이어지도록 통과 경로를 둠.
	- 코드 실행과 화면 클릭을 단일 도구로 합치고 작업 제한을 200스텝 · 2시간에서 500스텝 · 6시간으로 늘림.
	→ GUI 조작 도중 터미널 명령을 섞어 수백 스텝에 달하는 장기 작업을 중단 없이 수행하게 됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 화면 기반 모델은 API 접근이 막히면 헛돌고, 도구 호출 모델은 그래픽 화면만 있는 소프트웨어를 건드리지 못했음. 화면 조작 도구와 코드 실행 도구가 분리되어 컨텍스트 전환 비용이 컸음.
- 이번 방식 : 단일 모델이 화면 클릭, 셸 스크립트 실행, MCP 도구 호출을 필요에 따라 전환함. 셸 자체에서 데스크톱을 제어하므로 코드와 클릭이 한 흐름으로 이어짐.
→ 환경마다 모델을 갈아 끼울 필요 없이 실제 업무 소프트웨어 파이프라인을 단일 가중치로 끝낼 수 있게 됨.

# 숫자로 보면
| 항목 | 이전 베이스 (Qwen3.8 27B) | 이번 모델 (Holo4-27B) | 출처 |
|---|---|---|---|
| OSWorld 단일 작업 점수 | 84.3% | 85.2% | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| OSWorld 태스크당 비용 | $0.22 | $0.08 | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| OSWorld 2.0 긴 워크플로우 점수 | 48.0% | 61.7% | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| OSWorld 2.0 성공률 | 19.4% | 41.5% | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| OSWorld 2.0 태스크당 비용 | $3.49 | $1.22 | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| AutomationBench (비즈니스 자동화) | 40.3% | 45.4% | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| AutomationBench 태스크당 비용 | $0.09 | $0.05 | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| ALE-CLI (Linux 105개 전문가 작업) | 43.5% | 44.1% | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| AndroidWorld 모바일 제어 | 81.9% | 85.1% | [H Company 뉴스룸](https://hcompany.ai/newsroom/holo4) |
| FreeCAD H 로고 3D 모델링 | 118회 호출 · 1.9M 토큰 | 94회 호출 · 1.5M 토큰 | [Hugging Face 공식 블로그](https://huggingface.co/blog/Hcompany/holo4) |
| Godot 팩맨 게임 구현 소모 토큰 | 197회 호출 · 11.4M 토큰 | 68회 호출 · 2.4M 토큰 | [Hugging Face 공식 블로그](https://huggingface.co/blog/Hcompany/holo4) |

# 주의할 점 / 한계
- 27B 모델의 라이선스 제약 : Holo4-27B 가중치는 비상업용 라이선스(CC BY-NC 4.0)로 공개되어 상업 서비스에 바로 넣을 수 없음.
- 경량 오픈 가중치 모델의 한계 : 상업용 라이선스(Apache 2.0)인 Holo4-35B-A3B(활성 3B)는 OSWorld 2.0 점수가 30.9%로 27B(61.7%) 대비 낮음.
- 프런티어 모델과의 격차 : OSWorld 2.0에서 프런티어 폐쇄형 모델 최고 점수(81.8%) 대비 Holo4-27B(61.7%)는 여전히 격차가 있음.
- 수치의 벤치마크 조건 : OSWorld 2.0과 ALE-CLI는 1회 실행(single run) 측정값이며, AutomationBench는 600개 공개 과제 기준임.
- 아직 확인 안 된 것 : AutomationBench 공식 비공개(private) 셋 채점 결과는 원문에 없음.

# 정리
- GUI 스크린샷과 터미널 셸 도구를 분리하지 않고 단일 모델에 통합해 컴퓨터 작업 성공률(OSWorld 2.0 기준 19.4% → 41.5%)을 끌어올렸음.
- 상업용 구축에는 Apache 2.0인 35B-A3B를, 연구와 고성능 자동화 검증에는 27B를 골라 쓸 수 있음.

# 참고
- [Holo4: powering generalist computer-use agents](https://huggingface.co/blog/Hcompany/holo4) — Hugging Face 공식 블로그
- [Holo4: powering generalist computer-use agents](https://hcompany.ai/newsroom/holo4) — H Company 뉴스룸
- [Hcompany/Holo4-27B](https://huggingface.co/Hcompany/Holo4-27B) — Hugging Face 모델 카드
- [Hcompany/Holo4-35B-A3B](https://huggingface.co/Hcompany/Holo4-35B-A3B) — Hugging Face 모델 카드
- [Hcompany/trajectories](https://huggingface.co/datasets/Hcompany/trajectories) — Hugging Face 평가 궤적 데이터셋
