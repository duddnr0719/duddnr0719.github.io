---
title: "About"
---

# About

**레옴(박영욱)** 의 노트.
순천향대학교 컴퓨터공학과에서 공부하고, 효율컴퓨팅 연구실(ECLab)에서 학부연구생으로 있음.
AI 모델을 만들고, 그 모델이 실제로 돌아갈 서버와 엣지 보드까지 같이 다루는 걸 좋아함.

## 요즘 하는 것
- **의료 영상 AI** — 흉부 X-ray 결핵 진단 (TREAT-MMTB 2026, MICCAI 2026 챌린지 제출), CT로 합성한 X-ray 학습 연구
- **엣지 LLM** — Jetson에서 LLM 돌리기 : GRPO 파인튜닝한 3B 모델로 센서 이상 감지 (MIRU 2026 포스터 1저자), 27B 1-bit 모델을 Jetson Orin NX 16GB에서 서빙
- **GPU 클러스터 운영** — 연구실 GPU 6장 Slurm 클러스터 설계 · 운영, AI 에이전트가 Slurm으로 잡을 내게 하는 MCP 서버
- **AI 에이전트** — Claude Code · Opencode · Hermes로 여러 에이전트에 작업을 나눠 맡기는 환경

## 이 블로그에는
- **스터디 노트** — 운영체제, 데이터구조, 컴퓨터네트워크, 데이터베이스, 컴퓨터비전, 인공지능, 빅데이터분석 등 전공 정리. 카테고리 안에서는 1장부터 순서대로 보임.
- **AI 리포트** — 최신 AI 기술 소식 중 하나를 골라 원문(공식 블로그 · 논문 · 모델 카드)을 읽고 정리한 글. 가능하면 연구실 장비로 직접 써본 결과도 같이 붙임.
	- 원문 수집과 초안은 연구실 에이전트 파이프라인(Hermes + Gemini)이 돕고, 모든 수치에 출처가 있는지 · 원문에 없는 내용이 없는지 검사를 통과한 글만 올라감.
- **구축기 · 도구 정리** — 쿠버네티스, AI 코딩 에이전트, Git 등

## 공개 프로젝트
- [mmtb-task2-tb-cxr](https://github.com/duddnr0719/mmtb-task2-tb-cxr) — 흉부 X-ray 결핵 진단, 데이터 누수 진단부터 Docker 제출본까지
- [edge-llm-iot-anomaly](https://github.com/duddnr0719/edge-llm-iot-anomaly) — GRPO 파인튜닝 소형 LLM으로 IoT 센서 이상 감지 (MIRU 2026)
- [bonsai-27b-jetson](https://github.com/duddnr0719/bonsai-27b-jetson) — 27B 1-bit LLM을 Jetson Orin NX에서 돌리는 재현 가이드
- [f1-project](https://github.com/duddnr0719/f1-project) — FIA 규정 RAG + 실시간 레이스 데이터 에이전트

## 연락
- Email : [duddnr0719@gmail.com](mailto:duddnr0719@gmail.com)
- GitHub : [@duddnr0719](https://github.com/duddnr0719)
