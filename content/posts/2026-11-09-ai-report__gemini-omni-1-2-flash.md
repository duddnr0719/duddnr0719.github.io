---
weight: 184
title: "Gemini Omni 1.2 Flash — 15초 네이티브 영상 생성과 멀티턴 편집을 초당 $0.07에 실행한다"
date: 2026-11-09T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 네이티브 비디오 생성 길이를 15초로 늘리고 출력 단가를 30% 낮춰 720p 기준 초당 $0.07에 멀티턴 영상 편집까지 처리하는 Google DeepMind의 비디오 생성 모델 !

# 개요
- 무엇 : Google DeepMind가 2026.11.05(Google Cloud 블로그는 2026.11.06)에 Gemini API와 Google Cloud를 통해 정식 출시(GA)한 비디오 생성 · 편집 모델 Gemini Omni 1.2 Flash(`gemini-omni-1.2-flash`)임.
- 한 줄 정의 : Gemini Omni 1.2 Flash는 텍스트 · 이미지 · 비디오 입력을 받아 네이티브 오디오가 결합된 최대 15초 영상을 생성하고 다회차 대화로 수정 · 연장하는 멀티모달 모델이다.
- 원문 : [Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips](https://deepmind.google/blog/gemini-omni-12-flash-fast-and-cost-effective-with-longer-clips/)

# 그래서 도대체 뭔데 ?
- 기존 Gemini Omni 1.1 Flash의 최대 생성 길이(10초)를 15초로 늘리고 720p 기준 초당 생성 비용을 $0.10에서 $0.07로 30% 낮춘 정식 출시 모델임.
- 전체 장면을 다시 설명하거나 처음부터 새로 만들지 않고 후속 대화만으로 제품 · 배경 · 조명 · 날씨 · 카메라 앵글 · 화면비를 고치는 상태 유지(Stateful) 멀티턴 편집을 지원함.
- 최대 6장의 참조 이미지와 클립당 최대 3초 길이의 참조 비디오를 조합해 프레임 전체에서 얼굴 · 의상 · 패키지 타이포그래피 · 브랜드 색상의 일관성을 유지함.
	- 💡 Interactions API : 비디오 생성 · 편집 · 연장을 처리하는 엔드포인트로 후속 턴에 `previous_interaction_id`를 전달하면 이전 영상을 재업로드하지 않고 문맥을 유지한 채 수정 · 연장함.
	- 💡 10-second lookback window : 비디오 연장 시 앞선 프레임은 보존하면서 입력 영상의 마지막 10초 구간을 문맥으로 참조해 움직임과 오디오를 이어 붙이는 방식임.

# 어떻게 동작하나 ?
1. 자연어 역할 추론과 멀티모달 레퍼런스 결합
	- 기존 `<FIRST_FRAME>` · `<LAST_FRAME>` · `<IMAGE_REF_0>` · `<VIDEO_REF_0>` 제어 태그를 폐기하고 자연어 프롬프트만으로 입력 미디어의 역할을 추론함 (폴백으로만 `video_config`의 `task` 파라미터 5종 사용).
	- REST 응답의 `steps` 배열은 `user_input` 뒤에 내부 추론 단계인 `thought`를 거쳐 `model_output`(`video/mp4`)을 반환함.
	- 참조 이미지는 요청당 최대 6장(캐릭터 최대 2명 · 인당 최대 3장), 참조 비디오(클립당 최대 3초)는 3 ~ 10초 생성 시 최대 3개 · 11 ~ 15초 생성 시 최대 1개까지 결합함.
	→ 태그 문법 없이 인물 사진 1장과 의상 3벌의 전후면 사진으로 360도 회전 가상 피팅 영상을 만들거나 건축물 참조 사진 2장으로 점프컷 없는 연속 FPV 드론 비행 장면을 생성함.

2. 상태 유지 멀티턴 편집과 30초 비디오 연장
	- `previous_interaction_id`를 전달하거나 Files API로 최대 15초 영상을 업로드해 지정한 요소만 수정하며, 편집 프롬프트에 `Keep everything else the same` 지시문을 넣어 나머지 요소를 고정한 채 배경 · 조명만 턴마다 바꿀 수 있음.
	- 비디오 연장은 입력 영상의 마지막 10초를 문맥으로 삼아 클립 끝에 턴당 3 ~ 10초(기본값 10초)씩 이어 붙이며 최대 총 30초까지 확장함.
	→ 언급하지 않은 요소를 보존한 채 장면 전체를 다시 설명하거나 처음부터 재생성하지 않고도 타깃 · 매체별 광고 변형본을 빠르게 제작함.

3. 저해상도 초안 작성 후 고해상도 업스케일 워크플로
	- 해상도는 `360p` · `720p`(기본값) · `1080p`(업스케일) · `4k`(업스케일) 4단계와 가로(`16:9`, 기본값) · 세로(`9:16`) 화면비를 지원함.
	- 초당 $0.023인 360p(1,931 tokens/s)나 $0.07인 720p(5,792 tokens/s)로 초안을 잡고 편집을 마친 뒤 최종본만 1080p($0.104/s)나 4K($0.209/s)로 업스케일함 (4MB 초과 영상은 `delivery="uri"`로 폴링 다운로드).
	→ 초안 탐색 단계의 토큰 소모를 아끼면서 최종본은 광고나 방송용 고해상도로 확보함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 (Gemini Omni 1.1 Flash) : 단일 생성 길이가 최대 10초였고 비디오 출력 단가가 1M 토큰당 $17.50(720p 초당 약 $0.10)였으며, 5단계 조명 전시 포스터 애니메이션 같은 다층 프롬프트에서 참조 이미지 일치도가 상대적으로 낮고 카메라 전환 시 시각적 변형이나 원치 않는 점프컷이 더 자주 발생했음.
- 이번 방식 (Gemini Omni 1.2 Flash) : 단일 생성 · 편집 길이가 3 ~ 15초(1초 단위 지정)로 늘어났고 비디오 출력 단가를 1M 토큰당 $12.00(720p 초당 약 $0.07)로 낮췄으며, 참조 미디어 준수력과 연속 드론 비행 궤적 제어 · 다중 화자 립싱크를 개선함.
→ 출력 단가 인하와 멀티턴 부분 편집 · 저해상도 초안 워크플로가 맞물려 반복 수정 비용이 내려갔고 4주 전환 기간 뒤 2026.12.03부터는 `gemini-omni-1.1-flash` 호출도 코드 변경 없이 1.2 모델과 요금으로 자동 전환됨.

# 숫자로 보면
| 항목 | 이전 (Gemini Omni 1.1 Flash) | 이번 (Gemini Omni 1.2 Flash) | 출처 |
|---|---|---|---|
| 단일 생성 · 편집 최대 길이 | 10초 | 15초 (3 ~ 15초, 1초 단위 설정 / 기본값 10초) | DeepMind Blog / AI Studio Docs |
| 비디오 출력 토큰 단가 (1M 토큰당, 유료 티어) | $17.50 | $12.00 (입력 $1.50 · thinking 포함 텍스트 출력 $9.00은 동일) | AI Studio Pricing |
| 720p 비디오 초당 유효 가격 | 약 $0.10/s (5,792 tokens/s) | 약 $0.07/s (30% 인하, 10초 약 $0.70 · 15초 약 $1.04) | DeepMind Blog / AI Studio Pricing |
| 해상도별 초당 토큰 · 가격 (360p / 1080p / 4K) | 원문에 없음 | 360p : 1,931 tokens/s ($0.023/s) / 1080p : 8,688 tokens/s ($0.104/s) / 4K : 17,376 tokens/s ($0.209/s) | AI Studio Pricing |
| 참조 미디어 최대 개수 | 원문에 없음 | 참조 이미지 최대 6장(캐릭터 최대 2명 · 인당 3장) / 참조 비디오(클립당 최대 3초) 3 ~ 10초 생성 시 최대 3개 · 11 ~ 15초 생성 시 최대 1개 | AI Studio Docs |
| 키프레임 보간 · 비디오 연장 길이 | 원문에 없음 | 첫 · 끝 프레임 보간 3 ~ 10초 / 비디오 연장 턴당 3 ~ 10초 (최대 총 30초) | AI Studio Docs |

# 주의할 점 / 한계
- 원문이 밝힌 생성 한계 : 빠른 스포츠 액션 · 급격한 대본 변화 · 복잡한 물리 현상 표현은 아직 개선 중임.
- 오디오 레퍼런스 제약 : DeepMind 블로그에서는 1초 음성 레퍼런스 예시를 소개했으나 Cloud 블로그는 허용 목록(allowlisting) 승인 대상이라고 명시했고 AI Studio 문서 기준으로는 현재 API에서 오디오 입력 · 음성 편집 · 참조 비디오 오디오 반영을 지원하지 않음.
- 편집 및 연장 제약 : 편집 입력 영상은 15초 이하여야 하고 첫 · 끝 프레임 보간은 3 ~ 10초까지만 작동하며 비디오 연장은 클립 끝에만 이어 붙일 수 있음. 업로드 영상에 대화 장면이 있으면 새 대사를 추가하는 연장이 불가하며(무음 유지 또는 모델 생성 영상의 `previous_interaction_id` 멀티턴 연장은 대사 생성 가능), 참조 비디오는 신규 생성 시에만 지원되고 다중 비디오 동시 참조는 불가함.
- API 파라미터 및 과금 · 환경 조건 : `system_instruction` · `temperature` · `top_p` · `stop_sequences` · 별도 `negative_prompt` 파라미터와 YouTube URL 입력을 지원하지 않으며 `store=false` 설정 시 후속 멀티턴 편집이 불가함. 요금은 유료 티어 출력 토큰 기준(무료 티어 미제공)이며 Provisioned Throughput은 Google Cloud에서만 제공되고 EEA · 스위스 · 영국에서는 업로드 비디오의 편집 · 연장 및 미성년자 이미지 편집이 제한됨(공식 언어 평가는 영어만 완료).
- 아직 확인 안 된 것 : 모델 파라미터 규모 · 내부 아키텍처 세부 구조 · 외부 정량 벤치마크 점수는 원문에 없음.

# 정리
- 네이티브 생성 길이를 15초로 늘리고 720p 초당 단가를 $0.07로 30% 낮추면서 Interactions API 기반 멀티턴 편집과 30초 연장 기능을 정식 출시(GA)로 묶어낸 업데이트임.
- 360p($0.023/s) 초안 생성과 `previous_interaction_id` 기반 부분 수정으로 전체 클립을 처음부터 다시 생성하는 비용을 줄일 수 있어 제품 카탈로그 회전 영상이나 15초 광고 · 가상 피팅 영상 제작 파이프라인에 써먹을 만함.

# 참고
- [Gemini Omni 1.2 Flash: Fast and cost-effective with longer clips](https://deepmind.google/blog/gemini-omni-12-flash-fast-and-cost-effective-with-longer-clips/) — Google DeepMind Blog
- [Gemini Developer API pricing — Gemini Omni 1.2 Flash](https://aistudio.google.com/docs/pricing#gemini-omni-1-2-flash) — Google AI Studio Docs
- [Generate and edit videos with Gemini Omni Flash](https://aistudio.google.com/docs/omni) — Google AI Studio Docs
- [Gemini Omni 1.2 Flash now GA: cost-effective video](https://cloud.google.com/blog/products/ai-machine-learning/gemini-omni-1-2-flash-generally-available) — Google Cloud Blog
