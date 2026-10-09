---
weight: 43
title: "6. CSS 레이아웃과 애니메이션"
date: 2025-10-22T12:00:00+09:00
categories: ["HTML/CSS/JS"]
draft: false
---

## 레이아웃
: 웹페이지에서 HTML 요소의 위치, 크기 등을 결정하는 것
## 박스모델
: 웹 브라우저가 각 요소들을 화면에 그릴 때는 무조건 사각형으로 간주한다는 것. → 사각형에는 패딩, 경계선, 마진이 붙어있다.
### 블록 요소
: 화면의 한 줄을 전부 차지한다.
→ <h1>, <p>, <ul>, <li>, <table>, <blockquote>, <pre>, <div>, <form>, <header>, <nav>
### 인라인 요소
: 한 줄에 차례대로 배치된다. 현재 줄에서 필요한 만큼의 너비만을 차지한다. 위치나 크기 설정 무시
→ <a>, <img>, <strong>, <em>, <br>, <input>, <span>
### 인라인 블록 요소
: 기본적으로 인라인 요소처럼 줄바꿈 없이 한 줄에 다른 요소들과 함께 배치된다. 하지만 블록 요소처럼 위치와 크기 설정이 가능하다.
→ 인라인 요소처럼 동작 : 한 줄에 여러 개의 요소가 나란히 배치된다. ⇒ 다른 요소와 같은 줄에 위치할 수 있다.
→ 블록 요소처럼 동작 : 블록 요소의 특성인 width, height, margin, padding 등을 설정할 수 있다.
## display 속성
: 블록, 인라인, 인라인 블록, 안보임 중 하나를 선택한다.
→ 속성 display를 block으로 설정하면 블록 요소처럼 배치한다.
- display:block : 블록
- display:inline : 인라인 
- display:none : 없는 것으로 간주
- display:hidden : 화면에서 감춤
- display:inline-block
## 요소의 크기 설정
: width, height 속성으로 결정된다.
- width, height : 요소의 크기
- min-width, min-height : 요소의 최소 크기
- max-width, max-height : 요소의 최대 크기
## 대체 박스 모델
<columns>
<column ratio="100">: width, height이 패딩과 경계선을 포함한다.
→ box-sizing:border-box;
→ 요소의 패딩과 테두리가 요소의 지정된 너비와 높이 안에 포함되도록 크기를 계산할 수 있다.
→ 기본적으로 요소의 크기를 계산할 때는 content-box라는 모델이 사용되며 이 방식에서는 요소의 width, height이 콘텐츠 영역만을 의미한다. ⇒ 패딩과 테두리는 이 크기에서 추가적으로 더한다.
→ 대체 박스 모델에서는 다음의 방식으로 크기가 계산된다.</column>
<column ratio="100">![](/images/e218a5e598ef0dbc.png)</column>
</columns>
## 위치 설정 방법
- 정적 위치 설정 - 정상적인 흐름에 따른 배치
  → 블록 요소들은 박스처럼 상하로 쌓이게 되고 인라인 요소들은 한 줄에 차례대로 배치
  → 정적 위치 설정은 top, bottom, left, right 속성의 영향을 받지 않는다.
- 상대 위치 설정 - 정상적인 위치가 기준점이 된다.
  → 정상적인 위치에서 상대적으로 요소가 배치되는 방법 ⇒ 원래의 위치에서 px만큼 떨어진 곳에 위치, 원래 위치에 다른 콘텐츠가 올 수 없음
- 절대 위치 설정 - 컨테이너의 원점이 기준점이 된다.
  → 전체 페이지를 기준으로 하는 배치 방법. ⇒ 페이지의 시작 위치에서 top, left, bottom, right 만큼 떨어진 위치에 배치된다.
- 고정 위치 설정 - 화면의 원점이 기준점이 된다.
  → 화면을 기준으로 하는 배치 방법. ⇒ 화면 시작 위치에서 top, left, bottom, right 만큼 떨어진 위치에 배치된다.
## float 속성
: 하나의 콘텐츠 주위로 다른 콘텐츠들이 물처럼 흘러가는 스타일 지정
### clear 속성
: float 속성을 중단할 때 사용
→ float 속성이 clear되지 않으면 비어있는 부분을 채우기 위해 float 속성이 적용된 콘텐츠가 물 흐르듯 빈 곳을 채우려 한다.
## z-index
<columns>
<column ratio="100">: 요소의 스택 순서를 지정한다.</column>
<column ratio="100">![](/images/a6ef134f8fe6b4ec.png)</column>
</columns>
## overflow 속성
: 자식 요소가 부모 요소의 범위를 벗어났을 때 어떻게 처리할 것인지를 지정한다.
→ overflow 속성을 설정하지 않으면 자식 요소의 콘텐츠가 부모 요소의 범위까지 넘쳐버린다.
- hidden : 넘어가는 콘텐츠는 보이지 않는다.
- scroll : 스크롤하여 모든 콘텐츠를 볼 수 있다.
