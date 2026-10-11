---
weight: 135
title: "EmbeddingGemma 2 — 텍스트부터 영상까지 하나로 묶는 740M 온디바이스 멀티모달 임베딩"
date: 2026-10-11T22:00:00+09:00
categories: ["AI 리포트"]
draft: false
---

> 텍스트 · 이미지 · 비디오 · 오디오를 단일 768차원 벡터 공간으로 묶고 모듈러 구조로 모바일에서 텍스트 전용 191MB(전체 567MB) 메모리로 구동되는 오픈 멀티모달 임베딩 모델 등장 !

# 개요
- 무엇 : Google DeepMind가 2026.10.06에 오픈 가중치 멀티모달 임베딩 모델 EmbeddingGemma 2를 발표함.
- 한 줄 정의 : EmbeddingGemma 2는 Gemma 4 아키텍처를 기반으로 텍스트 · 코드 · 이미지 · 비디오 · 오디오를 768차원 벡터 공간에 통합하는 740M 파라미터 온디바이스 임베딩 모델이다.
- 원문 : [EmbeddingGemma 2: an open, lightweight multimodal embedding model](https://deepmind.google/blog/embeddinggemma-2-an-open-lightweight-multimodal-embedding-model/)

# 그래서 도대체 뭔데 ?
- 텍스트뿐만 아니라 코드 · 이미지 · 비디오 · 오디오를 단일 임베딩 공간에서 직접 비교할 수 있게 만든 모델임.
- 기존처럼 이미지 캡셔닝이나 음성 인식(STT) 모델을 거치는 중간 변환 없이 원본 미디어를 바로 벡터로 변환함.
- 텍스트 270M · 비전 170M · 오디오 300M 인코더를 분리 설계해 필요한 모달리티만 골라 메모리에 올릴 수 있음.
- MRL(Matryoshka Representation Learning) 기법을 기본 탑재해 768차원 출력을 128차원까지 잘라내 벡터 저장소 용량을 최대 6배 줄임 (256차원까지 품질 유지).
	- 💡 MRL (Matryoshka Representation Learning) : 벡터 앞부분에 중요한 표현 정보를 집중시켜 뒤쪽을 잘라내도 유사도 검색 성능을 보존하는 임베딩 학습 기법
	- 💡 온디바이스 멀티모달 임베딩 : 외부 클라우드 통신 없이 기기 내부에서 텍스트 · 이미지 · 오디오를 단일 벡터 공간으로 변환하는 기술

# 어떻게 동작하나 ?
1. 모듈러 인코더 분기와 선택적 적재
	- 텍스트 · 코드는 270M 백본(130M 트랜스포머 + 140M 임베더)이 담당함.
	- 시각 데이터는 170M 비전 인코더, 음성은 300M 오디오 인코더가 16kHz 모노 오디오를 처리함.
	- 텍스트 전용(270M)부터 전체 멀티모달(740M)까지 필요한 인코더만 골라 로드함.
	→ 배포 환경의 메모리 제약에 맞춰 모델 크기를 최적화함.

2. 공용 8192 토큰 컨텍스트와 인터리빙
	- 모든 모달리티가 단일 8192 토큰 컨텍스트 윈도우를 공유함.
	- 텍스트 서브워드당 1 토큰, 이미지 기본 280 토큰(최대 29장), 비디오 프레임당 140 토큰, 오디오 초당 25 토큰(최대 327초)을 소모함.
	- `<|image|>`, `<|video|>`, `<|audio|>` 토큰으로 텍스트 중간에 미디어를 삽입함.
	→ 텍스트 설명과 사진 · 영상이 뒤섞인 복합 문서를 단일 벡터로 인코딩함.

3. 트랜스포머 백본과 MRL 프로젝션
	- 24개 레이어, 히든 차원 2048, 모델 차원 512를 거쳐 프로젝션 레이어에서 768차원 공간으로 투영함.
	- 768차원 출력을 512 · 256 · 128차원으로 잘라내고 L2 재정규화를 거침.
	→ 동일한 벡터 공간 안에서 자연어 검색어로 이미지나 비디오 구간을 즉각 탐색함.

# 기존이랑 뭐가 다른가 ?
- 이전 방식 : 멀티모달 검색을 위해 음성을 텍스트로 바꾸는 STT 모델이나 이미지 캡셔닝 모델을 앞에 두고 텍스트 임베딩 모델로 전달하는 파이프라인 방식을 씀.
- 이번 방식 : 단일 모델 안에서 텍스트 · 코드 · 이미지 · 비디오 · 오디오를 직접 인코딩하고 필요한 모달리티 인코더만 270M ~ 740M 크기로 선택 적재함.
→ 모델을 여러 개 띄우는 메모리 낭비와 단계별 직렬화 지연이 사라지고 오프라인 환경에서 기기 자체 교차 모달리티 검색이 가능해짐.

# 숫자로 보면
| 항목 | 이전 (EmbeddingGemma 1) | 이번 (EmbeddingGemma 2) | 출처 |
|---|---|---|---|
| 전체 파라미터 | - | 740M (텍스트 270M / 비전 170M / 오디오 300M) | DeepMind 공식 블로그 |
| 지원 모달리티 | 텍스트 (단일) | 텍스트 · 코드 · 이미지 · 비디오 · 오디오 (4개 모달리티) | 모델 카드 |
| 컨텍스트 길이 | 2048 토큰 | 8192 토큰 (4배 확장) | DeepMind 공식 블로그 |
| MTEB Code (v1) | 68.76 | 78.68 (9.92 포인트 향상) | DeepMind 공식 블로그 |
| MTEB Multilingual (v2) | 61.15 | 61.36 | 모델 카드 |
| MTEB Code (v1, 256d) | - | 76.18 | 모델 카드 |
| MTEB Code (v1, 128d) | - | 71.41 (저장 공간 6배 절감) | 모델 카드 |
| Pixel 11 Pro RAM (양자화) | - | 191MB (텍스트) / 567MB (전체 모달리티) | DeepMind 공식 블로그 |
| M5 Pro GPU 지연 (70 비전 토큰) | - | 37.3ms (비전 임베딩, 초당 26.9개 이미지) | AI Edge 공식 블로그 |

# 주의할 점 / 한계
- 연산 정밀도 제한 : 반드시 bfloat16 또는 float32를 써야 함. float16 사용 시 활성화 값이 동적 범위를 넘어 경고나 에러 없이 NaN이 반환되거나 임베딩 품질만 조용히 떨어짐.
- MRL 차원 축소 후 L2 재정규화 필수 : 768차원에서 512 · 256 · 128차원으로 슬라이싱하면 단위 벡터 길이가 깨지므로 코사인 유사도 계산 전에 반드시 재정규화해야 함. 생략 시 오류 없이 랭킹 정확도만 떨어짐.
- 128차원 축소 시 멀티모달 품질 급락 : 256차원까지는 성능 보존이 양호하지만 128차원에서는 MMEB v2 점수가 59.01에서 45.65로, MSEB 음향 검색 점수가 69.54에서 56.71로 크게 떨어짐. 128차원은 텍스트 전용 작업에 국한하는 편이 안전함.
- 작업 지시어 접두사 의존성 : 텍스트 작업 시 검색 질의(`SearchQuery`)나 코퍼스 문서(`Document`), 코드 검색(`CodeRetrieval`) 같은 작업별 지시어 접두사를 생략하면 임베딩 정밀도가 저하됨 (이미지 · 비디오 · 오디오는 접두사 없이 전달).
- 사후 안전성 정렬 미적용 : 생성 모델과 달리 사후 정렬이나 안전 튜닝을 거치지 않으며 사전 학습 데이터 필터링에만 의존함. 애플리케이션 단에서 검색 결과 필터링을 직접 설계해야 함.

# 정리
- 거대한 클라우드 인프라 없이도 모바일과 엣지 장비에서 텍스트 · 코드 · 이미지 · 비디오 · 음성을 단일 벡터 공간으로 묶어 검색할 수 있는 경량 모델임.
- 기기 내부 로컬 RAG 파이프라인 · 시맨틱 코드 검색기 · 개인 미디어 아카이브 탐색기를 개발하려는 엔지니어에게 실용적인 선택지임.

# 참고
- [EmbeddingGemma 2: an open, lightweight multimodal embedding model](https://deepmind.google/blog/embeddinggemma-2-an-open-lightweight-multimodal-embedding-model/) — Google DeepMind
- [EmbeddingGemma 2 model card](https://ai.google.dev/gemma/docs/embeddinggemma/model_card_2) — Google DeepMind
- [EmbeddingGemma 2: The Developer Guide](https://developers.googleblog.com/en/embeddinggemma-2-the-developer-guide/) — Google Developers Blog
- [Bring multimodal semantic search to the edge with EmbeddingGemma 2](http://developers.googleblog.com/google-ai-edge-with-embeddinggemma-2) — Google AI Edge
