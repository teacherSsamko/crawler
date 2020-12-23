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
col = db['sk_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = "http://www.skstoa.com/display/goods/"


with open('crawler/sk/prod_id_list.txt','r') as f:
    prod_ids = f.readlines()

total = len(prod_ids) - 1
start_t = datetime.datetime.now()
today = datetime.date.today()

for prod_id in prod_ids:
    print(f'{prod_ids.index(prod_id)}/{total}')
    print(f'runtime >> {datetime.datetime.now() - start_t}')
    prod_id = prod_id.replace("\n","")
    if len(prod_id) == 8:
        url = url_prefix + prod_id
    else:
        url = url_prefix + "deal/" + prod_id
    print(url)
    driver.get(url)
    time.sleep(2)
    try:
        prod_name= driver.find_element_by_css_selector('div.cont_tit > div.upper.clearfix > div.l_part').text
        price = driver.find_element_by_css_selector('p.price > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('img#goodsImg').get_attribute('src')

    #goodsView > div.goods_detail.clearfix > div.l_cont_wrap > div.js_conts.goods_info > div.pic1 > div > p:nth-child(1) > img
    detail_imgs = driver.find_elements_by_css_selector('#goodsView > div.goods_detail.clearfix > div.l_cont_wrap > div.js_conts.goods_info > div.pic1 > div > p')
    detail_img_url = []
    for img in detail_imgs:
        imgs = img.find_elements_by_css_selector('img')
        while imgs:
            detail_img_url.append(imgs.pop().get_attribute('src'))
    print(detail_img_url)


    try:
        video_url = driver.find_element_by_css_selector('video.vod > source').get_attribute('src')
    except:
        video_url = None
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': None,
        'score_persons': 0,
        'img_url':img_url,
        'detail_img_url':detail_img_url,
        'video_url':video_url,
        'reg_date':str(today)
    }
    
    print(prod_name)
    # print()
    col.insert_one(db_data)
    # break
    # time.sleep(2)

driver.quit()