---
weight: 36
title: "Selenium 정복하기"
date: 2024-11-19T12:00:00+09:00
categories: ["Python"]
draft: false
---

# Selenium 라이브러리에 대해 자세히 알아보자 !
대학교 1학년 전공 시간에 BeautifulSoup은 다루어 보았지만, Selenium은 한 번도 사용해본 적이 없기 때문에 이번 장을 통해서 확실히, 정확하게 알아보는 시간이 될 것이다.
## Selenium을 정복해 보자 👊
### Selenium이란 ?
→ 동적 웹 페이지를 크롤링하기 위해 필요한 파이썬 패키지. chromedriver를 제어하거나 원하는 정보를 얻기 위해 사용한다.
크롤링을 하다보면 웹 페이지에서 입력하거나 버튼을 누르는 등 웹 페이지를 조작해야하는 상황이 발생하곤 한다. 그 때 이 패키지를 사용하여 사람이 그러한 행동을 하는 대신 컴퓨터가 할 수 있도록 자동화 해주는 패키지가 Selenium이다.
다양한 언어를 지원하기 때문에 보편적으로 쓰이는 파이썬 패키지이다.
### Selenium의 특징
1. 브라우저 호환성 : 대부분의 브라우저(Chrome, Firefox, Safari 등)와 호환 된다. 또한 각 브라우저마다의 WebDriver를 제공하여 해당 브라우저를 자동으로 제어할 수 있다.
1. 다양한 웹 테스팅 기능 : 웹 페이지의 요소를 찾고, 클릭하고, 텍스트를 입력하고, 페이지를 탐색하는 등 다양한 웹 테스팅 및 자동화 작업을 수행할 수 있는 기능을 제공한다.
1. 강력한 웹 테스트 스크립트 작성 : Selenium은 웹 페이지에서 동적으로 변경되는 요소들을 감지하고 처리할 수 있도록 설계되었다. 이를 통해 복잡한 웹 애플리케이션의 테스트도 쉽게 수행할 수 있다.
1. 클라우드 테스트 통합 : 다양한 클라우드 테스트 플랫폼과 통합되어 있어 대규모 테스트를 자동화하고 분산 시스템에서 실행할 수 있다.
### Selenium 기초
1. 웹 드라이버(Web Driver)
  웹 드라이버는 특정 브라우저와의 통신을 담당한다. chrome, firefox 등의 브라우저를 제어할 수 있는데, 제어하기 위해 각 브라우저에 맞는 웹 드라이버가 필요하다.
```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 크롬드라이버 실행 -> 브라우저 제어 가능
driver = webdriver.Chrome()

# 크롬드라이버에 google url 주소를 넣고 실행
driver.get("https://www.google.co.kr/")
```
1. 요소 찾기
  HTML에는 여러가지 요소가 존재한다. Selenium에는 이 요소를 선택하기 위한 다양한 메서드를 제공한다. 이를 통해 버튼을 클릭하거나, 텍스트를 입력하는 등 작업을 수행할 수 있음.
  요소를 찾는 메서드는 find_element, find_elements가 존재하며, id / name / class_name / tag_name / link_text / partial_link_text / css_selector / xpath가 있다.
```
element = driver.find_element("id", "example-id")
```
→ HTML의 특정 id를 가진 요소를 찾기 위한 예제
1. 요소와 상호작용
  선택한 요소와 상호작용하여 다양한 작업을 수행할 수 있다.
```
# 텍스트 입력
input_box = driver.find_element("name", "username")
# -> 요소(텍스트를 입력할 수 있는 곳)를 찾음
input_box.send_keys("my_username")
# -> 사용자가 입력하기 원하는 값을 전달

# 버튼 클릭
submit_button = driver.find_element("id", "submit")
submit_button.click()
```
1. 페이지 탐색과 대기
  Selenium으로 웹 페이지 크롤링을 하면서 페이지가 로드될 때까지 기다려야 하는 상황이 발생하는 경우가 많다. Selenium에는 이때 사용할 수 있는 두 가지 방식이 있는데, Implicit Wait와 Explicit Wait가 존재한다.
  - Implicit Wait : 지정한 시간 동안 요소를 찾으려 시도하며, 찾을 때까지 기다린다.
  - Explicit Wait : 특정 조건을 만족할 때까지 대기한다.
```
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Explicit Wait 의 예시
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "example-id")))
```
1. 브라우저 종료
  모든 작업이 끝나면 quit() 메서드를 통해 브라우저를 종료한다.
```
driver.quit()
```
## Selenium을 이용하여 웹 크롤링을 해보자
```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Chrome 드라이버 설정
driver = webdriver.Chrome()  # 또는 webdriver.Chrome(executable_path='드라이버 경로')로 지정

try:
    # 구글 페이지 열기
    driver.get("https://www.google.com")
    
    # 검색 창 찾기
    search_box = driver.find_element(By.NAME, "q")
    
    # 검색어 입력
    search_box.send_keys("파이썬 Selenium")
    
    # 검색 실행
    search_box.send_keys(Keys.RETURN)
    
    # 검색 결과 로드 대기
    time.sleep(2)
    
    # 결과 출력 (첫 번째 검색 결과의 텍스트와 링크를 가져옴)
    results = driver.find_elements(By.CSS_SELECTOR, "h3") # 원하는 요소값 찾기
    for idx, result in enumerate(results[:5], 1):  # 상위 5개 결과만 출력
        print(f"{idx}. {result.text}")
        
finally:
    # 브라우저 닫기
    driver.quit()
```
- 실행 결과
<columns>
<column ratio="100">![](/images/50b06f351e21a47a.png)</column>
<column ratio="100">![](/images/9f4032037a9faa89.png)</column>
</columns>
![](/images/d11ae4287d59fd2f.png)
## 이번 장을 통해 얻은 것들
동적으로 만들어진 웹 페이지의 데이터를 크롤링하기 위해 Selenium을 사용한다.
웹 페이지의 데이터를 가져오는 것뿐만 아니라 웹 페이지를 자동으로 조작하고 제어할 수 있다는 점을 알게 되었다.
Selenium을 사용하면 브라우저를 제어하여 웹 페이지의 요소를 찾고, 클릭하고, 텍스트를 입력하는 등의 다양한 작업을 자동화할 수 있다.
또한, 동적으로 변하는 웹 페이지의 내용을 효과적으로 처리할 수 있어 복잡한 웹 애플리케이션의 테스트와 크롤링에 유용하다.
Selenium의 다양한 기능을 활용하면 웹 자동화 작업을 더욱 효율적으로 수행할 수 있을 것이다.
Selenium은 브라우저를 직접 동작시켜 사용자에게 제공되는, 눈에 보이는 데이터는 전부 크롤링이 가능하지만, 컴퓨터 사양에 따라 속도가 다르다.
브라우저를 직접 동작시키므로 자원을 많이 사용한다.
→ 이는 requests 라이브러리를 같이 사용하여 웹 크롤링 시의 속도 측면을 보완할 수 있다.
