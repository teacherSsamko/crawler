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
col = db['lotte_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open(f'crawler/lottemall/daily/{today}_details.txt', 'r') as f:
    urls = f.readlines()
    for url in urls:
        driver.get(url)
        time.sleep(2)
        prod_id = url.split("=")[1].split("&")[0]
        prod_name = driver.find_element_by_css_selector('h3.title_product > span.tit').text.strip()
        try:
            price = driver.find_element_by_css_selector('strong.final > span.num').text
        except:
            continue
        driver.find_element_by_css_selector('a.product_thumb').click()        
        img_url = driver.find_element_by_css_selector('div.thumb_product > a > img').get_attribute('src')

        img_sec = driver.find_elements_by_css_selector('div.img_statem > img')
        detail_img_url = []
        for img in img_sec:
            detail_img_url.append(img.get_attribute('src'))

        video_url = driver.find_element_by_css_selector('video.vjs-tech').get_attribute('src')
        db_data = {
            'prod_id': int(prod_id),
            'prod_name': prod_name,
            'price': price,
            'score': None,
            'score_persons': 0,
            'img_url':img_url,
            'detail_img_url':detail_img_url,
            'video_url':video_url,
            'reg_date':str(today)
        }
        print(prod_id)
        # print(prod_name)
        # print(price)
        # print(img_url)
        print(detail_img_url)
        print()
        col.insert_one(db_data)

driver.quit()