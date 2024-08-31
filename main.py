import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 페이지 접근
url = "https://m.sivillage.com/dispctg/initDispCtg.siv?disp_ctg_no=2302079174&outlet_yn="
driver.get(url)


# 5초 동안 대기
time.sleep(5)

# Esc 키를 눌러 팝업 닫기 시도
try:
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("Popup closed with ESC key.")
except Exception as e:
    print("Failed to close popup with ESC key:", e)


# product__list thumb-2 하위의 product__item 요소들 찾기
product_items = driver.find_elements(By.CSS_SELECTOR, "ul.product__list.thumb-2 li.product__item")

# 결과 저장을 위한 리스트 초기화
results = []

# 각 product__item에서 데이터 추출
for item in product_items:
    # 이미지 경로 추출
    image_element = item.find_element(By.CSS_SELECTOR, "img.lazyload")
    image_src = image_element.get_attribute("src")
    
    # 브랜드, 이름 데이터 추출
    brand = item.find_element(By.CSS_SELECTOR, "p.product__data-brand").text
    name = item.find_element(By.CSS_SELECTOR, "p.product__data-name").text
    
    # 이름에서 용량 정보 분리
    try:
        # 용량 정보는 마지막 부분에 존재한다고 가정하고, 공백으로 구분하여 마지막 단어를 용량으로 추출
        volume = name.split()[-1]
    except IndexError:
        volume = "N/A"
    
     # 가격과 할인율 데이터 추출
    try:
        price_element = item.find_element(By.CSS_SELECTOR, "p.product__data-price")
        discount_rate = price_element.find_element(By.CSS_SELECTOR, "span.discount-rate").text
        price = price_element.find_elements(By.CSS_SELECTOR, "span")[1].text  # 두 번째 span 태그의 내용이 가격
    except NoSuchElementException:
        discount_rate = "N/A"
        price = "N/A"
    
    # 평점 데이터 추출 (존재하지 않을 경우 처리)
    try:
        rating = item.find_element(By.CSS_SELECTOR, "div.product__data-rating").text
    except NoSuchElementException:
        rating = "N/A"
    
    try:
        delivery_info = item.find_element(By.CSS_SELECTOR, "p.product__data__delivery").text
    except NoSuchElementException:
        delivery_info = "N/A"


    # 필요한 데이터를 CSV 형식으로 저장하기 위한 정리
    results.append({
        "image_src": image_src,
        "brand": brand,
        "name": name,
        "volume": volume,
        "price": price,
        "discount_rate": discount_rate,
        "rating": rating,
        "delivery_info": delivery_info
    })

# CSV 파일로 저장
csv_file = "products.csv"
csv_columns = ["image_src", "brand", "name", "volume", "price", "discount_rate", "rating", "delivery_info"]

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in results:
            writer.writerow(data)
except IOError:
    print("I/O error")

print(f"Data has been written to {csv_file}")

# 브라우저 종료
driver.quit()