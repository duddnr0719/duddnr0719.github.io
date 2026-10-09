---
weight: 53
title: "AI 코딩 에이전트 활용 (Opencode)"
date: 2026-02-20T12:00:00+09:00
categories: ["agent"]
draft: false
---

> Opencode는 터미널 환경에서 LLM을 활용해 코딩을 자동화하는 오픈소스 AI 에이전트 도구입니다.
# Opencode 개요
- 터미널 기반: IDE를 벗어나지 않고 효율적인 작업 가능
- 모델 자유도: Claude, OpenAI, Gemini 등 다양한 LLM 연동 지원
---
## 설치 및 설정
```
npm install -g opencode-google-antigravity-auth
nano ~/.config/opencode/config.json
```
config.json 설정 예시:
- reasoningEffort: 대답 노력도 (high)
- textVerbosity: 답변 상세 수준 (low)
---
## oh-my-opencode 에이전트
1. Sisyphus: PM 및 오케스트레이터 (작업 계획 및 분배)
1. Oracle: 아키텍처 설계 및 전략적 판단
1. Librarian: 공식 문서 및 코드베이스 탐색
1. frontend-ui-ux-engineer: UI/UX 중심 구현
