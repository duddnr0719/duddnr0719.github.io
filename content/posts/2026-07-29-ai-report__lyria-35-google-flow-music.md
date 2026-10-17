---
weight: 149
title: "Lyria 3.5 — 감정 보컬과 템포 제어로 최대 3분 곡을 만드는 음악 생성 모델"
date: 2026-07-29T12:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 텍스트 프롬프트 하나로 최대 3분짜리 완곡을 작곡하고 가사와 보컬 감정까지 디렉팅한다 ! 구글 딥마인드가 Flow Music에 얹은 최신 음악 생성 모델을 뜯어보자.

# 개요
- 무엇 : Google DeepMind와 Google Labs가 2026.07.29 공개한 최신 음악 생성 모델 Lyria 3.5 및 웹 기반 창작 스튜디오 Google Flow Music
- 한 줄 정의 : Lyria 3.5는 복합 멜로디 구조와 감정 보컬, 템포 및 재생 길이 제어 기능을 결합해 최대 3분 길이의 완곡을 작곡하는 프런티어 음악 생성 모델이다.
- 원문 : [We’re launching Lyria 3.5 in Google Flow Music, with advances across musicality, lyrics, vocals, and creative control.](https://deepmind.google/blog/were-launching-lyria-35-in-google-flow-music-with-advances-across-musicality-lyrics-vocals-and-creative-control/)

# 그래서 도대체 뭔데 ?
- Lyria 3.5는 복합 멜로디 구조와 구조 인식 가사, 감정 뉘앙스를 반영한 보컬 합성 및 템포 · 재생 길이 제어를 통합한 음악 생성 모델임.
- 웹 스튜디오인 Google Flow Music을 통해 프로듀서와 대화하듯 편곡하고, 스템 분리와 Veo 영상 연동까지 묶었음.
	- 💡 프런티어 음악 모델 : 멜로디 구조 · 화성 · 가사 · 보컬 감정을 통합 생성하는 최신 음악 파운데이션 모델
	- 💡 스템 분리 (Stem split) : 완성된 음악 파일에서 보컬, 베이스, 드럼, 기타 등 개별 악기 트랙을 독립적으로 추출해 분리하는 기술
	- 💡 SynthID : 사람이 들을 수 없는 비가청 디지털 워터마크를 생성 시점에 삽입해 음질 손상 없이 AI 생성물 여부를 추적하는 기술

# 어떻게 동작하나 ?
1. 텍스트 프롬프트 및 멀티모달 입력
	- 원하는 장르 · 악기 구성 · 분위기, 템포(BPM) 및 조성(Key)을 자연어로 입력하거나 이미지를 업로드함
	- 대화형 프로듀서(Chat with Producer) 창을 통해 피드백을 전달하며 요구사항을 단계적으로 구체화함
	→ 대화형 프롬프트와 이미지 입력을 바탕으로 곡 구성이 시작됨
2. Lyria 3.5 코어 생성 엔진
	- 향상된 음악성(Musicality)을 바탕으로 복합 멜로디 구조를 자연스럽게 전개함
	- 벌스와 코러스 같은 곡 구조(structural awareness)를 인식해 가사를 배치하고 명확한 발음과 감정 실린 보컬을 합성함
	- 60초 클립부터 최대 3분 완곡까지 지정한 재생 길이(duration)에 맞춰 곡이 자연스럽게 이어지도록 생성함
	→ 지정한 길이에 맞춰 자연스럽게 이어지는 트랙이 생성됨
3. 스튜디오 후가공 및 확장 연동 (Flow Music)
	- 생성된 곡에 대해 오디오 이펙트 적용, 리믹스, 스템 분리(Stem split)를 거쳐 개별 트랙 단위로 편집함
	- Veo 비디오 생성 모델과 연동해 음악의 분위기와 캐릭터에 어울리는 뮤직비디오를 자체 제작함
	- 모든 생성 음원에 SynthID 비가청 디지털 워터마크를 자동으로 삽입함
	→ 별도 외부 툴 없이 스튜디오 안에서 음악 편집부터 영상화, 저작물 식별까지 한 번에 끝냄

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 장르 탐색 및 사운드스케이프 중심 생성, 세부 곡 구조 및 템포 · 길이 제어 제약
- 이번 방식 : 60초부터 최대 3분까지 가변 길이 완곡 생성, 감정 뉘앙스와 발음이 개선된 보컬, 템포(BPM) 및 조성 지정 지원
→ 곡의 구조 인식과 세부 제어 인터페이스를 강화하고, 스튜디오 플랫폼(Flow Music)과 워터마킹(SynthID)을 하나로 엮었기 때문

# 숫자로 보면
| 항목 | 이전 | 이번 | 출처 |
|---|---|---|---|
| 생성 곡 재생 길이 | - | 60초 ~ 최대 3분 (가변 제어) | DeepMind 모델 페이지 |
| 템포(BPM) 제어 지원 | - | 프롬프트로 지정 지원 (예: 82, 90, 95, 108, 110, 130–135 BPM) | DeepMind 모델 페이지 |
| 오디오 워터마킹 누적 실적 (SynthID) | - | 240,000년 분량 | Google 공식 블로그 |
| 이미지 및 비디오 워터마킹 실적 (SynthID) | - | 1800억 개 이상 | Google 공식 블로그 |
| 쇼케이스 앨범 수록 곡 수 | - | 8 ~ 15곡 (Fog Harbor 12, Golden Afternoon 8, Crystal Sky 15) | Flow Music 공식 사이트 |

# 주의할 점 / 한계
- 원문이 스스로 밝힌 한계 : 여러 장르의 음악을 생성할 수 있으나 핵심 기능은 여전히 개선 중인 단계임. 생성 트랙이 의도한 방향에 맞는지 직접 확인할 필요가 있음
- 수치 및 벤치마크 조건 : 정량적인 객관적 음질 평가 점수(벤치마크 지표)는 원문에 공개되지 않았음 (원문에 없음)
- 곡 길이 상한 : 재생 길이를 유연하게 조절할 수 있으나 단일 생성 최대 상한은 3분으로 제한됨
- 플랫폼 이용 환경 : Flow Music 웹 스튜디오를 통해 일일 크레딧(Daily credits) 기반으로 제공됨

# 정리
- 텍스트와 이미지 입력으로 최대 3분짜리 완곡을 작곡하며, 감정 보컬과 템포 제어력까지 지원함.
- 웹 기반 스튜디오(Flow Music)에서 스템 분리, 리믹스, Veo 비디오 연동을 한곳에 묶었음.
- 배경음악이나 프로젝트 음원을 빠르게 구상하려는 음악 창작자가 써먹을 만함.

# 참고
- [We’re launching Lyria 3.5 in Google Flow Music, with advances across musicality, lyrics, vocals, and creative control.](https://deepmind.google/blog/were-launching-lyria-35-in-google-flow-music-with-advances-across-musicality-lyrics-vocals-and-creative-control/) — Google DeepMind 공식 블로그
- [Google Flow Music](http://flowmusic.google/) — Flow Music 공식 사이트
- [Lyria 3.5](https://deepmind.google/models/lyria/) — Google DeepMind 모델 페이지
- [TIME has named Google SynthID one of the Best Inventions of 2026.](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/synthid-time-best-inventions/) — Google 공식 블로그
