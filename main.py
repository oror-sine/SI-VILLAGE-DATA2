from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 페이지 접근
url = "https://m.sivillage.com/main/initMain.siv?&partnerNm=SVGS0552&utm_source=google&utm_medium=cpc&utm_campaign=siv_all_br_main_SVFK0107&utm_content=2402_main_SVGS0552&utm_term=si%EB%B9%8C%EB%A6%AC%EC%A7%80&gad_source=1&gclid=Cj0KCQjw_sq2BhCUARIsAIVqmQtlhYCkXmIWqtUgYpLXRrUJEwPZUf7d1i_zhUS_dx2AEFN7WhhlQ5caAhdKEALw_wcB"
driver.get(url)