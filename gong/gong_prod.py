import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['gong_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open("crawler/gong/ctg_id.txt", 'r') as f:
    ctg_list = f.readlines()

url_prefix = "https://www.gongyoungshop.kr/tvshopping/selectDepth1List.do?dispCatNo="

with open("crawler/gong/prod_id_list.txt", 'w') as f:
    for ctg in ctg_list:
        url = url_prefix + ctg
        print(url)
        driver.get(url)
        time.sleep(2)
        while True:
            items = driver.find_elements_by_css_selector('ul#prdTemp1List > li > div')
            for item in items:
                prod_id = item.get_attribute('id').split("_")[-1]
                print(prod_id)
                f.write(f'{prod_id}\n')
            current_page = driver.find_element_by_css_selector('#gnbSearchPage > div > strong')
            
            try:
                current_page.find_elements_by_xpath('following-sibling::a')[0].click()
                # driver.find_elements_by_css_selector('div#allGoodsPager > button')[-1].click()
                print('next page')
                time.sleep(1)
            except:
                break



# driver.find_element_by_css_selector('div.center.clearfix > ul.clearfix > li > a').click()
# time.sleep(2)
# ctg_list = driver.find_elements_by_css_selector('ul.normal_nav.no_border > li')



driver.quit()
