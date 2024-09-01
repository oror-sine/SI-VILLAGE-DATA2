import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def scrape_category(category_url, output_file, max_items, top_category_name, middle_category_name, bottom_category_name, sub_category_name):
    # ChromeDriver 설정 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 페이지 접근
    driver.get(category_url)

    # 5초 동안 대기
    time.sleep(3)

    # Esc 키를 눌러 팝업 닫기 시도
    try:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        print("Popup closed with ESC key.")
    except Exception as e:
        print("Failed to close popup with ESC key:", e)

    # 무한 스크롤 구현
    scroll_pause_time = 2  # 스크롤 후 대기 시간 (초)
    last_height = driver.execute_script("return document.body.scrollHeight")
    collected_items = 0

    # 결과 저장을 위한 리스트 초기화
    results = []

    while collected_items < max_items:
        # 페이지 끝까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 스크롤 후 로딩 대기
        time.sleep(scroll_pause_time)

        # 새로 로드된 product__item 요소들 찾기
        product_items = driver.find_elements(By.CSS_SELECTOR, "ul.product__list.thumb-2 li.product__item")

        for item in product_items[collected_items:]:  # 이미 수집된 데이터는 제외하고 새로 추가된 데이터만 처리
            # 이미지 경로 추출
            image_element = item.find_element(By.CSS_SELECTOR, "img.lazyload")
            image_src = image_element.get_attribute("src")
            
            # 브랜드, 이름 데이터 추출
            brand = item.find_element(By.CSS_SELECTOR, "p.product__data-brand").text
            name = item.find_element(By.CSS_SELECTOR, "p.product__data-name").text
                
            # 이름에서 용량 정보 분리 (ml, L, g, kg)
            # 이름에서 용량 정보 분리 (ml, L, g, kg)
            volume = "N/A"
            for word in name.split():
                if any(unit in word.lower() for unit in ["ml", "l", "g", "kg"]):
                    volume = word
                    break
            
            # 가격과 할인율 데이터 추출
            try:
                price_element = item.find_element(By.CSS_SELECTOR, "p.product__data-price")
                discount_rate = price_element.find_element(By.CSS_SELECTOR, "span.discount-rate").text
                price = price_element.find_elements(By.CSS_SELECTOR, "span")[1].text  # 두 번째 span 태그의 내용이 가격
            except NoSuchElementException:
                discount_rate = "N/A"
                price = "N/A"
            
            # 평점과 리뷰 개수 데이터 추출 (존재하지 않을 경우 처리)
            try:
                rating = item.find_element(By.CSS_SELECTOR, "span.point").text
                review_count = item.find_element(By.CSS_SELECTOR, "span.number").text.strip("()")
            except NoSuchElementException:
                rating = "N/A"
                review_count = "N/A"
            
            try:
                delivery_info = item.find_element(By.CSS_SELECTOR, "p.product__data__delivery").text
            except NoSuchElementException:
                delivery_info = "N/A"
                
            # 컬러 이미지와 이름 추출
            color_images = item.find_elements(By.CSS_SELECTOR, "div.product__data__color img")
            color_names = item.find_elements(By.CSS_SELECTOR, "div.product__data__color img")
            
            color_image_srcs = [img.get_attribute("src") for img in color_images]
            color_names = [img.get_attribute("alt") for img in color_names]
            
            # 뱃지 정보 추출
            try:
                bedge = item.find_element(By.CSS_SELECTOR, "div.product__bedge-wrap span").text
            except NoSuchElementException:
                bedge = "N/A"

            # 필요한 데이터를 CSV 형식으로 저장하기 위한 정리
            data_entry = {
                "top_category_name": top_category_name,
                "middle_category_name": middle_category_name,
                "bottom_category_name": bottom_category_name,
                "image_src": image_src,
                "brand": brand,
                "name": name,
                "volume": volume,
                "price": price,
                "discount_rate": discount_rate,
                "rating": rating,
                "review_count": review_count,
                "delivery_info": delivery_info,
                "color_image_src": ",".join(color_image_srcs),  # 다수의 컬러 이미지 URL을 ";"로 구분하여 저장
                "color_name": ",".join(color_names),  # 다수의 컬러 이름을 ";"로 구분하여 저장
                "bedge": bedge
            }
            
            if sub_category_name:
                data_entry["sub_category_name"] = sub_category_name
                
            results.append(data_entry)
            
            collected_items += 1
            if collected_items >= max_items:
                break
        
        # 스크롤 높이 갱신
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # CSV 파일로 저장
    csv_columns = ["top_category_name", "middle_category_name", "bottom_category_name", "sub_category_name", "image_src", "brand", "name", "volume", "price", "discount_rate", "rating", "review_count", "delivery_info", "color_image_src", "color_name", "bedge"]

    if not sub_category_name:
        csv_columns.remove("sub_category_name")  # sub_category_name이 없을 경우 컬럼 제거
        
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in results:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    print(f"Data has been written to {output_file}")

    # 브라우저 종료
    driver.quit()
