---
weight: 179
title: "CWE-bench v2 — 185개 취약점 패치와 실행 검증으로 방어 에이전트를 시험한다"
date: 2026-11-05T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 취약점 이름도 알려주지 않는 실제 저장소에서 결함을 찾아 고치고 정상 기능까지 지켜내는지 완전 실행형 코드로 판정하는 사이버 방어 벤치마크다 !

# 개요
- 무엇 : Collinear AI가 2026.11.03에 소프트웨어 보안 취약점 감사 및 패치 벤치마크 CWE-bench v2를 공개함.
- 한 줄 정의 : CWE-bench v2는 실제 오픈소스 코드베이스에서 보안 취약점을 탐지해 수정하고 기존 기능 보존 여부를 결정론적 검증기로 채점하는 방어 특화 에이전트 벤치마크다.
- 원문 : [CWE-bench v2: More coverage, quality, and transparency](https://huggingface.co/blog/cwe-bench)

# 그래서 도대체 뭔데 ?
- 프런티어 AI 모델이 보안 취약점을 찾아내고 스스로 고치는 사이버 방어 능력을 측정함.
- 에이전트에게 CVE 번호나 취약점 위치를 알려주지 않고 실제 오픈소스 저장소와 간단한 지시문만 던져줌.
- 단순히 취약점만 막는다고 통과되지 않으며 기존 소프트웨어의 정상 기능이 그대로 유지되어야만 합격 판정을 받음.
- 공격 코드를 직접 생성하게 하는 레드팀 평가가 아니라 실제 방어자가 마주하는 유지보수 환경을 그대로 재현함.
	- 💡 CWE : 소프트웨어 보안 취약점의 유형을 체계적으로 분류한 표준 목록.
	- 💡 결정론적 검증기 : LLM 판정에 의존하지 않고 실제 공격 입력과 정상 테스트 케이스를 코드로 직접 실행해 결과를 가르는 평가 프로그램.
	- 💡 Harbor : 격리된 도커 환경에서 에이전트를 구동하고 검증기를 실행하는 벤치마크 실행 프레임워크.

# 어떻게 동작하나 ?
1. 도커 환경 배포 및 사전 빌드
	- Harbor 프레임워크가 실제 취약점이 존재하는 오픈소스 저장소를 도커 컨테이너 안에 미리 빌드해 격리함.
	- 외부 의존성 설치 문제로 평가가 중단되지 않도록 필요한 패키지를 컨테이너 내부에 모두 설치해 둠.
	→ 네트워크 문제에 따른 평가 왜곡을 방지함.

2. 에이전트의 코드베이스 탐색 및 패치 수행
	- 에이전트는 결함 위치나 취약점 개수에 대한 힌트 없이 백지상태에서 탐색을 시작함.
	- 태스크당 2 CPUs · 2 GB 메모리 · 4 GB 스토리지 환경에서 3600초 동안 코드를 분석하고 수정을 진행함.
	→ 힌트 없이 실제 보안 감사 작업과 동일한 조건에서 추론하도록 유도함.

3. 엄격한 다중 입력 검증과 이진 보상 산출
	- 패치가 적용된 저장소에 대해 검증기가 공격 입력과 정상 기능 확인 입력을 차례로 주입함.
	- 예를 들어 Rust 이미지 디코더인 blurhash-rs 과제(CVE-2023-42447)에서는 총 8개 입력으로 패치를 시험함.
	- 3개의 문자 경계 입력과 2개의 파싱 값 범위 초과 입력을 주입해 패닉 없이 타입 에러를 반환하는지 확인함.
	- 동시에 3개의 정상 이미지 입력을 넣어 픽셀 출력을 그대로 유지하는지 검증함.
	- 문자 검증만 거친 불완전한 패치는 숫자 경로에서 여전히 패닉을 일으켜 0점 탈락 처리됨.
	- 모든 공격 입력을 막아내고 정상 기능까지 온전히 보존한 패치만 보상 1점을 획득함.
	→ 말만 그럴듯한 껍데기 패치나 소프트웨어 기능을 망가뜨리는 억지 방어를 원천 차단함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : v1에서는 120개 비공개 태스크와 73개 CWE 유형만 다루었고 OWASP Top 10 기준에 맞춰 분류했음. 게다가 평가 프레임워크가 닫혀 있어 외부 연구자가 직접 실행하거나 재현하기 어려웠음.
- 이번 방식 : v2는 100개 공개 태스크와 150개 비공개 태스크로 총 250개 태스크를 지원하며 CWE 유형을 185개로 확장함. 분류 체계도 10개 독자 약점 클래스로 개편하고 Hugging Face 레포에서 Harbor 명령 한 줄로 재현할 수 있게 개방함.
→ 실제 오픈소스 결함은 특정 웹 취약점에 국한되지 않으므로 광범위한 취약점 유형과 엄격한 기능 보존 검증이 결합되어야 실전 방어력을 판정할 수 있기 때문임.

# 숫자로 보면
| 항목 | v1 (이전) | v2 (이번) | 출처 |
|---|---|---|---|
| 전체 태스크 수 | 120개 (전부 비공개) | 250개 (공개 100개 + 비공개 150개) | [src: https://cwe-bench.com/] |
| 다루는 CWE 유형 수 | 73개 | 185개 (공개 세트 91개) | [src: https://cwe-bench.com/] |
| 취약점 분류 체계 | OWASP Top 10 (2025) | 독자 10개 약점 클래스 (K01 ~ K10) | [src: https://cwe-bench.com/] |
| 채점 및 검증 방식 | 결정론적 게이트 + 3인 판정단 | 판정단으로 다듬은 결정론적 검증기 단독 | [src: https://cwe-bench.com/] |
| 일반 공개 및 재현 | 비공개 (기관 전용) | 100개 세트 및 하네스 완전 공개 | [src: https://huggingface.co/blog/cwe-bench] |
| 태스크당 실행 자원 | 원문에 없음 | 2 CPUs · 2 GB 메모리 · 4 GB 스토리지 | [src: https://huggingface.co/datasets/collinear-ai/cwe-bench] |
| 태스크당 에이전트 제한 시간 | 원문에 없음 | 3600초 (1시간) | [src: https://huggingface.co/datasets/collinear-ai/cwe-bench] |

모델별 평가 결과 (전체 250개 태스크 기준, 4회 시도 평균) :
| 순위 | 모델 | 실행 하네스 | pass@1 | pass@4 | 롤아웃당 평균 비용 | 출처 |
|---|---|---|---|---|---|---|
| 1 | Claude Opus v5.5 | Claude Code | 67.1% | 79.2% | $1.85 | [src: https://cwe-bench.com/] |
| 2 | Muse Wonder | opencode | 66.1% | 78.8% | $2.73 | [src: https://cwe-bench.com/] |
| 3 | Gemini 4 Argon | Antigravity | 65.0% | 77.2% | $3.70 | [src: https://cwe-bench.com/] |
| 4 | GPT-6 Astra | Codex | 64.2% | 72.8% | $3.87 | [src: https://cwe-bench.com/] |
| 5 | DeepSeek-V4.1-Flash (1017) | opencode | 57.6% | 73.6% | $0.04 | [src: https://cwe-bench.com/] |
| 6 | Grok 4.7 | opencode | 54.7% | 71.2% | $2.97 | [src: https://cwe-bench.com/] |
| 7 | Hy4 Preview | opencode | 47.3% | 64.4% | $0.43 | [src: https://cwe-bench.com/] |
| 8 | Mistral Large 4 | opencode | 45.6% | 60.4% | $0.37 | [src: https://cwe-bench.com/] |
| 9 | Qwen3.8-Max (0902) | opencode | 45.4% | 64.8% | $2.06 | [src: https://cwe-bench.com/] |
| 10 | Kimi K3.1 Pro | opencode | 45.3% | 64.0% | $0.96 | [src: https://cwe-bench.com/] |
| 11 | GLM-5.3 | opencode | 42.0% | 63.6% | $0.58 | [src: https://cwe-bench.com/] |

- 전체 250개 태스크 기준 파레토 프론티어에서 46배 비용($0.04 → $1.85)을 지불해도 통과율 증가는 1.16배(57.6% → 67.1%)에 그침. [src: https://cwe-bench.com/]

공개 100개 태스크 기준 주요 지표 :
- 평가 대상 11개 모델 중 Gemini 4 Argon이 pass@1 67.8%, pass@4 81.0% ($3.92)로 1위를 기록함. [src: https://huggingface.co/blog/cwe-bench]
- Claude Opus v5.5는 pass@1 67.3%, pass@4 78.0% ($1.83)로 뒤를 바짝 쫓음. [src: https://huggingface.co/blog/cwe-bench]
- DeepSeek-V4.1-Flash (1017)는 롤아웃당 $0.04의 저렴한 비용으로 pass@1 57.0%를 달성함. [src: https://huggingface.co/blog/cwe-bench]

# 주의할 점 / 한계
- 상위권 모델도 여전히 한계가 뚜렷함 : 전체 250개 중 20개 태스크는 11개 모델 전원이 한 번도 해결하지 못했음. 공개 100개 세트에서도 선두 모델이 19%의 과제에서 4회 시도 모두 실패함.
- 언어별 격차가 큼 : Rust(최고 87%)와 C/C++(최고 75%) 패치 성공률은 높은 반면 Java(최고 63%)와 Python(최고 59%)은 저조함.
- 취약점 클래스별 편차 : 신뢰 경계(K07 · 최고 58%) · 인증(K05 · 최고 60%) · 오류 처리(K10) 클래스에서 모델들이 일관되게 취약점을 보임.
- 단일 취약점 격리 평가의 한계 : 각 태스크는 저장소당 단 1개의 보안 결함만 패치하도록 설계됨. 복합적인 취약점이 얽혀 있는 실전 저장소 감사 능력까지 대변하지는 못함.
- 하드웨어 및 런타임 제약 : 태스크당 2 CPUs · 2 GB 메모리 · 4 GB 스토리지 환경에서 3600초 동안 수행됨.
- 훈련 데이터 분리 및 비공개 세트 : 사전에 보지 못한 태스크의 진척 추적을 위해 150개 세트는 비공개로 유지되며, 평가 태스크는 별도 제공되는 4000개 이상의 훈련 코퍼스에 포함되지 않음.

# 정리
- CWE-bench v2는 단순 탐지나 공격 생성을 넘어 취약점을 고치고 기존 기능까지 지켜내는 소프트웨어 방어력을 시험함.
- 오픈소스 저장소 기반의 자율 엔지니어링 에이전트를 구축하거나 보안 패치 자동화 파이프라인을 검증하려는 엔지니어에게 실질적인 평가 기준이 됨.

# 참고
- [CWE-bench v2: More coverage, quality, and transparency](https://huggingface.co/blog/cwe-bench) — Hugging Face Blog
- [collinear-ai/cwe-bench](https://huggingface.co/datasets/collinear-ai/cwe-bench) — Hugging Face Datasets
- [CWE-bench Leaderboard](https://huggingface.co/spaces/collinear-ai/cwe-bench-leaderboard) — Hugging Face Spaces
- [CWE-bench: cybersecurity benchmark](https://cwe-bench.com/) — Collinear AI 공식 웹사이트
- [CWE-bench: Refocusing Agentic Security from Exploitation to Defense](https://arxiv.org/abs/2610.17020) — arXiv 논문
