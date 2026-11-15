---
weight: 199
title: "IBM Granite 4.1 LLMON — 특수 토큰과 실행 블록으로 명령과 데이터를 분리한다"
date: 2026-11-15T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 파서용으로 만들어진 JSON 대신 토크나이저 레벨의 특수 토큰과 실행 블록으로 명령과 데이터를 분리해 간접 프롬프트 인젝션을 차단하는 LLM 전용 마크업 언어 !

# 개요
- 무엇 : IBM Granite 팀이 2026.11.12에 LLM 전용 마크업 언어인 LLMON과 이를 적용한 `granite-4.1-3b-LLMON-preview` · `granite-4.1-8b-LLMON-preview` 모델 2종, 변환 툴킷을 Apache 2.0 라이선스로 공개함.
- 한 줄 정의 : LLMON(LLM Object Notation)은 프롬프트의 각 구성 요소를 고유 ID가 붙은 개별 블록으로 감싸고 실행 블록(`exec`)으로 명령과 입력 데이터를 명시적으로 바인딩하는 LLM 네이티브 마크업 언어다.
- 원문 : [LLMON: An LLM-Native Markup Language, now in Granite 4.1 3B and 8B](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite)

# 그래서 도대체 뭔데 ?
- 에이전트나 RAG 파이프라인이 길어지면 컨텍스트 안에 시스템 프롬프트 · 이전 대화 턴 · 검색된 문서 · 도구 실행 결과 · 출력 제약 조건이 한데 뒤섞이게 됨.
- 기존에는 이 구조를 평문으로 이어 붙이거나 파서(parser)를 위해 만들어진 JSON으로 표기했는데, 특히 3B · 8B 같은 소형 모델일수록 어디까지가 명령이고 어디부터가 외부 데이터인지 구분하지 못해 오작동하거나 프롬프트 인젝션 공격에 뚫리는 문제가 있었음.
	- 💡 간접 프롬프트 인젝션(Indirect Prompt Injection) : 사용자가 직접 입력한 명령이 아니라 외부 검색 문서 · 웹페이지 · 도구 반환값 같은 데이터 안에 악성 지시문을 숨겨 모델의 동작을 가로채는 공격 기법임.
- LLMON은 프로그래밍 언어에서 함수를 호출하고 인자를 넘기듯, 프롬프트 구성 요소마다 태그와 2글자 고유 ID를 부여한 뒤 마지막 `exec` 블록에서 실행할 명령 ID와 대상 데이터 ID를 포인터로 묶어 모델에 전달함.
	- 💡 실행 블록(`exec` block) : 현재 턴에서 어떤 명령(`instruction`)을 어떤 입력(`input`)과 제약 조건(`requirement`)에 적용해 어느 출력 블록(`output`)에 답을 쓸지 지정하는 바인딩 블록임.

# 어떻게 동작하나 ?
1. 예약된 6개 단일 특수 토큰으로 구조와 본문 어휘 분리
	- `<|open|>` · `<|close|>` · `<|open_end|>` · `<|self_close|>` · `<|.|>` · `<|:|>` 6개 구분자를 토크나이저에 단일 특수 토큰으로 등록함.
	- 블록을 열 때 태그 경로(`instr` · `data` · `req` · `doc` · `tool` · `system` · `assistant` · `exec`)와 2글자 단일 토큰 ID를 붙여 `<|open|>instr<|:|>ID<|close|>...<|open_end|>` 형태로 감쌈.
	→ 본문 텍스트에 따옴표나 중괄호가 아무리 나와도 구조 구분자와 토큰 공간 자체가 겹치지 않으며, 블록 ID 참조에 항상 2토큰만 소모됨.

2. `exec` 블록 포인터 바인딩과 권한 규칙(Privilege Rule) 적용
	- 내장된 `chat_template.jinja`가 메시지 리스트의 각 항목에 붙은 `"exec": True` 또는 `"exec": False` 속성을 읽어 프롬프트 하단에 `exec` 블록을 자동 생성함.
	- `exec<|.|>instruction`과 `exec<|.|>system` 포인터가 가리키는 블록만 실행 권한이 있는 명령으로 인정하고, `exec<|.|>input`이 가리키는 데이터 · 문서 · 도구 결과는 내부 문구가 명령형이라 해도 읽어야 할 자료로만 취급함.
	→ 외부 문서나 도구 결과에 악성 명령이 들어 있거나 `"exec": False`로 미바인딩된 상태라면 모델이 해당 지시를 실행하지 않고 무시하게 됨.

3. 미바인딩 미끼(Decoy) 증강 SFT와 다단계 강화학습(GRPO · DPO)
	- 기존 Instruct 모델 위에 덧씌우지 않고 `Granite-4.1-3B-base` 및 `Granite-4.1-8B-base` 베이스 체크포인트에서 후학습을 시작함.
	- 일반 SFT 코퍼스(채팅 · 멀티턴 · RAG · 도구 호출)를 LLMON 포맷으로 재직렬화하면서 컨텍스트에 존재하지만 `exec` 블록에 연결되지 않은 가짜(decoy) 명령과 데이터 블록을 섞어 학습시킴.
	- 이어서 다중 도메인 추론 · RLHF · 지식 보정 · 수학을 다루는 5단계 순차 GRPO를 거친 뒤, 인젝션 시도에 대한 모델 자체 응답으로 만든 1,000개 온폴리시 선호 쌍으로 최종 DPO 학습을 수행함.
	→ 별도 외부 가드레일 없이도 모델 어텐션 레이어가 `exec` 블록에 바인딩된 명령과 데이터에만 집중하고 나머지는 흘려보내는 행동을 내재화함.

4. 무손실 JSON 변환기와 도메인별 커스텀 어휘 LoRA 확장
	- `json-to-llmon` 같은 무손실 변환 도구를 통해 중첩된 JSON 문서를 `tool<|.|>parameters<|.|>...`처럼 평탄화된 개별 블록으로 자동 변환하고 다시 JSON으로 되돌릴 수 있음 (`Mellea` 라이브러리는 내부 LLM 호출을 자동으로 LLMON으로 변환해 처리함).
	- 고정된 태그에 묶이지 않고 ScienceWorld 환경처럼 `instr.task.goal` · `data.state.room` · `assistant.next_action` 등 도메인 전용 어휘를 직접 정의해 LoRA 어댑터로 파인튜닝할 수 있음.
	→ 기존 JSON 기반 파이프라인 코드를 뜯어고치지 않고도 도입할 수 있으며, 에이전트의 계획 궤적이나 도구 호출 구조를 도메인에 맞게 확장하게 됨.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : JSON이나 일반 채팅 템플릿을 사용해 시스템 · 사용자 · 어시스턴트 역할만 나눴음. JSON의 `{` · `"` · `:` 기호는 일반 텍스트에도 똑같이 등장하는 문자라 토크나이저가 구조와 본문을 구분하지 못했고, 중첩 깊이를 파악하려면 트랜스포머가 취약한 괄호 개수 세기에 의존해야 했음. 또한 사용자 턴 안에 명령 · 검색 문서 · 제약 조건이 하나의 평문 문자열로 합쳐져 모델이 스스로 역할을 추론해야 했음.
- 이번 방식 : 토크나이저에 예약된 특수 토큰으로 태그 경계를 표시하고, 중첩 구조를 로컬 태그 경로(`<|.|>`)로 풀어서 표기함. 한 턴 안에서도 명령(`instr`) · 데이터(`data`) · 제약(`req`)을 별도 ID 블록으로 쪼갠 뒤 `exec` 블록에서 실행 대상을 포인터로 지정함.
→ 문서 안의 따옴표와 필드 종료 따옴표가 섞이는 파싱 오류와 긴 구간의 괄호 추적 문제를 없애고, 명령과 데이터의 경계를 문법 수준에서 분리해 간접 프롬프트 인젝션과 문맥 오염(오래된 대화 턴이나 무관한 문서가 답변에 섞이는 현상)을 함께 막아냄.

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| OPI 간접 프롬프트 인젝션 방어 (vs 최고 프런티어 모델) | 비교 기준 모델 | 공격 회피 47% 더 많음 | [공식 블로그](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite) |
| OPI 간접 프롬프트 인젝션 방어 (vs 최고 오픈소스 모델) | 비교 기준 모델 | 공격 회피 95% 더 많음 | [공식 블로그](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite) |
| 8B Tulu3 Safety Eval Avg (안전성) | 75.57 (8B-Instruct) | 87.31 (8B-LLMON) | [8B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) |
| 8B AttaQ / SALAD-Bench (안전성) | 81.19 / 95.80 (8B-Instruct) | 86.07 / 97.70 (8B-LLMON) | [8B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) |
| 8B MMLU (5-shot) / IFEval Avg (일반 · 정렬) | 73.84 / 87.06 (8B-Instruct) | 74.20 / 86.69 (8B-LLMON) | [8B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) |
| 8B HumanEval / BigCodeBench (pass@1, 코드) | 85.37 / 35.00 (8B-Instruct) | 86.59 / 44.04 (8B-LLMON) | [8B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) |
| 8B BFCL v3 (도구 호출) | 68.27 (8B-Instruct) | 67.93 (8B-LLMON) | [8B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) |
| 3B Tulu3 Safety Eval Avg / SALAD-Bench (안전성) | 66.84 / 93.95 (3B-Instruct) | 86.13 / 97.25 (3B-LLMON) | [3B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview) |
| 3B MMLU (5-shot) / HumanEval (pass@1) / BFCL v3 | 67.02 / 81.71 / 60.80 (3B-Instruct) | 68.05 / 84.15 / 60.71 (3B-LLMON) | [3B 모델 카드](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview) |

# 주의할 점 / 한계
- 권한 규칙은 강제 보장이 아닌 학습된 행동임 : `exec` 블록을 통한 명령 · 데이터 분리 규칙은 후학습으로 습득한 통계적 행동이라 인젝션 성공 확률을 크게 낮추지만 0으로 보장하지는 못함. 민감한 시스템 권한을 가진 에이전트의 단독 방어 수단으로 써서는 안 됨.
- 일반 채팅 프롬프트 입력 시 품질 저하 : LLMON 포맷 입력에 맞춰 학습되었기 때문에 일반 채팅 템플릿 형식을 그대로 넣으면 학습 분포(OOD)를 벗어나 성능이 떨어짐. 반드시 내장된 `chat_template.jinja`를 거쳐 렌더링해야 하며, 현재 공개본은 프로덕션용이 아닌 실험용 프리뷰임.
- 일부 추론 · 수학 벤치마크 점수 하락 및 정적 공격 한계 : 8B 모델 기준 Minerva Math(80.10 → 72.20) · DeepMind Math(80.07 → 70.86) · GPQA(41.96 → 35.05) · CRUXEval-O(47.63 → 36.88)에서는 기존 Instruct 모델보다 점수가 낮게 측정됨. 또한 OPI · ASB · StruQ 결과는 단일 턴의 정적 간접 프롬프트 인젝션 기준이며, 여러 대화 턴에 걸쳐 진행되는 적응형(adaptive) 공격 방어는 아직 연구 중임.
- 아직 확인 안 된 것 : OPI 벤치마크에서 비교 대상 모델들의 개별 절대 점수 수치와 후학습에 투입된 구체적인 GPU 하드웨어 사양 및 학습 시간은 원문에 없음.

# 정리
- 파서 중심의 JSON이나 평문 채팅 템플릿 대신 특수 토큰 구분자와 `exec` 포인터 바인딩을 도입해, LLM이 명령 · 데이터 · 제약 조건의 구조와 실행 범위를 문법 수준에서 구분하게 만든 시도임.
- 3B · 8B 규모 소형 모델로 외부 문서를 긁어오는 RAG 파이프라인이나 도구 호출 에이전트를 구축하면서 간접 프롬프트 인젝션과 문맥 섞임 문제를 줄이고 싶을 때 테스트해볼 만함.

# 참고
- [LLMON: An LLM-Native Markup Language, now in Granite 4.1 3B and 8B](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite) — Hugging Face Blog (IBM Granite)
- [ibm-granite/granite-4.1-8b-llmon-preview](https://huggingface.co/ibm-granite/granite-4.1-8b-llmon-preview) — Hugging Face Model Card
- [ibm-granite/granite-4.1-3b-llmon-preview](https://huggingface.co/ibm-granite/granite-4.1-3b-llmon-preview) — Hugging Face Model Card
- [generative-computing/llmon](https://github.com/generative-computing/llmon) — GitHub Repository
