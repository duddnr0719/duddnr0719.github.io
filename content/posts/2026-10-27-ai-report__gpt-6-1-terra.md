---
weight: 169
title: "GPT-6.1 Terra — 데스크톱 조작과 시각 추론을 3배 빠른 속도와 절반 가격으로 실행한다"
date: 2026-10-27T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 데스크톱 화면을 보며 도면을 3D 모델로 바꾸고 인보이스를 입력하는 컴퓨터 조작 작업을 상위 모델 대비 3배 빠른 속도와 이전 세대 대비 50% 낮아진 API 비용으로 해결하는 실무형 모델이 나왔다 !

# 개요
- 무엇 : OpenAI가 2026.10.27 공개한 실무용 컴퓨터 조작 에이전트 모델 'GPT-6.1 Terra'.
- 한 줄 정의 : GPT-6.1 Terra는 정밀한 시각 추론과 데스크톱 도구 사용 능력을 결합해 고반복 실무를 저비용으로 처리하는 업무용 에이전트 모델이다.
- 원문 : [Introducing GPT-6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra)

# 그래서 도대체 뭔데 ?
- OpenAI 모델군 중에서 속도 · 성능 · 비용의 균형을 전면 재조정한 실무 특화 모델임.
- 표준 API 가격은 기존 GPT-5.6 Terra 대비 50% 낮추고, 작업 완료 속도는 상위 모델인 Astra 및 Sol 대비 3배 이상 빠름.
- 회계 프로그램 인보이스 입력, 도면 해석, 영상 편집 지원처럼 화면을 보고 프로그램을 직접 다루는 작업에 맞춰졌음.
- 글쓰기 자연스러움도 개선되어 제안서 초안 작성이나 양식 입력 같은 커뮤니케이션 작업도 함께 처리함.
	- 💡 컴퓨터 유즈 (Computer Use) : 인공지능이 사람처럼 마우스 클릭, 키보드 입력, 화면 캡처 분석을 수행하며 데스크톱 애플리케이션을 조작하는 기능.
	- 💡 reasoning effort : 추론 과정에서 모델이 연산 자원을 얼마나 투입할지 결정하는 설정값 (low, medium, max).

# 어떻게 동작하나 ?
1. 화면 인식과 시각 추론
	- 기술 도면이나 화면 캡처를 읽고 맥락을 분석함.
	- MMMU-Pro 전 구간에서 이전 세대를 넘어서며 상위 모델 수준으로 화면을 파악함.
	→ 복잡한 도면이나 프레임 데이터도 시각적으로 정확히 분해함.

2. 데스크톱 앱과 터미널 제어
	- 화면 좌표와 UI 요소를 바탕으로 다단계 마우스 · 키보드 조작을 실행함.
	- OSWorld 2.1에서 소프트웨어를 직접 다루며, Terminal-Bench 4.0 환경에서 코드 수정과 CLI 명령도 병행함.
	→ 도면을 읽고 3D 모델을 세우거나 웹 레이아웃 버그를 터미널로 잡음.

3. 정렬 제어와 오류 억제
	- 작업 도중 한계나 차단 요소를 숨기지 않고 사용자에게 솔직하게 보고하도록 정렬됨.
	- 외부 프롬프트 인젝션 공격에 저항하며, 오류 유발 프롬프트 환경에서 오류율을 대폭 낮춤.
	→ 작업 범위를 벗어나지 않고 안전하게 작업을 완수함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : GPT-5.6 Terra는 컴퓨터 조작이 가능했으나 오류 유발 프롬프트에서 53.6%(low effort 기준)의 높은 오류율을 보였고, 상위 모델인 Astra나 Sol은 비용과 지연 시간이 컸음.
- 이번 방식 : GPT-6.1 Terra는 오류율을 16.7%(low effort 기준) 및 4.3%(max effort 기준)로 낮췄음. 작업 완료 속도는 Astra 및 Sol 대비 3배 이상 빠르고, 표준 API 비용도 GPT-5.6 Terra 및 GPT-6.1 Sol 대비 50% 낮췄음.
→ 더 적은 토큰으로 작업을 끝내는 높은 토큰 효율과 저렴한 토큰 단가가 결합했기 때문.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 표준 API 입력 가격 (1M 토큰) | - | $1 | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| 표준 API 캐시 입력 가격 (1M 토큰) | - | $0.05 | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| 표준 API 출력 가격 (1M 토큰) | - | $5 | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| API 가격 변동 (vs GPT-5.6 Terra / Sol) | 기준 | 50% 인하 | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| 작업 완료 속도 (vs Astra / Sol) | 기준 | 3배 이상 빠름 | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| Agents' Last Exam 점수 (medium effort) | 기준 (GPT-5.6 Terra) | 15%p 상승 (비용 1/3) | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| 오류 유발 프롬프트 오류율 (low effort) | 53.6% (GPT-5.6 Terra) | 16.7% (37%p 하락) | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| 오류 유발 프롬프트 오류율 (max effort) | - | 4.3% (18%p 하락) | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| Terminal-Bench 4.0 해결률 (max effort) | 21.5% (GPT-5.6 Terra) | 50.3% | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |
| 타사 플래그십 대비 작업당 비용 (max effort) | 기준 | 약 9배 절감 | [OpenAI 공식 블로그](https://openai.com/index/introducing-gpt-6-1-terra) |

# 주의할 점 / 한계
- 최고 난도 코딩 작업의 한계 : 원문에서 직접 밝혔듯, 가장 복잡한 소프트웨어 엔지니어링 작업에서는 여전히 GPT-6.1 Sol이나 GPT-6 Astra가 더 나은 선택지로 남아 있음.
- 평가 환경 차이 : 시스템 카드에 따르면 연구 환경과 API 환경의 평가는 시스템 프롬프트, 가용 도구, reasoning effort 설정에 따라 실제 상용 서비스 출력과 약간 다를 수 있음.
- 수치 측정 조건 : 사실성 및 오류율 수치는 OpenAI 내부의 오류 유발 프롬프트 평가 기준임.
- 아직 확인 안 된 것 : 모델 파라미터 수, 세부 아키텍처, 사전학습 토큰 수 등은 원문에 없음.

# 정리
- 데스크톱 조작과 시각 추론을 묶어 일상적인 반복 업무를 빠르고 저렴하게 위임할 수 있는 실무 모델임.
- 플래그십 모델의 높은 비용이 부담스러웠던 대량 인보이스 처리와 다단계 데스크톱 에이전트 구축팀에게 잘 맞음.

# 참고
- [Introducing GPT-6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra) — OpenAI Blog
- [Addendum to GPT-6 Astra System Card: GPT-6.1 Terra](https://deploymentsafety.openai.com/gpt-6-1-terra) — OpenAI Deployment Safety Hub
