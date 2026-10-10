---
weight: 124
title: "2장 OpenCV와 Python 개발 환경 (설치, PyCharm, 첫 OpenCV 프로그램)"
date: 2026-10-10T12:00:00+09:00
categories: ["컴퓨터비전"]
draft: false
---

> Python 설치(PATH 체크) → PyCharm에 인터프리터 연결 → opencv-python, matplotlib 설치 → NumPy 배열을 만들어 cv2.imshow로 띄우면 환경 준비 끝. OpenCV 영상은 그냥 NumPy 배열이다. (OpenCV 소개·버전 표는 1장 참고)
### Python
- 귀도 반 로섬(1991), 한 줄씩 실행하는 **인터프리터** 언어, 동적 타입, 객체지향, 플랫폼 독립
- 설치: python.org → Downloads → 설치 첫 화면에서 **Add Python to PATH** 체크 → Customize installation으로 경로 지정(예: `C:\Python`)
- 대화형 셸
```text
>>> print('hello')
hello
>>> a = 5
>>> b = 10
>>> c = a + b
>>> c
15
```
- IDLE: Python에 기본 포함된 셸 + 에디터. File → New File → 저장(`hello.py`) → Run → Run Module(**F5**)
### PyCharm
- JetBrains(IntelliJ 기반) Python IDE. 프로젝트별 Python 버전·환경, 실행 결과 즉시 확인, 디버거, 운영체제 무관 UI
- Community(무료) / Professional(유료: 웹, DB 등 추가)
- 설치 옵션: 64-bit launcher(바탕화면 바로가기), Open Folder as Project(탐색기 우클릭), `.py` 연결, launchers를 PATH에 추가 (전부 체크해도 됨)
- 첫 실행: Do not import settings → 테마(Darcula 어둡게 / Light)
### 인터프리터와 프로젝트
- Settings → Project Interpreter → Add → **System Interpreter**에 `C:\Python\python.exe` 지정 (처음엔 `pip`, `setuptools`만 설치돼 있음)
- New Project
  - **Existing interpreter**: 시스템 Python 공유 (기본)
  - **New environment (venv)**: 프로젝트 안에 독립된 Python 복사본 → 프로젝트마다 라이브러리 버전을 따로 관리 가능
- 프로젝트 우클릭 → New → Directory(`chap02`) → New → Python File(`01.hello`) → `print("hello")` → Run
```text
C:\Python\python.exe D:/source/chap02/01.hello.py
hello

Process finished with exit code 0
```
- 터미널로 같은 일을 하려면
```bash
python -m venv venv               # 가상환경 생성
venv\Scripts\activate             # 활성화 (macOS·Linux: source venv/bin/activate)
pip install opencv-python matplotlib
```
### 라이브러리 설치
- PyCharm: File → Settings → Project: source → Project Interpreter → [+] → `opencv-python` 검색 → Install Package (특정 버전은 Specify version)
- `matplotlib`도 설치 (그래프·영상 표시용). 설치되면 의존성으로 `numpy` 등이 함께 들어옴
- 패키지 이름은 `opencv-python`, 코드에서 import 이름은 `cv2`
### 첫 OpenCV 프로그램
```python
import numpy as np
import cv2

image = np.zeros((300, 400), np.uint8)   # 300행(높이) × 400열(너비), 8비트 1채널
image.fill(200)                          # 전부 회색 200 (image[:] = 200)

cv2.imshow("Window title", image)        # 창 제목, 영상
cv2.waitKey(0)                           # 0: 키를 누를 때까지 무한 대기 (창이 실제로 그려지려면 필요)
cv2.destroyAllWindows()
```
- `shape`는 `(행, 열)` = `(높이, 너비)` 순서. 크기를 (너비, 높이)로 받는 `cv2.resize` 등과 순서가 반대라 헷갈리기 쉬움
- 파일 읽기
```python
path1 = r"Z:\open\Lenna.png"                       # r"" : 역슬래시를 이스케이프로 해석하지 않음
image = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)    # 흑백으로 읽기 (기본은 컬러 BGR 3채널)
if image is None:
    raise FileNotFoundError(path1)                 # 경로가 틀려도 에러 없이 None을 돌려줌
cv2.imshow("first", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
- 실수하기 쉬운 점 (OpenCV 4.13으로 확인)
  - `cv2.imread`는 파일이 없으면 **예외 없이 `None`** 반환 (경고만 출력) → 이후 `imshow`에서 엉뚱한 에러가 나므로 바로 검사
  - 컬러로 읽으면 shape이 `(300, 400, 3)`, 흑백이면 `(300, 400)`
  - 컬러 순서는 RGB가 아니라 **BGR** → matplotlib으로 보일 땐 `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`
  - Windows에서 **경로에 한글**이 있으면 `imread`가 None을 반환 → `cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)`로 우회
### 요약
- Python = 대화형 인터프리터, OpenCV = 영상 처리·비전·기계학습 API 라이브러리, PyCharm = 에디터·디버거·인터프리터를 통합한 IDE
- PyCharm은 프로젝트의 Python 인터프리터(`python.exe`)에 연결돼야 실행되고, 라이브러리는 Project Interpreter 화면에서 검색·설치
