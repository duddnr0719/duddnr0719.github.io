---
weight: 185
title: "OpenAI Images 2.6 — 생성 속도를 50% 높이고 루프 GIF와 API 마크업 편집을 결합한다"
date: 2026-11-10T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 생성 속도를 50% 끌어올린 Sunburst · Flare 모델로 루프 GIF 생성부터 API 마크업 편집, SVG 출력까지 지원하는 OpenAI의 신규 이미지 생성 모델 !

# 개요
- 무엇 : OpenAI가 2026.11.06(시스템 카드 2026.11.04)에 ChatGPT · Codex · API로 공개한 이미지 · GIF 생성 및 편집 모델 `Images 2.6` (`GPT-Image-2.6 Sunburst`, `GPT-Image-2.6 Flare`)임.
- 한 줄 정의 : `Images 2.6`은 생성 속도를 이전 대비 50% 높이고 루프 GIF 생성, API 이미지 마크업 편집, SVG 내보내기, 장면 계획량(`complexity`) 제어를 결합한 이미지 · GIF 생성 및 편집 모델이다.
- 원문 : [Introducing Images 2.6](https://openai.com/index/introducing-images-2-6)

# 그래서 도대체 뭔데 ?
- ChatGPT · Codex · API에서 주당 40억 장(일평균 5억 장 이상)이 생성되는 환경에서, 속도를 50% 높이고 편집 간 디테일 일관성을 강화한 모델임.
- API 모델로 고속 생성 · 레이아웃 개선용 `GPT-Image-2.6 Flare`와 정밀 디테일 · 편집 일관성용 `GPT-Image-2.6 Sunburst`를 업데이트해 제공함.
- 스프라이트 시트 등으로 마스코트 · 제품 샷을 루프 GIF로 만들고, 펜 스케치도 애니메이션 캐릭터로 변환함.
	- 💡 스프라이트 시트 (Sprite Sheet) : 연속 프레임을 격자 이미지에 배열해 루프 GIF를 만드는 기법임.
- API 이미지 마크업(Image markup), SVG 내보내기, 계획량 제어(`complexity`)와 C2PA · SynthID 출처 증명을 지원함.
	- 💡 C2PA · SynthID : 출처 표준 메타데이터(C2PA)와 비가시성 워터마킹 레이어를 심는 Google DeepMind 기술(SynthID)임.

# 어떻게 동작하나 ?
1. 모델(`Flare` / `Sunburst`) 선택과 계획 복잡도(`complexity`) 설정
	- 빠른 생성 · 레이아웃에는 `Flare`(`low` 품질 최소 6초)를, 정밀 디테일 · 편집 일관성에는 `Sunburst`(`medium` · `high` 품질)를 씀.
	- 화질(`quality`)과 별개로 장면 계획량을 ChatGPT 모델 피커(추론 노력)와 API(`complexity`)로 조절함.
	→ 빠른 편집엔 `low`를, 제약이 많은 장면엔 `medium` · `high`를 써서 속도를 조율함.
2. 스프라이트 시트 기반 루프 GIF 및 스케치 애니메이션
	- OpenArt 예시 기준, 고정 배경에서 3열 2행 그리드에 연속 프레임 6개를 배치해 6번째가 1번째로 이어지게 구성함.
	→ 마스코트 · 리액션 · 제품 루프 GIF나 스토리보드, 스케치 기반 애니메이션 캐릭터를 생성함.
3. API 이미지 마크업 편집과 SVG 출력
	- ChatGPT의 이미지 마크업(photo markup)과 주석 반응성을 개선해 API로 확장하고, 결과물을 SVG로도 내보냄.
	→ 캐릭터 · 제품 · 브랜드 일관성을 유지하며 수정 위치를 지정하고, 완성본을 웹 · 앱 · 인쇄물에 바로 투입함.
4. 다계층 안전 모더레이션과 이중 출처 증명
	- 업스트림 LLM 정책 검사와 다운스트림 안전 특화 멀티모달 추론 모델이 입출력을 차단함(ChatGPT엔 동기식 CSAM 분류기 추가).
	- 추론된 움직임을 고려한 GIF 가드레일을 적용하고, C2PA 메타데이터와 SynthID 워터마킹을 함께 심음.
	→ 프레임 연결 시 드러나는 유해 모션을 차단하고 공개 검증 도구로 출처를 확인함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : `Images 2.5`는 정지 이미지 위주였고, 이미지 마크업은 ChatGPT에만 있었으며 `complexity` 제어 · API SVG 출력 · 루프 GIF 생성이 없었음.
- 이번 방식 : 속도를 50% 높인 `Images 2.6`에서 `Flare`(최소 6초 · 레이아웃 개선)와 `Sunburst`(고품질 · 편집 일관성)를 업데이트하고, 루프 GIF · API 마크업 · SVG · `complexity` 제어를 추가함.
→ 화질(`quality`)과 계획량(`complexity`)을 분리해 속도를 조율하고, 정지 이미지부터 루프 GIF · 웹 · 앱 · 인쇄용 SVG까지 ChatGPT와 API에서 처리함.

# 숫자로 보면
| 항목 | 이전 (`Images 2.5` 등) | 이번 (`Images 2.6`) | 출처 |
|---|---|---|---|
| 이미지 생성 속도 | 원문에 없음 (비교 기준선) | 이전 대비 50% 향상 (`Flare` + `low` 품질 시 최소 6초) | 공식 블로그 |
| 플랫폼 전체 생성 규모 | 원문에 없음 | 주당 40억 장 / 일평균 5억 장 이상 | 공식 블로그 |
| 안전성 평가 — `Sunburst` (3,077개 적대적 프롬프트) | 안전 생성 76.15% / 차단 21.94% / 미차단 1.92% | 안전 생성 75.50% / 차단 22.78% / 미차단 1.72% | 시스템 카드 |
| 안전성 평가 — `Flare` (3,077개 적대적 프롬프트) | 안전 생성 78.36% / 차단 20.15% / 미차단 1.49% (46건) | 안전 생성 75.04% / 차단 22.81% / 미차단 2.14% (66건) | 시스템 카드 |
| 성적(Sexual) 카테고리 미차단율 (3,077개 세트 내) | `2.5 Sunburst` 1.06% / `2.5 Flare` 0.53% | `2.6 Sunburst` 1.06% / `2.6 Flare` 0.00% | 시스템 카드 |
| 극단주의(Extremism) 카테고리 미차단율 (3,077개 세트 내) | `2.5 Sunburst` 2.56% / `2.5 Flare` 5.13% | `2.6 Sunburst` 0.00% / `2.6 Flare` 0.00% | 시스템 카드 |
| GIF 유해 모더레이션 탐지 재현율 (적대적 위반 GIF 세트) | 해당 없음 (신규 기능) | 전체 77.7% (폭력 행위 96.6%, 극단주의 92.9%, 혐오 · 학대 90.9%, 폭력 · 고어 89.7%, 성적 77.8%, 자해 77.5%) | 시스템 카드 |
| API 토큰 단가 (1M 토큰당) | `gpt-image-2` Batch 기준 : 이미지 입력 $4.00 / 출력 $15.00 / 캐시 $1.00 (텍스트 입력 $2.50 / 캐시 $0.625) | `Sunburst` · `Flare` Standard 기준 : 이미지 입력 $8.00 / 출력 $30.00 / 캐시 $2.00 (텍스트 입력 $5.00 / 캐시 $1.25) | API 가격 문서 |

# 주의할 점 / 한계
- 움직임 기반 GIF 유해성 탐지 한계 : 단일 프레임에선 안 보이나 프레임 연결 시 나타나는 유해 모션은 탐지가 까다로움. 적대적 위반 GIF 세트 기준 모더레이션 재현율(Recall)이 전체 77.7%이며 자해(77.5%) · 성적(77.8%) 영역에서 미탐지가 남아 있음.
- `Flare`의 모더레이션 전 안전 생성 비율 감소 : 3,077개 적대적 프롬프트에서 `2.6 Flare`의 모더레이션 전 안전 생성 비율이 `2.5 Flare`(78.36%) 대비 75.04%로 통계적으로 유의미하게 낮아졌음(Other · 성적 영향이 큼). 최종 미차단 비율도 1.49%(46건)에서 2.14%(66건, 순증 20건 중 14건이 Other)로 0.65%p 늘었으나 최종 차이는 유의미하지 않음.
- 평가 및 과금 조건 : 안전성 수치는 3,077개 적대적 프롬프트 오프라인 채점 결과로 실제 트래픽 빈도가 아님. 사이버 · 생물학 평가는 이미지 내 스크래치패드와 답안을 함께 그린 뒤 답안만 채점했으며 두 모델 모두 High 임계치 미만임(예방적 High 생물학 완화 적용). `Sunburst` · `Flare`의 1M 토큰 단가는 같으나 장당 비용은 `quality` · `complexity`별 토큰량으로 달라짐.
- 아직 확인 안 된 것 : 파라미터 크기 · 아키텍처, 외부 벤치마크 점수, `quality` · `complexity`별 장당 토큰 수는 원문에 없음.

# 정리
- `Images 2.6`은 생성 속도를 50% 높이면서 고속 · 레이아웃용 `Flare`(최소 6초)와 정밀 · 일관성용 `Sunburst`를 업데이트하고, 루프 GIF · API 마크업 · SVG 출력 · `complexity` 제어를 결합한 모델이다.
- 마케터 · 크리에이터 · 개발자 팀이 마스코트 · 제품 루프 GIF, 스토리보드, 마크업 반복 수정, 웹 · 앱 · 인쇄용 SVG 에셋 생성에 써먹을 만함.

# 참고
- [Introducing Images 2.6](https://openai.com/index/introducing-images-2-6) — OpenAI Blog
- [ChatGPT Images 2.6 System Card](https://deploymentsafety.openai.com/chatgpt-images-2-6) — OpenAI Deployment Safety Hub
- [Pricing | OpenAI API](https://developers.openai.com/api/docs/pricing#image-generation) — OpenAI Developers Documentation
