import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['w_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = "http://www.w-shopping.co.kr/display/goods/"

today = datetime.date.today()

with open(f'crawler/w/daily/{today}.txt','r') as f:
    prod_ids = f.readlines()

total_count = len(prod_ids)
current = 1

for prod_id in prod_ids:
    prod_id = prod_id.replace("\n","")
    url = url_prefix + prod_id
    driver.get(url)
    try:
        prod_name= driver.find_element_by_css_selector('h2.title_detail').text
        price = driver.find_element_by_css_selector('span.txt_price > em').text
    except:
        print("!!error on ",prod_id)
        current += 1
        continue
    img_url = driver.find_element_by_css_selector('div.detail_main_img > img').get_attribute('src')
    try:
        driver.find_element_by_css_selector('a.btn_video').click()
        video_url = driver.find_element_by_css_selector('video#video1').get_attribute('src')
    except:
        video_url = None
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': None,
        'score_persons': 0,
        'img_url':img_url,
        'video_url':video_url,
        'reg_date':str(today)
    }
    print(f"{current} / {total_count}")
    current += 1
    print(prod_id)
    print(prod_name)
    print()
    col.insert_one(db_data)


driver.quit()