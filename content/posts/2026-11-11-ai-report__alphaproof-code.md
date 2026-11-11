---
weight: 186
title: "AlphaProof Code — 650만 줄 Lean 증명으로 Signal 암호화 기계어를 4주 만에 검증한다"
date: 2026-11-11T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 전문가의 명세 검토와 자율 에이전트 팀의 650만 줄 Lean 증명을 결합해, 배포된 Signal 암호화 바이너리를 기계어 수준에서 4주 만에 정형 검증한 프레임워크 !

# 개요
- 무엇 : Google DeepMind · Google이 2026.11.10에 공개한 다중 에이전트 정형 검증 프레임워크 `AlphaProof Code`와 Signal 프로토콜(`libsignal`) 기계어 검증 연구임.
- 한 줄 정의 : `AlphaProof Code`는 인간과 AI가 협업해 Lean 명세를 작성하고, `Gemini Carbon` 기반 에이전트 팀이 컴파일된 AArch64 바이너리가 보안 명세를 만족함을 수학적으로 증명하는 프레임워크다.
- 원문 : [Introducing AlphaProof Code: a breakthrough in verifying complex software at depth](https://deepmind.google/blog/introducing-alphaproof-code/)

# 그래서 도대체 뭔데 ?
- 기존 정형 검증은 수십 인년이 걸리고 설계 수준에 머물렀으나, 증명 작성을 에이전트 팀에 맡겨 수정하지 않은 상용 코드(`libsignal v0.105.4`) 바이너리를 4주 만에 검증함.
	- 💡 정형 검증 (Formal Verification) : 소프트웨어가 명세된 보안 · 정확성 조건을 만족함을 수학적으로 증명하는 기법임.
- 전문가는 약 26,000줄의 명세 · 기계어 의미론을 신뢰 기반으로 삼고 에이전트가 감사해 추려낸 코드베이스의 1%만 재검토하며, 에이전트가 짠 약 650만 줄의 증명은 `Lean` 커널이 전수 검사함.
	- 💡 Lean : 코드의 수학적 정확성과 정형 증명을 기계적으로 검증하는 정리 증명 언어 및 커널임.
- Signal의 양자 내성 핸드셰이크(`PQXDH`)와 키 갱신(`Triple Ratchet`)을 묶어, 기호 모델 10개 정리와 계산 모델 보안 상한을 AArch64 기계어 수준에서 증명함.
	- 💡 PQXDH · Triple Ratchet : Diffie-Hellman에 양자 내성 KEM(`Kyber1024` · `ML-KEM-768`)을 결합한 Signal 암호화 프로토콜임.

# 어떻게 동작하나 ?
1. 인간 · 에이전트 협업 Lean 명세 작성과 변이 테스트
	- 명세 에이전트가 Lean 정리 초안을 짜고 리뷰어 비평을 거쳐 전문가가 승인함.
	- 인위적 버그를 심는 변이 테스트와 과거 `libsignal` 버그 2건 재주입으로 명세 강도를 검증함.
	→ 신뢰해야 하는 명세(약 18,000줄)가 버그를 놓치지 않게 보장함.
2. AArch64 기계어 의미론(`ElfRunsTo`) 모델링과 바이너리 적재
	- 수정 없는 `libsignal`(`v0.105.4`)과 `spqr`(`v1.6.0`)을 `rustc`(`1.98.1`) · `musl`로 정적 링크한 AArch64 바이너리로 만듦.
	- 명령어 467개 · 시스템 콜 31개를 7,532줄(웹 공개본 7,578줄) Lean 코드로 정의하고, 암호 프리미티브 등 39개(웹 공개본 37개) 루틴만 신뢰 계약으로 후킹해 나머지를 명령어 단위로 추론함.
	→ 컴파일러를 신뢰하지 않고 실제 기계어 실행 경로를 추적함.
3. 자율 에이전트 팀의 계층적 증명 합성 (Proof Synthesis)
	- 단일 머신에서 캠페인당 40 ~ 80개 에이전트가 24 ~ 72시간 돌며, 전체 약 650만 줄(블로그 600만 줄 이상)의 Lean 증명을 생성함.
	- 오케스트레이터 아래 팀 리드와 워커를 두고 파일당 1명만 편집하며 인테그레이터만 커밋함.
	→ 충돌이나 컨텍스트 유실 없이 수백만 줄의 증명을 완성함.
4. 게이트키퍼의 `comparator` 검증과 이중 보안 모델 증명 완료
	- 게이트키퍼가 격리 보관된 명세 사본과 최종 증명을 `comparator` 및 Lean 커널로 대조해 일치할 때만 완료를 선언함.
	- `DyLean` 기호 모델 10개 정리와 계산 모델 공격자 이점 상한(Theorem 2)을 모두 증명함.
	→ 증명 코드에 오류가 있어도 Lean 커널이 거부하므로 증명 에이전트를 신뢰할 필요가 없음.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : `seL4`(20인년)나 `CompCert`(6인년)처럼 검증용으로 짠 코드에 수년의 인력을 투입하거나, 추상 설계 모델만 검증해 설계와 구현 사이의 버그를 막지 못했음.
- 이번 방식 : 상용 Rust 구현체(`libsignal`)를 수정 없이 컴파일한 AArch64 바이너리 그대로 두고, 인간은 약 26,000줄의 명세 · 의미론에 집중하며 에이전트 팀이 650만 줄 증명을 작성해 4주 만에 끝냄.
→ 수작업 증명 비용을 에이전트 자율 작업과 Lean 커널 검사로 대체해 프로덕션 코드까지 검증 범위를 넓힘.

# 숫자로 보면
| 항목 | 이전 (기존 정형 검증 / 프로토콜 분석) | 이번 (`AlphaProof Code` + `libsignal`) | 출처 |
|---|---|---|---|
| 검증 소요 기간 및 인력 | `seL4` 20인년 / `CompCert` 6인년 (검증용으로 작성된 코드 기준) | 수정 없는 상용 `libsignal` 기계어 검증에 4주 소요 | 공식 블로그 · 논문 |
| 검증 대상 및 깊이 | 추상 프로토콜 모델 또는 검증용 재구현 코드 (설계 수준) | 기본 `rustc` 1.98.1로 컴파일된 `libsignal` v0.105.4 + `spqr` v1.6.0 AArch64 바이너리 | 논문 |
| 생성된 Lean 증명 규모 | 수작업 증명 작성 (대규모 상용 코드 적용 불가) | 약 650만 줄 (블로그 본문 600만 줄 이상) | 공식 블로그 · 논문 |
| 사람이 신뢰 · 검토하는 규모 | 전체 명세 및 증명 과정 전반 | 코드베이스의 1%만 인간 재검토 / 신뢰 기반(TCB) 총 약 26,000줄 (명세 약 18,000줄 + 의미론 · 심볼 약 8,000줄) | 공식 블로그 · 논문 |
| AArch64 기계어 의미론 규모 | 해당 없음 | 명령어 467개 · 시스템 콜 31개 (PDF 7,532줄 / 웹 논문 7,578줄, 10회 호출 · 1,560만 명령어 대조 검증) | 논문 · 웹 공개본 |
| 자율 증명 에이전트 팀 규모 | 해당 없음 | 단일 머신에서 캠페인당 40 ~ 80개 에이전트가 24 ~ 72시간 구동 | 논문 |
| 바이너리 메모리 · 실행 보장 | 부분적 크래시 방지 또는 미검증 | 1GiB 힙 · 8MiB 스택 기준 세션 레코드 1.2MB 미만 유지, 입력 한도(표준 입력 $2^{20}$바이트 · 평문 $10^6$바이트) 내 OOM · 폴트 · 무한루프 없음 증명 | 논문 |
| 버그 탐지 실증 (과거 버그 재주입) | 해당 없음 | 과거 수정된 실제 `libsignal` 버그 2건 재주입 시 2건 모두 비보안(정리 위반)임을 기계 증명 | 공식 블로그 · 논문 |

# 주의할 점 / 한계
- 검증 범위 제약 : `libsignal v0.105.4`의 1대1 세션(`init` · `send` · `recv`)만 다뤘으며 그룹 메시징 · 다중 기기 상태 · 키 생성(`keygen`)은 제외됨.
- 모델별 미포함 영역 : 기호 모델은 8바이트 MAC 추측($2^{-64}$ 확률) 같은 충돌이 없는 실행을 전제하며 계산적 비밀성 · 다자간 세션 · SPQR 양자 내성 치유 · 일회용 Kyber 프리키를 제외함. 계산 모델은 양자 공격자를 다루지 않으며 다수 장기 세션에선 보안 상한이 공허해짐.
- 기계어 의미론 및 신뢰 경계(TCB) : 단일 스레드 · 정적 링크만 모델링해 스레드 · 시그널 · 동적 링킹은 검증 불가함. 39개(웹 공개본 37개) 후킹 루틴은 신뢰 계약으로 대체했으며, 약 26,000줄의 명세 · 의미론과 Lean 커널은 사람이 신뢰해야 함.
- 아직 확인 안 된 것 : 머신 사양, 토큰량 · 비용, 명세 모델 비중은 원문에 없음.

# 정리
- `AlphaProof Code`는 인간의 Lean 명세 설계 · 검토(약 26,000줄 신뢰 기반, 에이전트 감사 후 코드베이스 1% 재검토)와 `Gemini Carbon` 에이전트 팀의 자율 증명(약 650만 줄)을 결합해, 상용 `libsignal` 무수정 바이너리를 AArch64 기계어 수준에서 4주 만에 첫 정형 검증한 프레임워크다.
- Lean 기반 AArch64 기계어 의미론과 `libsignal` 명세 · 증명 아티팩트(`code-verification`)가 오픈소스로 공개되어 암호 · 시스템 보안 검증 연구자와 엔지니어가 참고할 수 있으며, 원문은 이를 의료기기 펌웨어 · 전력망 소프트웨어 등 핵심 인프라로 확장하기 위한 후속 연구의 기반으로 제시함.

# 참고
- [Introducing AlphaProof Code: a breakthrough in verifying complex software at depth](https://deepmind.google/blog/introducing-alphaproof-code/) — Google DeepMind Blog
- [AlphaProof Code: Verifying Signal’s Security at the Machine-Code Level (PDF)](https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf) — Google DeepMind Technical Paper
- [AlphaProof Code: Verifying Signal’s Security at the Machine-Code Level (Web & Artifacts)](https://google-deepmind.github.io/code-verification) — Google DeepMind GitHub Pages
- [Introducing CodeMender: an AI agent for code security](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/) — Google DeepMind Blog
