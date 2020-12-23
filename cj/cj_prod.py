import os
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
col = db['cj_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

url = "http://display.cjmall.com/p/homeTab/main?hmtabMenuId=002409&broadType=plus"

if not os.path.exists(f"crawler/cj/daily/{today}"):
    os.mkdir(f'crawler/cj/daily/{today}')

urls = set()

with open(f"crawler/cj/daily/{today}/url_list.txt", 'w') as f:
    
    driver.get(url)
    time.sleep(1)
    items = driver.find_elements_by_css_selector('ul.list_schedule_prod > li > a')
    for item in items:
        page_url = item.get_attribute('href')
        print(page_url)
        urls.add(page_url)

    for page_url in urls:
        f.write(f'{page_url}\n')



# driver.find_element_by_css_selector('div.center.clearfix > ul.clearfix > li > a').click()
# time.sleep(2)
# ctg_list = driver.find_elements_by_css_selector('ul.normal_nav.no_border > li')



driver.quit()
