---
weight: 202
title: "NVIDIA SimReady 로봇 시뮬레이션 — 사전 검증된 OpenUSD 자산과 에이전트로 픽앤플레이스를 구축한다"
date: 2026-11-18T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 물리 속성과 관절 검증을 마친 OpenUSD 3D 자산을 Hugging Face에서 바로 내려받아 AI 에이전트로 로봇 픽앤플레이스 시뮬레이션을 조립하고 실행하는 워크플로를 뜯어보자 !

# 개요
- 무엇 : NVIDIA가 2026.11.13 Hugging Face 공식 블로그에 SimReady Central 오픈 자산과 프런티어 AI 에이전트를 결합해 Isaac Sim 6.2에서 로봇 픽앤플레이스 시뮬레이션을 구축하는 기술 가이드를 공개함.
- 한 줄 정의 : SimReady 기반 로봇 픽앤플레이스 워크플로는 충돌 기하 · 질량 · 관절 드라이브 속성이 사전 검증된 OpenUSD 자산을 조합해 수동 물리 설정 없이 시뮬레이션 장면과 제어 코드를 바로 구동하는 파이프라인이다.
- 원문 : [Build a Robot Pick-and-Place Simulation with SimReady Assets](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place)

# 그래서 도대체 뭔데 ?
- 3D CAD 모델만 시뮬레이터에 불러오면 겉모습은 멀쩡해도 물리 속성이 빠져 있어 그리퍼가 물체를 그냥 통과하거나 관절이 의도대로 움직이지 않는 문제가 생김.
- NVIDIA는 Hugging Face에 공개한 2,000개 이상의 오픈 자산 라이브러리인 SimReady Central에서 사전 검증된 OpenUSD 자산인 로봇 팔(UR17G) · 그리퍼(Robotiq 2F-140) · 음료 캔을 가져와 조립하는 SimReady 워크플로를 제시함.
	- 💡 OpenUSD : 3D 장면의 기하 구조 · 조립 계층 · 재질 · 물리 시뮬레이션 속성을 하나의 공통 포맷으로 기술하고 합성하는 오픈 프레임워크다.
	- 💡 SimReady (Simulation-Ready) : 단순 3D 형상을 넘어 충돌 기하 · 질량 · 마찰 · 관절 한계 · 드라이브 설정까지 특정 시뮬레이션 용도에 맞게 준비하고 검증을 마친 OpenUSD 자산을 뜻한다.
- 여기에 Isaac Sim 6.2의 원격 Python 서버와 에이전트 스킬(Agent Skills)을 연결해, GPT-6 Sol 같은 프런티어 AI 모델이 자연어 지시만으로 로봇 팔과 그리퍼를 하나의 아티큘레이션으로 묶고 픽앤플레이스 제어 코드를 작성해 실행함.
	- 💡 아티큘레이션 (Articulation) : 여러 강체(링크)와 물리 관절로 이루어진 로봇 기구학을 물리 엔진이 단일 다물체 시스템으로 묶어 통합 제어하는 구조다.

# 어떻게 동작하나 ?
1. SimReady Foundation 3단계 규격 기반의 자산 검증 확인
	- SimReady Foundation은 시뮬레이션 용도별 기능 묶음인 프로파일(Profile) · 개별 역량인 기능(Features) · 세부 설정 검사 규칙인 요구사항(Requirements)의 3단계로 자산 품질을 정의함.
	- 이번 워크플로에 쓰인 Universal Robots의 UR17G 팔은 `Robot-Body 4.0.0` 프로파일을, Robotiq 2F-140 그리퍼는 `Robot-Gripper 3.0.0` 프로파일 검증을 통과한 상태로 배포됨.
	- 두 자산 모두 PhysX 구동 관절 계약인 `FET_022_PHYSX`의 8개 요구사항 규칙(`DJ.001` ~ `DJ.007` 및 `DJ.011`)을 통과해 관절 상태 API · 드라이브 및 미믹(mimic) API · 최대 속도 · 드라이브 설정값 · 아티큘레이션 루프 부재 등이 사전 보증됨.
	→ 개발자가 CAD 파일에서 링크별 질량이나 관성 텐서를 일일이 추정하고 디버깅할 필요 없이 물리 동작이 보장된 기준선 위에서 작업을 시작하게 됨.

2. 자산 다운로드 및 Isaac Sim 원격 에이전트 연결 (Step 1 ~ Step 2)
	- SimReady Central 또는 자연어 기반 USD Search 엔드포인트에서 UR17G 로봇 팔 · Robotiq 2F-140 그리퍼 · 음료 캔(`food_beverage_can_n01`) 3종의 패키지 폴더 전체를 로컬에 내려받음.
	- `./isaac-sim.sh --enable isaacsim.code_editor.python_server` 명령으로 원격 Python 서버를 활성화해 Isaac Sim 6.2를 실행하고, 같은 디렉터리에서 에이전트(예제에서는 GPT-6 Sol)를 띄워 내장 스킬을 로드함.
	- 에이전트에게 팔과 그리퍼의 로컬 USD 경로를 넘기면 `isaac-sim-remote`와 `usd-articulation` 스킬을 호출해 두 자산을 단일 아티큘레이션으로 조립함. 픽앤플레이스 실행 전에는 에이전트 또는 GUI로 ① 팔 · 그리퍼의 관절 한계와 드라이브 설정, ② 팔의 소폭 이동 및 그리퍼 개폐 동작, ③ 음료 캔이 작업대를 뚫고 떨어지지 않는 바닥 접촉의 3가지를 점검함.
	→ GUI에서 수작업으로 관절 계층을 잇지 않아도 에이전트가 Python API를 통해 실시간으로 시뮬레이터 장면을 조작하고 물리 결합 상태를 확인함.

3. 접촉 기반 파지 제어 생성 및 6단계 픽앤플레이스 실행 (Step 3)
	- 조립이 끝난 뒤 에이전트에게 음료 캔 USD 경로와 함께 접촉 기반 파지(contact-based grasp) 및 위치 오차 검증을 지시하면 `isaac-sim-remote` · `manipulation-ik` · `physics-simulation` 스킬이 작동함.
	- 제어기는 접근(approach) → 파지(grasp) → 들어올리기(lift) → 유지(hold) → 이동(transfer) → 놓기(release)로 이어지는 6단계 시퀀스를 수행함.
	- 수평 파지 구간에서는 시뮬레이션 테스트로 고른 2N·m 드라이브 토크 상한(drive-effort cap)으로 그리퍼를 닫고, 팔이 고정된 웨이포인트를 따라 이동하는 동안 접촉과 마찰력으로 캔을 유지해 목표 지점에 내려놓음.
	→ 개별 자산 단위의 정적 검증을 넘어 팔 · 그리퍼 · 캔 · 제어기가 한 장면 안에서 맞물려 돌아가는 전체 물리 상호작용을 끝단까지 확인하게 됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 원본 CAD(`STEP` 파일)에서 출발해 OpenUSD 변환 · 레퍼런스 사진 기반 재질 매칭 · URDF 참조 및 부피 기반 질량 정규화 · SimReady 규격 검증 · 태스크 실행까지 5단계를 매번 거쳐야 했음 (ABB YuMi 양팔 로봇 예제 기준 21개 강체와 팔당 7개 회전 관절 및 그리퍼 슬라이드 2개를 직접 설정하고 본체 38kg · 그리퍼 0.28kg 질량 및 마찰계수 0.8 / 0.6, 반발계수 0을 수동 가정해야 했음).
- 이번 방식 : OEM과 공급사가 SimReady Foundation 프로파일에 맞춰 사전 검증해 SimReady Central에 올려둔 2,000개 이상의 오픈 자산을 그대로 가져와 쓰므로, 앞단의 자산 변환과 단품 물리 설정 과정을 건너뛰고 다운로드 → 로봇 조립 → 픽앤플레이스 제어 실행의 3단계로 압축됨.
→ 로봇 부품마다 반복되던 물리 파라미터 추정과 단품 검증 과정이 사전 검증된 오픈 자산과 에이전트 스킬 조합으로 대체되어 전체 준비 단계가 5단계에서 3단계로 줄어듦.

# 숫자로 보면
| 항목 | 이전 (원본 CAD 기반 YuMi 자체 변환 워크플로) | 이번 (SimReady Central 자산 재사용 워크플로) | 출처 |
|---|---|---|---|
| 워크플로 단계 수 | 5단계 (STEP 변환 → 외형 매칭 → 물리 설정 → 규격 검증 → 태스크 실행) | 3단계 (자산 다운로드 → 에이전트 조립 · 검증 → 제어 및 픽앤플레이스 실행) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Blog](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) |
| 사용 로봇 및 그리퍼 구성 | ABB YuMi 양팔 로봇 (팔당 회전 관절 7개 · 그리퍼 손가락 2개 · 강체 21개) | Universal Robots UR17G 팔 + Robotiq 2F-140 그리퍼 + 음료 캔 (총 3종 자산) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Blog](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) |
| 질량 · 물리 파라미터 준비 | 부피 추정 후 본체 38kg · 그리퍼 0.28kg 정규화 및 마찰계수 0.8(정지) / 0.6(운동) · 반발계수 0 직접 설정 | 자산 내 충돌 기하 · 질량 · 관절 드라이브 사전 포함 (`Robot-Body 4.0.0`, `Robot-Gripper 3.0.0` 검증 완료) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Blog](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) |
| 구동 관절 규격 검사 (`FET_022_PHYSX`) | 변환 후 에이전트로 SimReady 요구사항 사후 검증 수행 | 배포 전 8개 요구사항 규칙(`DJ.001` ~ `DJ.007`, `DJ.011`) 통과 리포트 제공 (런타임 벤치마크 9개 테스트 항목 별도 정의) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Blog](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place), [SimReady Foundation Docs](https://nvidia.github.io/simready-foundation/latest/features/FET_022_PHYSX.html) |
| 시뮬레이터 및 보조 에이전트 모델 | Isaac Sim 6.1 + GPT-6 Astra (Codex CLI 연동) | Isaac Sim 6.2 + GPT-6 Sol (원격 Python 서버 및 내장 스킬 연동) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Blog](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) |
| 픽앤플레이스 실증 조건 | 45mm · 40g 큐브 (122.2초 동안 4회 사이클, 2초 유지) 및 140mm · 10g 마커 파지 | 고정 작업대 위 음료 캔 수평 파지 (드라이브 토크 상한 2N·m, 6단계 시퀀스, 4배속 데모 공개) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Blog](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) |
| 오픈 라이브러리 재사용 풀 | 개별 STEP 파일 및 레퍼런스 이미지 · 영상 수동 확보 | SimReady Central 오픈 자산 2,000개 이상 (Palatial 협력 NVIDIA Robotics 1K 데이터셋 1,000개 포함) | [NVIDIA Technical Blog](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/), [HF Announcement Blog](https://huggingface.co/blog/nvidia/simready-central-assets-robotics-ai-factories) |

# 주의할 점 / 한계
- 고정된 작업대 환경과 강체 가정 : UR17G 픽앤플레이스 예제는 바닥에 고정된 로봇과 캔의 초기 위치가 정해진 평평한 작업대에서 수행됐음. 카메라 비전 인식을 쓰지 않았고 충돌 검사도 제한적이며, 캔의 찌그러짐이나 내부 액체 흔들림을 모델링하지 않아 과도한 파지력에 의한 파손 여부는 확인하지 못함.
- 수치 및 제어 조건의 한계 : 수평 파지에 쓰인 2N·m 드라이브 토크 상한은 제조사 권장치나 실제 손가락 끝 힘에 보정된 값이 아니라 시뮬레이션 테스트로 고른 수치이며, 팔 이동 역시 실시간 경로 재계획 없이 고정된 웨이포인트를 따름 (이전 YuMi 워크플로의 질량 분포 · 마찰계수 0.8 / 0.6 역시 실물 로봇 계측값과 보정되지 않은 추정치임). 따라서 물체 위치가 달라지거나 다른 무게의 물체를 다룰 때 및 실제 하드웨어 환경에서의 동작까지는 보장하지 않음.
- 에이전트 생성 코드 편차 : 사용하는 프런티어 AI 모델이나 추론 설정 · 프롬프트에 따라 생성되는 제어 코드와 시뮬레이션 결과가 달라질 수 있어 실행 전 코드와 동작을 직접 확인해야 함.
- 아직 확인 안 된 것 : UR17G + Robotiq 2F-140 픽앤플레이스 실행 시 최종 목표 지점에서의 구체적인 배치 위치 오차(mm)와 반복 시도 성공률(%) 수치는 원문에 없음.

# 정리
- SimReady Central에 공개된 2,000개 이상의 사전 검증 OpenUSD 자산과 Isaac Sim 6.2의 에이전트 스킬을 결합해, 단품 물리 · 관절 설정 단계를 건너뛰고 3단계 만에 로봇 조립부터 접촉 기반 픽앤플레이스 시뮬레이션까지 구동하는 방법을 보여줌.
- 상용 로봇 팔과 그리퍼를 조합해 픽앤플레이스 작업을 구성하거나, 프런티어 AI 에이전트로 로봇 작업장(Workcell) · 학습 및 평가 환경 · AI 팩토리 디지털 트윈을 구축하려는 로보틱스 및 시뮬레이션 개발자가 시작점으로 삼기 좋음.

# 참고
- [Build a Robot Pick-and-Place Simulation with SimReady Assets](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) — Hugging Face Blog (NVIDIA)
- [Announcing SimReady Central: An Open Library of Simulation-Ready 3D Assets for Robotics and AI Factories](https://huggingface.co/blog/nvidia/simready-central-assets-robotics-ai-factories) — Hugging Face Blog (NVIDIA)
- [5 Steps to Create SimReady Assets for Robotics with Frontier AI Models](https://developer.nvidia.com/blog/5-steps-to-create-simready-assets-for-robotics-with-frontier-ai-models/) — NVIDIA Technical Blog
- [Feature: FET_022_PHYSX — Content Capabilities](https://nvidia.github.io/simready-foundation/latest/features/FET_022_PHYSX.html) — NVIDIA SimReady Foundation Documentation
