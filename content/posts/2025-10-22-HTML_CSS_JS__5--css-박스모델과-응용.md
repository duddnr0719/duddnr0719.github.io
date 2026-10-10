---
weight: 42
title: "5. CSS 박스모델과 응용"
date: 2025-10-22T12:00:00+09:00
categories: ["HTML/CSS/JS"]
draft: false
order: 4
---

## 박스모델
<columns>
<column ratio="100">- HTML 요소들을 박스 형태로 그리는 것
- 박스는 배치, 색상, 경계 등의 속성을 가진다.
### 경계선 속성을 한 줄로 정의
→ border: (두께) (스타일) (색상)
---
- border-radius 속성을 사용하여 경계선을 둥글게 만들 수 있다.
- border-image 속성을 사용하면 이미지로 경계선을 만들 수 있다. (9구역)</column>
<column ratio="100">![](/images/d3c5d8eea7373de3.png)</column>
</columns>
## 요소 크기 설정
- CSS에서는 모든 요소의 크기를 width, height 속성을 이용하여 설정할 수 있다.
  - auto : 브라우저가 크기를 계산한다. 디폴트값.
  - length : 크기를 px, pt, cm 단위로 지정할 수 있다.
  - % : 크기를 컨테이너 블록의 퍼센트로 지정한다.
  - initial : 크기를 디폴트값으로 설정한다.
  - inherit : 마진이 부모 요소로부터 상속된다.
## 마진 설정
- auto : 브라우저가 마진을 설정한다.
- length : 마진을 px, pt, cm 단위로 지정할 수 있다. 디폴트는 0px.
- % : 마진을 요소 폭의 퍼센트로 지정한다.
- inherit : 마진이 부모 요소로부터 상속된다.
## 패딩 설정
- length : px, pt, em 단위로 패딩을 설정한다.
- % : 패딩을 내용물의 퍼센트로 지정한다.
- padding-top,right,bottom,left 를 사용하여 각 변에대한 값을 지정할 수 있다.
## 수평 정렬
### 인라인 요소
: 컨텐츠의 크기만큼만 자리를 차지하는 요소
→ 인라인 요소를 컨테이너의 중앙에 놓으려면 컨테이너의 text-align 속성을 사용한다.
### 블록 요소
: 한 줄을 다 차지하는 요소
→ 블록 요소를 중앙 정렬하려면 왼쪽 마진과 오른쪽 마진을 auto로 설정한다.
## 배경 설정
- background : 한 줄에서 모든 배경 속성을 정의한다.
- background-attachment : 배경 이미자가 고정되어 있는지, 스크롤 되는지를 지정한다.
- background-color : 배경색을 정의한다.
- background-image : 배경 이미지를 정의한다.
- background-position : 배경 이미지의 시작 위치를 지정한다.
- background-repeat : 배경 이미지의 반복 여부를 지정한다.
## 링크 스타일
- a:link → 방문되지 않은 링크의 스타일
- a:visited → 방문된 링크의 스타일
- a:hover → 마우스가 위에 있을 때의 스타일
- a:active → 마우스로 클릭되는 때의 스타일
## 테이블 스타일
- border : 테이블의 경계선
- border-collapse : 이웃한 셀의 경계선을 합칠 것인지 여부
  → collapse : 이웃하는 셀의 경계선을 합쳐서 단일선으로 표시
  → separate : 이웃하는 셀의 경계선을 합치지 않고 분리하여 표시
- width : 테이블의 가로 길이
- height : 테이블의 세로 길이
- border-spacing : 테이블 셀 사이의 거리
- empty-cells : 공백 셀을 그릴 것인지 여부
- table-align : 테이블 셀의 정렬 설정
