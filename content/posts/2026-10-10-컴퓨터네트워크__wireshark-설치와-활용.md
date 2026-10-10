---
weight: 57
title: "Wireshark 설치와 활용"
date: 2026-09-12T23:30:00+09:00
categories: ["컴퓨터네트워크"]
draft: false
---

> 패킷을 캡처해서 헤더를 계층별로 뜯어보면, 교재 속 프로토콜이 실제로 어떻게 오가는지 눈으로 확인할 수 있다.
### 패킷 분석기
- 네트워크 분석: 전달되는 트래픽을 캡처 → 해석(디코드)하는 행위. 패킷 분석기 = LAN 분석기 = 패킷 스니퍼.
- 덤프 분석: 캡처한 패킷의 의미를 알아보는 것.
- 하드웨어 분석기: 휴대형, 케이블 품질·오류 프레임 측정, 고가(기업용).
- 소프트웨어 분석기: NIC로 접속, 통계·보고·임계치 기능, 무료 많음 → 대표: Wireshark.
- 타인 통신 도청·악용은 법적 처벌 대상.
### Wireshark 개요
- Gerald Combs 개발, 원래 이름 Ethereal, GPL 오픈소스. Windows는 Npcap과 함께 써야 캡처 가능.
- 용도: 프로토콜 학습, 트러블슈팅, 보안 테스트, 프로토콜 구현 디버깅, 앱 품질 확인.
- 기능: 실시간 캡처, 프로토콜 상세 해석, 캡처 파일 저장/열기·변환, 조건 검색, 색상 규칙, 통계, 일부 암호화 프로토콜 복호화.
- 약점: 상용 대비 통계·경고 기능 약함(알림/메일 X), 네트워크를 직접 조작할 수 없음.
### 캡처 구조
- 패킷 캡처 드라이버: 소켓을 거치지 않고 NIC의 모든 패킷을 가져옴, 무차별(Promiscuous) 모드로 동작.
  - Npcap(Windows), libpcap(Unix/Linux), AirPcap(무선)
- 처리 요소
  - Wiretap: 저장된 추적 파일 입출력
  - dumpcap: 실제 캡처 엔진
  - 코어 엔진: 수천 개의 해석기(dissector)로 바이트 → 사람이 읽는 프레임으로 변환, 플러그인, 디스플레이 필터
  - GUI 툴킷이 화면 제공
### 설치
- wireshark.org → Download → Stable Release에서 OS에 맞는 설치 파일.
- 설치 중 Npcap 설치 체크 유지, USB 트래픽이 필요하면 USBPcap도 설치.
- 시작 화면: 캡처 필터 입력란 + 인터페이스 목록(선택 시 캡처 시작), Learn(가이드·위키·Q&A).
- CLI 도구: `tshark`(텍스트판 Wireshark), `editcap`(분할/편집), `mergecap`(결합), `reordercap`(타임스탬프 정렬), `capinfos`(파일 정보), `text2pcap`(텍스트→pcap), `rawshark`.
### 화면 구성
- 타이틀 바 / 메뉴 바 / 툴 바 / 디스플레이 필터 바
- 패킷 목록: 한 줄 = 한 프레임 요약(No, Time, Source, Destination, Protocol, Length, Info)
- 패킷 상세: 선택한 패킷을 계층별 트리로 디코드
- 패킷 바이트: 16진수 + ASCII (16진수 2글자 = 1바이트, 한 줄 16바이트)
- 상태 바: Expert 정보 색(청=정상, 황=주의, 적=오류), 코멘트, 선택 필드 정보, 패킷 수(전체/표시/마크), 프로파일
- 프로파일: 화면 구성·필터 등 설정 묶음을 저장/전환(기본값 Default)
### 실습: 홈페이지 접속 캡처
1. 인터페이스(이더넷) 선택 → 캡처 시작
1. 브라우저로 사이트 접속
1. Stop 후 디스플레이 필터로 제한 (예: `arp or dns or tcp or http`)
1. `GET / HTTP/1.1` 패킷의 바이트를 보면 Host, Connection: keep-alive, User-Agent, Accept-Encoding 등 요청 헤더가 ASCII로 보임
- Edit → Mark/Unmark 로 관심 패킷 표시 가능
### 헤더 읽기
- 상세 트리 순서: Frame → Ethernet II → Internet Protocol → TCP → HTTP. 한 패킷 안에 여러 계층 헤더가 캡슐화되어 있음.
- Frame: 실제 헤더가 아니라 Wireshark가 붙인 메타데이터(도착 시간, Epoch Time, 이전 프레임과의 시간차, Frame Number/Length, 프레임 내 프로토콜, 색상 규칙 등).
- 용어 구분
  - 프레임: MAC 헤더 ~ MAC 트레일러 전체
  - 패킷: IP 헤더 ~ 트레일러 직전 (분석이 대부분 IP부터라 '패킷 분석'이라 부름)
  - 세그먼트: TCP 헤더부터. 연결 설정 시 MSS 공유
- Ethernet II: 프리앰블(7B, 10101010…)·SFD(10101011)와 FCS(4B, 오류 검사)는 캡처에 보이지 않음. 트레일러 캡처 여부는 OS에 따라 다름.
- 해석 기준: TCP/IP는 RFC, LAN은 IEEE 규격.
### 덤프 분석
- 목적: 로그·오류 화면이 아닌 실제 통신 내용을 확인 → 개발 검증, 트래픽 조사, 프로토콜 학습.
- Statistics → Flow Graph로 통신을 '선(순서)'으로 보기. 웹 접속 시 흐름:
  1. DNS 질의/응답
  1. TCP 3-way handshake
  1. HTTP 요청 → ACK → `200 OK` 응답
  1. 서버 측, 클라이언트 측 TCP 연결 종료
- 주의
  - 환경(OS, 브라우저, 방화벽, ISP 라우팅 등)에 따라 매번 결과가 다름.
  - Windows는 백그라운드 통신이 많아 필터 필수.
  - ARP 캐시(기본 약 2분), DNS·브라우저 캐시 때문에 ARP/DNS/HTTP가 안 잡힐 수 있음 → 잠시 후 재시도, 캐시 삭제, 강력 새로고침.
  - 프록시 경유 시 프록시와의 통신이 잡힘.
