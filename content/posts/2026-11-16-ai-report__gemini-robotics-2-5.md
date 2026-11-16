---
weight: 200
title: "Gemini Robotics 2.5 — 시뮬레이션 가속과 실시간 안전 조향으로 공장 키팅 96%를 달성한다"
date: 2026-11-16T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 200개 이상의 조작 과업에서 성공률을 30% ~ 100% 높이고, 실제 자동차 생산 라인 부품 키팅 파일럿에서 96% 성공률을 기록한 Google DeepMind의 로봇 제어 VLA 모델 !

# 개요
- 무엇 : Google DeepMind가 2026.11.10에 로봇 제어용 시각 · 언어 · 행동(VLA) 모델인 Gemini Robotics 2.5와 물리 안전 벤치마크 ASIMOV-Jailbreak를 공개함.
- 한 줄 정의 : Gemini Robotics 2.5는 Gemini 4 Argon의 시뮬레이션 가속을 바탕으로 테이블탑 양팔 그리퍼부터 22자유도 5손가락 손과 전신 휴머노이드까지 제어하며 실시간 추론 안전 가이던스를 갖춘 로봇 행동(VLA) 모델이다.
- 원문 : [Gemini Robotics 2.5 accelerates real-world general dexterity](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/)

# 그래서 도대체 뭔데 ?
- 실제 환경은 비정형적이고 예측하기 어려워 기존 로봇 제어 모델이 변화에 적응하며 일상 물체를 정밀하고 신뢰성 있게 다루기 힘들었고, 복잡한 작업 공간에서 물리적 안전도 확보해야 했음.
- 또한 로봇에게 새로운 기술을 가르치려면 대규모 물리 데이터와 고효율 모델링 알고리즘이 필요해 학습 속도에 병목이 있었음.
- 시각 · 언어 · 행동(VLA) 모델인 Gemini Robotics 2.5는 Gemini 4 Argon을 시뮬레이션 엔진(Real2Sim)으로 삼아 카메라 장면에서 수천 개의 연습 에피소드를 생성하고 실시간 추론 안전 가이던스를 결합해, 200개 이상의 정밀 과업과 실제 공장의 자동차 키팅(Automotive Kitting) 공정까지 수행함.
	- 💡 VLA (Vision-Language-Action) : 카메라 영상과 텍스트 지시를 입력받아 로봇 관절 · 그리퍼의 제어 명령을 직접 출력하는 멀티모달 모델.
	- 💡 Real2Sim (Real-to-Simulation) : 로봇 카메라 영상 · 1인칭 인간 영상 · 손그림 스케치로부터 물리 법칙이 보정된 3D 시뮬레이션 환경(디지털 트윈)을 재구성하는 기법.
	- 💡 자동차 키팅 (Automotive Kitting) : 조립 라인의 각 차량 순서에 맞춰 벌크 부품함에서 개별 부품을 골라 지정된 트레이에 정렬해 담는 공정.

# 어떻게 동작하나 ?
1. 체화 추론 모델(ER)과 행동 모델(VLA)의 분업 제어
	- 상위 추론 모델인 Gemini Robotics ER이 다단계 작업 흐름을 추적하고 주변 환경 변화에 맞춰 추론함.
	- 하위 행동 모델인 Gemini Robotics 2.5가 2손가락 평행 그리퍼(Franka Duo / FR3)부터 5손가락 22자유도(22-DoF) 손과 76자유도(76-DoF) 전신을 갖춘 휴머노이드(Apptronik Apollo 2)까지 제어하며 전신 무게중심 균형을 잡음.
	- Mercedes-Benz 생산 라인 키팅 파일럿에서는 공급함의 금속 자동차 브래킷을 집어 트레이의 빈 공간을 보정하며 순서대로 담고, 정교한 도구 사용 · 변형 물체 조작 · 섬세한 물체 처리를 결합해 집게로 음식 서빙하기 · 선물 상자 리본 묶기 · 액체 피펫팅 등 200개 이상의 개별 과업을 수행함.
	→ 단일 로봇 형태에 묶이지 않고 테이블탑 로봇 팔부터 전신 휴머노이드까지 동일한 지능으로 구동하게 됨.
2. Gemini 4 Argon을 활용한 Real2Sim 합성 데이터 확장과 사후 라벨링
	- 실제 작업대 RGB 사진 1장이나 원격조작 기록, 1인칭 인간 영상에서 조작 대상 물체의 3D 메쉬와 MuJoCo 충돌 구조를 복원해 디지털 트윈을 구축함.
	- 로봇 원격조작 에피소드를 시뮬레이션 카메라 시점 및 손끝 촉각 센서 힘 · 토크에 맞출 때는 팔 관절 0.55rad · 손 관절 0.65rad 범위 안에서 오프라인 명령을 보정하고, 1인칭 인간 영상은 76자유도 휴머노이드 관절로 리타겟팅해 500Hz 물리 엔진에서 검증함.
	- 구축된 시뮬레이션에서 ±10cm 위치 무작위화를 적용해 4,500개 이상의 에피소드를 자동 수집해 VLA를 미세조정하고, 136초 분량의 종이접기 영상 같은 시연 데이터는 4단계 계층(전체 목표 1개 · 서브태스크 6개 · 3 ~ 15초 접촉 프리미티브 17개 · 미끄러짐 및 재시도 구간 가중치 0.15x ~ 0.25x 하향)으로 정제함.
	→ 실제 시연 데이터에 수천 개의 시뮬레이션 연습 에피소드와 영상 기반 실패 원인 진단이 더해져 새로운 물체와 환경에 빠르게 일반화함.
3. 실시간 추론 안전 가이던스(Inference-time Reasoning Guidance)와 적대적 방어
	- 텍스트 생성 모델의 안전 분류기처럼 로봇이 움직이는 동안 추론 시점 가이던스가 개입해 물리적 장애물과 주변 사람을 실시간으로 피해 궤적을 조향함.
	- 양팔 테이블탑 유해 · 무해 조작 쌍(암묵적 안전 200개 · 명시적 안전 정책 155개)과 다단계 대화 · 도구 호출 기반 적대적 탈옥(최대 10스텝, 15개 공격 전략 그룹, 845개 에피소드)으로 구성된 ASIMOV-Jailbreak 벤치마크 및 41개 기준의 물리 안전 루브릭(Rubric v2)으로 안전성을 검증함.
	→ 장애물이나 사람이 있는 환경에서 안전 과업 완료율을 높이고, 다단계 대화로 위장된 유해 명령에 대한 탈옥 저항성을 확보함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 새로운 기술을 가르칠 때마다 대규모 물리 데이터와 고효율 모델링 알고리즘을 직접 확보해야 했고, 다단계 적대적 프롬프트에 대한 탈옥 저항성도 이전 베이스라인인 Gemini Robotics ER 2 기준 82%였음.
- 이번 방식 : Gemini 4 Argon이 시뮬레이션 디지털 트윈 생성 · 실패 원인 영상 가설화 및 테스트 · 사후 데이터 가중치 조정을 수행해 개발을 가속하고(탈옥 저항성 99.5%), Gemini Robotics 2.5는 실시간 추론 안전 가이던스로 장애물 및 주변 사람 근처 안전 과업 완료율을 높임.
→ 실제 시연 데이터에 Argon의 시뮬레이션 연습 에피소드 생성과 실패 원인 진단 · 개선 테스트가 결합되면서 이전 베이스라인 대비 과업 성공률은 30% ~ 100% 향상되고 수행 시간은 20% ~ 30% 단축됨.

# 숫자로 보면
| 항목 | 이전 / 비교 기준 | 이번 (Gemini Robotics 2.5 / Argon) | 출처 |
|---|---|---|---|
| 200개 이상 조작 과업 성공률 | 이전 베이스라인 | 과업별 30% ~ 100% 향상 (Gemini Robotics 2.5) | DeepMind Blog |
| 200개 이상 조작 과업 완료 속도 | 이전 베이스라인 | 20% ~ 30% 단축 (Gemini Robotics 2.5) | DeepMind Blog |
| 실제 자동차 생산 라인 부품 키팅 성공률 | 단독 실증 (Mercedes-Benz 생산 라인 PoC 파일럿) | 96% (Apollo 2 + Gemini Robotics 2.5) | DeepMind Blog |
| 장애물 주변 안전 과업 완료율 | 추론 가이던스 미적용 | 33% 향상 (Gemini Robotics 2.5) | DeepMind Blog |
| 주변 사람 근처 안전 과업 완료율 | 추론 가이던스 미적용 | 43% 향상 (Gemini Robotics 2.5) | DeepMind Blog |
| ASIMOV-Jailbreak 탈옥 저항성 | 82% (Gemini Robotics ER 2) | 99.5% (Gemini 4 Argon) | DeepMind Blog |
| ERQA 3D 공간 · 물리 추론 점수 | 기존 프런티어 모델 | 87% (Gemini 4 Argon 순수 추론) | Google Developers Blog |
| Real2Sim 4,500개 이상 에피소드 미세조정 효과 | 성공률 56% / 완료 시간 35초 | 성공률 75% / 완료 시간 24초 (77개 과업) | Google Developers Blog |
| 하드웨어 픽앤플레이스 자기 개선 (SO-101) | 1회차 58.9초 (2회차 22.9초) | 3회차 17.4초 (정중앙 안착) | Google Developers Blog |

# 주의할 점 / 한계
- 파트너 우선 배포 및 모델별 접근 경로 : Gemini Robotics 2.5는 현재 Apptronik · Agile · Mercedes-Benz 등 로보틱스 파트너사에 우선 배포 중이며 일반 사용자는 대기자 명단(waitlist)을 신청해야 함. 반면 시뮬레이션 · 추론에 쓰인 Gemini 4 Argon(`gemini-4-argon`)은 Google AI Studio · Gemini API · Google Antigravity에서 바로 사용할 수 있음.
- 실제 공장 수치의 범위 : Mercedes-Benz 헝가리 Kecskemét 및 독일 Sindelfingen 공장에서 기록한 96% 성공률은 금속 브래킷 부품을 트레이에 정렬하는 키팅(kitting) 개념 증명(PoC) 파일럿 결과임.
- 오픈소스 공개 범위와 조건 : ASIMOV-Jailbreak 평가 하네스와 데이터셋(`google/asimov_agentic`)은 MIT 라이선스로 Hugging Face에 공개되었으나, 다운로드 시 이용 조건 동의 및 Git LFS 설치가 필요하며 Gemini Robotics 2.5 모델 가중치는 포함되지 않음.
- 아직 확인 안 된 것 : Gemini Robotics 2.5의 파라미터 규모, 온보드 제어 추론 지연 시간, 전체 사전학습 데이터 용량은 원문에 없음.

# 정리
- Gemini Robotics 2.5는 Gemini 4 Argon 기반 시뮬레이션 데이터 생성과 실시간 추론 안전 가이던스를 결합해 실험실 밖 비정형 환경으로 적용 범위를 넓히며, 200개 이상 과업에서 성공률을 30% ~ 100% 높이고(완료 속도 20% ~ 30% 단축) Mercedes-Benz 생산 라인 부품 키팅 파일럿에서 96% 성공률을 기록한 릴리스임.
- 로봇 학습 파이프라인에서 물리 데이터 부족 병목을 겪거나 MuJoCo 기반 Real2Sim 자동화 및 물리 안전 · 적대적 탈옥 평가(`google/asimov_agentic`)를 구축하려는 로보틱스 연구자가 참고할 만함.

# 참고
- [Gemini Robotics 2.5 accelerates real-world general dexterity](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/) — Google DeepMind Blog
- [google/asimov_agentic · Datasets at Hugging Face](https://huggingface.co/datasets/google/asimov_agentic) — Hugging Face
- [Gemini 4 Argon for Robotics](https://developers.googleblog.com/gemini-4-argon-for-robotics/) — Google Developers Blog
- [Gemini Robotics 2.5 Model Page](https://deepmind.google/models/gemini-robotics/vla/) — Google DeepMind
