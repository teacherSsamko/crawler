import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['cj_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open(f'crawler/cj/daily/{today}/url_list.txt','r') as f:
    urls = f.readlines()

for url in urls[21:]:
    driver.get(url)
    time.sleep(2)
    prod_id = url.split("?")[0].split("/")[-1]
    try:
        prod_name= driver.find_element_by_css_selector('h3.prd_tit').text.strip()
        price = driver.find_element_by_css_selector('span.price_txt > strong').text
    except:
        continue
    img_url = driver.find_element_by_css_selector('div#_topPrdImg > img').get_attribute('src')
    #_itemExplainAreaInfo > div:nth-child(1) > p > img
    # detail_imgs = driver.find_elements_by_css_selector('div#_itemExplainAreaInfo > div > p > img')
    # # detail_imgs = driver.find_elements_by_xpath('//*[@id="_itemExplainAreaInfo"]/div[1]/p/img')
    # print('detail imgs length >> ',len(detail_imgs))
    # detail_img_urls = []
    # for img in detail_imgs:
    #     detail_img_urls.append(img.get_attribute('src'))
    #     print(img.get_attribute('src'))
    # WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_itemExplainAreaInfo')))
    # WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_itemExplainAreaInfo > div:nth-child(1) > p > img')))
    #_itemExplainAreaInfo > div:nth-child(1) > p > img
    #_itemExplainAreaInfo > div:nth-child(3) > p > img
    #_itemExplainAreaInfo > div:nth-child(1) > img:nth-child(2)
    #_itemExplainAreaInfoIframe > iframe
    driver.switch_to.frame(0)
    divs = driver.find_elements_by_css_selector('#_itemExplainAreaInfo > div')
    skip_divs = ['prod_notice','special_top','original_ex']
    detail_img_blocks = []
    for div in divs:
        if div.get_attribute('class') in skip_divs:
            continue
        print(div.get_attribute('class'))
        detail_img_blocks = div.find_elements_by_css_selector('p')
        detail_img_blocks2 = div.find_elements_by_css_selector('img')
    print('ps >>',len(detail_img_blocks))
    detail_img_urls = []
    detail_img_blocks = driver.find_elements_by_css_selector('#_itemExplainAreaInfo > div:nth-child(1) > img')
    for b in detail_img_blocks:
        detail_img_urls.append(b.get_attribute('src'))
    if not detail_img_urls:
        for p in detail_img_blocks2:
            detail_img_urls.append(p.get_attribute('src'))

    # detail_img_urls = driver.find_element_by_css_selector('#_itemExplainAreaInfo > div:nth-child(1) > p > img').get_attribute('src')
    print(detail_img_urls)

    driver.switch_to.parent_frame()

    try:
        score = driver.find_element_by_css_selector('#_MENTION > div.review_summary > div > div > div > span').get_attribute('style').split(":")[-1].split("%")[0]
        print(score)
        score_persons = driver.find_element_by_css_selector('p.score_noti > strong').text[:-1]
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
        'detail_img_url':detail_img_urls,
        'reg_date':str(today)
    }
    print(prod_id)
    print(prod_name)
    print()
    col.insert_one(db_data)
    # break
    # time.sleep(2)

driver.quit()