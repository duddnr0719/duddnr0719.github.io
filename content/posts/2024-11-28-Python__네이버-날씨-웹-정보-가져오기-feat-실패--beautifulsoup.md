---
weight: 37
title: "네이버 날씨 웹 정보 가져오기(feat.실패, BeautifulSoup)"
date: 2024-11-28T12:00:00+09:00
categories: ["Python"]
draft: false
---

# BeautifulSoup을 사용하여 네이버 날씨 웹의 정보를 가져와보자 !
## 크롤링 ? 스크래핑 ?
> 구글에 크롤링을 검색하면 ‘스크래핑’ 또한 같이 검색이 된다. 크롤링과 스크래핑의 연관된 점은 무엇이고 / 크롤링, 스크래핑 둘의 차이점은 무엇일까 ?
- 크롤링(Crawling): 크롤링은 웹사이트의 다양한 페이지를 방문하며 데이터를 포괄적으로 수집 및 저장하는 작업을 뜻함. 크롤러가 여러 웹페이지를 자동으로 탐색하며 URL을 추출하고 해당 페이지의 내용을 수집.
  → 주로 검색 엔진이나 웹 인덱스에서 사용되며, 큰 규모의 데이터 수집이 목적 !
- 스크래핑(Scraping): 스크래핑은 특정 웹페이지에서 필요한 정보를 추출하는 작업을 뜻함. 크롤링 이후에 스크래핑을 통해 추출된 데이터에서 필요한 정보만 가공함.
  → 주로 HTML 또는 XML 문서에서 데이터를 파싱하고 추출하는 기술을 사용 !
  - 크롤링 : 여러 웹페이지를 대상으로 하는 일반적인 데이터 수집 프로세스.
  - 스크래핑 : 특정 웹페이지에서 원하는 정보를 추출하는 구체적인 프로세스.
  → 스크래핑은 크롤링의 하위 개념이라고 생각하면 편하다.
  → 크롤링으로 상위 데이터(큰 규모의 데이터)를 수집하고 스크래핑으로 해당 데이터에서 하위 데이터(필요한 데이터)를 추출.
## 웹 스크래핑/크롤링 전 고려사항 ?
> 
- 웹 스크래핑/크롤링을 통해 어떤 목적을 달성하려는가?
  → 추출한 결과물을 상업적으로 사용하기 위해 저작권을 침해하지 않는지 고려해야 한다. 웹 사이트 이용 약관에서 스크래핑/크롤링을 금지하거나, 일부 제한을 두고 있을 수 있기 때문에 이용 약관을 반드시 확인해야 한다.

- 웹 스크래핑/크롤링이 서버에 영향을 미치는가?
  → 웹 스크래핑/크롤링을 하면 서버와의 통신을 필요로 하기 때문에 packet을 반복적으로 주고받는다. 이 과정이 딜레이 없이 진행될 경우 웹 서버에 불필요한 부하를 유발하게 되어 서버에서 차단하는 경우가 발생할 수 있기 때문에 적절한 딜레이를 적용해야 한다.
- 로봇 배제 표준(Robots Exclusion Standard)을 준수했는가?
  → 로봇 배제 표준은 웹 사이트의 소유자가 로봇에 대한 액세스 권한을 제어하는 데 도움을 주는 프로토콜이다. 웹 스크래핑/크롤링을 하기 전 “URL/robots.txt”를 통하여 robots.txt파일을 반드시 확인해야 한다.
## 정적 크롤링 vs 동적 크롤링
[정적 크롤링 vs 동적 크롤링](https://app.notion.com/p/1359d2cf1d148032bf66e6cb5738d4df)
위 글을 참고하자.
## BeautifulSoup 정복하기 👊
### BeautifulSoup ?
- HTML 및 XML 파일에서 데이터를 추출하기 위해 사용하는 라이브러리. 데이터를 추출하기 위해 사용할 수 있는 파싱된 페이지의 파스 트리를 만듦 → 웹 스크래핑에 사용하기 용이.
- 웹 사이트에서 데이터를 추출하기 전 먼저 웹 페이지의 내용을 가져와야 하는데, 이를 위해 requests 라이브러리를 같이 이용한다. → HTTP 요청을 보낼 수 있음.
### 💡파싱(Parsing)이란 ?
특정 형식의 데이터나 문서를 해석하고 분석하는 과정.
이 과정에서 데이터나 문서를 구성하는 구문을 분석하고 그 구문을 기반으로 의미 있는 정보를 추출하거나 원하는 형태로 재구성함.
### 💡파서(Parser)란 ?
파싱 과정을 수행하는 도구.
입력된 데이터나 문서를 특정 형식의 토큰으로 분리하고 이 토큰들의 구성 규칙을 바탕으로 파싱을 수행함.
❗️주로 문법적인 오류를 찾아내거나 입력된 데이터를 의미 있는 정보로 변환하는데 사용.
BeautifulSoup 또한 대표적인 파서이다.
## 간단한 예제를 통해 배워보자
```
import requests
from bs4 import BeautifulSoup

# 스크래핑할 URL 지정
url = "https://example.com/"

# 웹 페이지의 HTML을 가져옴
response = requests.get(url)
# HTML 파서를 이용하여 BeautifulSoup 객체 생성
soup = BeautifulSoup(response.content, "html.parser")

# 가져올 데이터 결정 -> 데이터 추출
headers = soup.find_all('h1')

# 가져온 데이터 출력 혹은 원하는 작업 수행
for header in headers:
    print(header.text)
```
1. requests를 사용하여 내용 추출
  ```
  # 웹 페이지의 HTML을 가져옴
  response = requests.get(url)
  ```
  → requests 라이브러리의 get()메소드를 사용하여 웹 사이트에 요청을 보낼 수 있음.
  → get() 메소드는 응답 객체를 반환하며, 웹 페이지의 내용, 상태 코드, 헤더 등을 추출할 수 있음.
1. BeautifulSoup을 사용하여 HTML 파싱
  ```
  # HTML 파서를 이용하여 BeautifulSoup 객체 생성
  soup = BeautifulSoup(response.content, "html.parser")
  ```
  → 웹 페이지의 HTML 내용을 추출한 후, 파서를 이용하여 파싱.
  페이지의 내용과 파서 라이브러리를 BeautifulSoup 생성자에 전달.
  → 위의 코드에선 ‘html.parser’가 파서에 해당.
1. BeautifulSoup을 사용하여 데이터 추출
  ```
  # 가져올 데이터 결정 -> 데이터 추출
  headers = soup.find_all('h1')
  
  # 가져온 데이터 출력 혹은 원하는 작업 수행
  for header in headers:
      print(header.text)
  ```
  → BeautifulSoup 객체를 통하여 HTML 문서의 태그에 계층적으로 접근할 수 있음.
  → 위 코드는 find_all() 메소드를 통하여 모든 ‘h1’ 태그를 찾고, text 속성을 사용하여 헤더의 텍스트만 가져옴.
- 점 표기법을 사용하여 HTML의 트리 구조를 탐색할 수 있음.
```
link = soup.div.a
```
→ ‘div’ 태그 안에 중첩된 첫 번재 ‘a’ 태그에 접근하는 코드
## 네이버 날씨 웹 스크래핑
- 네이버 날씨 웹페이지에서 주간예보를 크롤링 해보자.
```
import requests
from bs4 import BeautifulSoup

url = "https://weather.naver.com/"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

week_data = soup.find(("ul", {"class":"week_list"})).find_all("li", {"class":"week_list"})

print(week_data)
```
→ 위 코드를 실행하면 빈 list 출력된다.. 이유가 뭘까…
find_all() 메소드는 속성에 담긴 데이터를 리스트에 담아 리턴함. → 빈 리스트가 나오는 이유
그렇다면 class의 값이 잘못되어 찾는 값이 존재하지 않는 것인가..?
- 여러가지 검색을 해 본 결과 네이버 날씨 웹의 날씨 정보는 정적인 정보가 아닌 동적인 정보기 때문에 BeautifulSoup이 아닌 Selenium을 사용하여 크롤링을 해야 한다.
→ 동적인 정보는 JavaScript를 이용하여 페이지를 렌더링 하는데, requests, BeautifulSoup은 이를 처리하지 못한다.
### 따라서 이번 장에서는 BeautifulSoup을 사용하여 정적인 정보를 가진 네이버 뉴스 페이지의 뉴스 제목을 크롤링하는 프로그램을 만들어 볼 것이다.
```
import requests
from bs4 import BeautifulSoup

url = "https://news.naver.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 주요 뉴스 제목 추출
headlines = soup.select("div.main_content div.main_headline a")
for idx, headline in enumerate(headlines, start=1):
    print(f"{idx}. {headline.get_text().strip()}")
```
위의 코드를 실행하면 네이버 뉴스 웹 페이지의 뉴스 제목 텍스트만 추출되어 프린트 된다.
---
## 이번 장을 통해 배운 것들을 정리하자면..
→ 크롤링과 스크래핑은 같은 용어의 느낌이지만 엄밀히 따지자면 크롤링이 대주제이고 스크래핑이 소주제이다. (크롤링에 스크래핑이 포함되어 있다.)
→ 크롤링 / 스크래핑을 하기 전에는 문제가 될 요소들을 고려하여 진행해야 한다. 법적인 문제, 웹 페이지에 부담되는 것들 등등 ..
→ BeautifulSoup 라이브러리를 사용하는 방법. 1. URL을 지정한다. 2. HTML을 파싱한다. 3. 원하는 태그를 특정하여 데이터를 추출한다. 4. 가공하여 사용자의 입맛대로 사용한다.
→ ✨BeautifulSoup으로는 동적인 웹 페이지를 크롤링 할 수 없다. Selenium을 사용해보자 !
