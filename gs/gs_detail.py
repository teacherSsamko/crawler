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
col = db['gs_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open('crawler/gs/url_list.txt','r') as f:
    urls = f.readlines()

total = len(urls) - 1

start_t = datetime.datetime.now()
for url in urls:
    print(f'{urls.index(url)} / {total}')
    driver.get(url)
    # time.sleep(2)
    prod_id = url.split("=")[1].split("&")[0]
    try:
        prod_name= driver.find_element_by_css_selector('p.product-title').text
        price = driver.find_element_by_css_selector('span.price-definition-ins > ins > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('a.btn_img > img').get_attribute('src')
    #prdDetailIfr
    driver.switch_to.frame('prdDetailIfr')
    #html2image > p > img
    details = driver.find_elements_by_css_selector('#html2image > p')
    # print('ppppp >>>', details)
    # print('length of ppppp >>>', len(details))
    detail_img_url = []
    for d in details:
        img = d.find_elements_by_css_selector('img')
        while img:
            detail_img_url.append(img.pop().get_attribute('src'))
    
    driver.switch_to.parent_frame()
    try:
        score = driver.find_element_by_css_selector('span.customer-reviews-score > em').text
        score_persons = driver.find_element_by_css_selector('a.customer-reviews-link-count > em').text.strip("()")
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
    # print(prod_id)
    # print(prod_name)
    # print(detail_img_url)
    # print()
    col.insert_one(db_data)
    # break
    # time.sleep(2)

driver.quit()
print(f'runtime >> {datetime.datetime.now() - start_t}')