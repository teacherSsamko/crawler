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
col = db['gong_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = "https://www.gongyoungshop.kr/goods/selectGoodsDetail.do?prdId="

with open('crawler/gong/prod_id_list.txt','r') as f:
    prod_ids = f.readlines()



today = datetime.date.today()

total = len(prod_ids) - 1
start_t = datetime.datetime.now()
for prod_id in prod_ids:
    print(f"{prod_ids.index(prod_id)} / {total}")
    print(f'runtime => {datetime.datetime.now() - start_t}"')
    prod_id = prod_id.replace("\n","")
    url = url_prefix + prod_id
    driver.get(url)
    time.sleep(2)
    try:
        prod_name= driver.find_element_by_css_selector('strong.goodsName').text
        price = driver.find_element_by_css_selector('p.afterPrice > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('img#zoomSnap').get_attribute('src')

    #goodsDetailInfo > center > img
    #goodsDetailInfo > div:nth-child(1) > img
    #goodsDetailInfo > div:nth-child(1) > div:nth-child(1) > img
    #goodsDetailInfo > p:nth-child(1) > img
    #goodsDetailInfo > img
    detail_imgs = driver.find_elements_by_css_selector('#goodsDetailInfo > center > img')
    if not detail_imgs:
        detail_imgs = driver.find_elements_by_css_selector('#goodsDetailInfo > div:nth-child(1) > img')
    if not detail_imgs:
        detail_imgs = driver.find_elements_by_css_selector('#goodsDetailInfo > div:nth-child(1) > div:nth-child(1) > img')
    if not detail_imgs:
        detail_imgs = driver.find_elements_by_css_selector('#goodsDetailInfo > p:nth-child(1) > img')
    if not detail_imgs:
        detail_imgs = driver.find_elements_by_css_selector('#goodsDetailInfo > img')
    detail_img_url = []
    for img in detail_imgs:
        detail_img_url.append(img.get_attribute('src'))

    try:
        score = driver.find_element_by_css_selector('strong.starScore').text[:-1]
        score_persons = driver.find_element_by_css_selector('span.reviewCount > a').text[:-1]
    except:
        score = None
        score_persons = 0
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': score,
        'score_persons': score_persons,
        'img_url':img_url,
        'detail_img_url':detail_img_url,
        'reg_date':str(today)
    }
    print(prod_id)
    print(detail_img_url)
    col.insert_one(db_data)
    # break
    # time.sleep(2)

driver.quit()