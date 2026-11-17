---
weight: 201
title: "ChatGPT for Healthcare — 컴퓨터 사용 에이전트와 20개 이상의 의료 플러그인으로 병원 업무를 잇는다"
date: 2026-11-17T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> API가 닿지 않는 병원 전자의무기록(EHR) · 보험사 포털 화면 조작부터 임상 근거 검색, 20개 이상의 의료 플러그인 호출까지 한 플랫폼에서 처리한다 !

# 개요
- 무엇 : OpenAI가 2026.11.16 의료 현장의 다단계 임상 · 행정 업무를 처리하는 ChatGPT for Healthcare 업데이트(컴퓨터 사용 에이전트 · 임상 근거 검색 개선 · 신규 플러그인 20개 이상)를 공개함 (ChatGPT for Clinicians · ChatGPT Work · Codex · OpenAI API 지원).
- 한 줄 정의 : ChatGPT for Healthcare는 화면 조작 에이전트와 임상 근거 검색 · 의료 플러그인을 한 플랫폼에 묶어 진료 및 행정 워크플로를 수행하는 의료 특화 AI 서비스다.
- 원문 : [More ways to move care forward with ChatGPT for Healthcare](https://openai.com/index/more-ways-to-move-care-forward-with-chatgpt-for-healthcare)

# 그래서 도대체 뭔데 ?
- 병원에서는 환자를 진료하고 행정을 처리할 때 전자의무기록(EHR) · 병원 정책 시스템 · 스케줄러 · 보험사 사전 승인(Prior Authorization) 포털에 흩어진 정보를 사람이 일일이 찾아 옮겨 적어야 했음.
- 이번 업데이트는 API 연동이 없거나 불완전한 소프트웨어를 화면에서 직접 조작하는 컴퓨터 사용 에이전트(Computer-use agent), 의학 근거를 찾아 평가 · 인용하는 임상 근거 검색, IMO Health MCP(Model Context Protocol) 서버 · UpToDate 등 20개 이상의 신규 헬스케어 플러그인을 BAA(비즈니스 제휴 계약) 기반 워크스페이스에 통합함.
	- 💡 전자의무기록(EHR) : 병원에서 환자의 방문 기록 · 처방 · 검사 · 영상 결과를 전산으로 관리하는 시스템.
	- 💡 사전 승인(Prior Authorization) : MRI 같은 검사나 처방을 시행하기 전 보험사에 의학적 근거를 제출해 급여 승인을 받는 절차.
	- 💡 MCP(Model Context Protocol) : AI 모델이 외부 도구 · 지식 그래프 서버에 연결해 용어 정규화와 데이터 질의를 수행하는 연동 규격.
	- 💡 BAA(비즈니스 제휴 계약) : 미국 의료정보보호법(HIPAA)에 따라 보호대상 건강정보(PHI)를 다루기 위해 체결하는 계약.

# 어떻게 동작하나 ?
1. 컴퓨터 사용 에이전트를 통한 다단계 UI 조작
	- 에이전트가 기존 의료 소프트웨어 화면을 읽고 클릭 · 타이핑 · 애플리케이션 간 이동을 수행함.
	- 요통 환자 MRI 데모(합성 환자 데이터)에서는 환자가 요통 메시지를 보내면 에이전트가 EHR 내 방문 기록 · 물리치료 기록 · 이전 영상 기록을 검토해 임상의 검토용 MRI 오더 · 진료 기록 · 환자 답장 초안을 작성하고, 같은 기록으로 보험사 포털에서 사전 승인 담당자 검토용 사전 승인 요청서를 준비함.
	→ API가 닿지 않는 병원 EHR과 보험사 포털 사이에서도 수동 복사 없이 다단계 업무를 이어감.

2. 현장 트러블슈팅 및 감독 구조 (API 한계 보완 · 모호한 기록 제어 · 행동 검증)
	- 현상 : Assort의 의뢰 워크플로에서는 Athena EHR API로 환자 차트에 의뢰서를 첨부할 수만 있고 최종 종료 처리가 안 돼 직원 후속 조치 목록에 계속 남음. Ambience의 사전 승인 과정에서는 보험사 웹사이트에 입력할 환자 차트 근거가 모호한 경우가 발생함.
	- 원인 : 의뢰를 닫는 단계나 보험사 포털 입력은 API가 지원하지 않아 GUI 화면에서 별도로 조작해야 하며, 의료 환경에서는 에이전트의 모든 행동이 통제 · 감사 가능해야 하기 때문임.
	- 해결 : Assort는 Codex 컴퓨터 사용 에이전트로 Athena UI에서 의뢰 의료진을 선택하고 세부 정보를 입력해 방문 예약됨 상태로 바꿔 후속 조치 목록에서 자동 제외함. Ambience는 기록이 모호하면 멈추고 임상의에게 질문한 뒤 승인을 거쳐 제출하며 단계별 감사 로그와 일시 정지 제어권을 제공함. CVS Health는 스크린샷과 행동 기록으로 에이전트 작업 · 앱 상태를 검증하는 OpenAI Agents SDK 기반 `Agent Kit`을 오픈소스로 공개함.
	→ API 미지원 구간은 UI 조작으로 메우면서 환자 안전과 직결되는 지점에서는 인간 감독과 감사 로그를 강제함.

3. 임상 근거 검색 및 20개 이상의 헬스케어 플러그인 · MCP 서버 연쇄 호출
	- 임상 근거 검색(trusted clinical search)은 의학 문헌을 찾아 평가 · 인용해 임상 질문을 다음 조치로 연결하며, IMO Health MCP Server(`imo-graphql` · `imo-normalize` · `imo-setup` 3개 스킬)는 문제(진단) · 시술 · 약물 · 검사 4개 도메인 용어를 정규화하고 ICD-10-CM · SNOMED CT · CPT · HCPCS · RxNorm 5개 표준 코드 매핑과 GraphQL 탐색을 수행함.
	- 비조영 무릎 MRI 병원 2곳을 비교할 때 IMO Health로 시술 코드를 찾고 Stedi로 보험 자격 · 혜택을 조회한 뒤 Turquoise Health로 병원별 협상 수가와 본인부담금 추정 추가 정보를 확인함. 타 병원 심부전 퇴원 환자는 Metriport로 퇴원 요약서를 찾아 변경된 약물을 파악하고 UpToDate Expert AI로 약물 변경에 따른 추적 관찰 지침과 출처 링크를 함께 불러옴.
	→ 여러 포털을 따로 띄우지 않고 한 대화 안에서 근거 확인부터 코드 매핑 · 수가 비교까지 처리함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 케이스 매니저나 의료진이 10개 이상의 임상 · 행정 시스템을 수동으로 오가며 정보를 모아야 했고, 기존 API 연동은 차트에 의뢰서를 첨부하는 등 일부 단계만 지원해 화면 조작이 필요한 후속 처리는 사람이 직접 마무리해야 했음.
- 이번 방식 : 컴퓨터 사용 에이전트가 GUI 화면을 조작해 API 밖 워크플로(EHR 의뢰 종료 · 보험사 사전 승인서 작성 · 다중 시스템 문맥 통합)를 수행하고, 이전 버전 대비 8개 평가 차원 모두 개선된 임상 근거 검색과 20개 이상의 신규 플러그인이 한 플랫폼에서 결합됨.
→ 단순 질의응답이나 부분 API 호출을 넘어 실제 병원 · 보험사 소프트웨어 화면 위에서 다음 임상 · 행정 단계를 이어갈 수 있는지가 차이점임.

# 숫자로 보면
| 항목 | 이전 / 비교 기준 | 이번 결과 | 출처 |
|---|---|---|---|
| EHR 인박스 임상 안전성 (GPT-6 Astra) | 의사 설계 다단계 EHR 인박스 과업 325건 | 99% 임상적으로 안전(Safe) 판정 | OpenAI 컴퓨터 사용 블로그 |
| EHR 인박스 유용성 (GPT-6 Astra) | 의사 5점 척도 평가 646건 | 93%가 매우 유용 또는 극도로 유용 응답 | OpenAI 컴퓨터 사용 블로그 |
| HealthAdminBench 점수 (GPT-6 Astra) | Stanford 독립 행정 벤치마크 (최대 추론 노력) | 가용 루브릭 점수의 94.3% 획득 | OpenAI 컴퓨터 사용 블로그 |
| HealthAdminBench 점수 및 비용 (GPT-6 Luna) | Stanford 독립 행정 벤치마크 · GPT-6 Astra 대비 (최대 추론 노력) | 가용 루브릭 점수의 91.8% 획득 · 과업당 8.5센트 (비용 98% 절감) | OpenAI 컴퓨터 사용 블로그 |
| 임상 근거 검색 블라인드 평가 | 이전 ChatGPT for Clinicians (의사 리뷰 1,300건 이상) | 사실 정확성 · 안전성 · 실행 가능성 · 출처 권위성 등 8개 차원 전 항목 우위 | OpenAI 헬스케어 블로그 |
| Cigna Healthcare 정보 탐색 | 10개 이상 임상 · 행정 시스템 수동 탐색 | 컴퓨터 사용 에이전트로 수 초 만에 문맥 통합 | OpenAI 컴퓨터 사용 블로그 |
| 신규 헬스케어 플러그인 및 코드 매핑 | 기존 플러그인 생태계 | 20개 이상 신규 추가 (IMO Health 기준 4개 도메인 · 5개 표준 코드 매핑 · 3개 스킬) | OpenAI 헬스케어 · 플러그인 문서 |

# 주의할 점 / 한계
- 사람 검토 및 승인 필수 : 처방 · 오더 · 보험 사전 승인 제출 등 환자 안전과 직결되는 단계는 에이전트가 초안 작성까지만 수행하거나 작업을 멈추며, 실제 발효 · 제출 전에는 임상의 · 담당자의 검토와 승인을 거쳐야 함.
- 계정 · 플러그인별 권한 한계 : 무료인 ChatGPT for Clinicians는 미국 내 인증된 임상의만 가입할 수 있고 일부 플러그인만 제공됨. UpToDate Expert AI는 별도 유효 구독 · 적격 계정 · 연결 권한 활성화가 필요하며 직접 처방 · 오더 생성 · EHR 접근을 하지 않고, IMO Health MCP Server도 읽기(Read) 전용이며 진단 구체화 시 문서화된 임상 세부 정보만 써야 함.
- HIPAA 준수 조건 : 보호대상 건강정보(PHI)가 포함된 워크플로를 운영하려면 OpenAI와 BAA가 체결된 적격 서비스를 써야 하며, 필수 보안 · 데이터 보존 설정을 적용하고 보호 조치를 연결된 시스템까지 확장해야 함 (입력 데이터는 파운데이션 모델 학습에 안 쓰임).
- 수치 조건과 원문에 없는 내용 : 요통 환자 MRI 데모는 합성 환자 데이터로 진행됐고 HealthAdminBench 점수(Astra 94.3% · Luna 91.8%)는 두 모델 모두 최대 추론 노력 조건에서 측정함. 임상 근거 검색 블라인드 평가(1,300건 이상 · 8개 차원)의 차원별 세부 수치 · GPT-6 Astra의 과업당 절대 비용 · EHR 인박스 평가(325건)의 세부 오답 사례는 원문에 없음.

# 정리
- 컴퓨터 사용 에이전트와 개선된 임상 근거 검색, IMO Health MCP Server 등 20개 이상의 신규 헬스케어 플러그인을 결합해 API가 없거나 불완전한 병원 EHR과 보험사 포털 사이의 다단계 업무를 잇는 업데이트임.
- HealthAdminBench에서 GPT-6 Luna가 과업당 8.5센트(Astra 대비 98% 절감)로 91.8%를 기록하고 CVS Health가 OpenAI Agents SDK 기반 `Agent Kit`을 오픈소스로 공개한 만큼, 의료 행정 자동화나 레거시 GUI 연동 에이전트를 설계하는 팀에서 참고할 만함.

# 참고
- [More ways to move care forward with ChatGPT for Healthcare](https://openai.com/index/more-ways-to-move-care-forward-with-chatgpt-for-healthcare) — OpenAI Blog
- [Advancing computer-use agents for healthcare teams](https://openai.com/index/advancing-computer-use-for-healthcare-teams/) — OpenAI Blog
- [IMO Health MCP Server plugin for ChatGPT](https://openai.com/business/plugins/imo-health/) — OpenAI Business Plugins
- [UpToDate Expert AI plugin for ChatGPT](https://openai.com/business/plugins/uptodate-expert-ai/) — OpenAI Business Plugins
