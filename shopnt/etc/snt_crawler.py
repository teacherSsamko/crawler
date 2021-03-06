import os
import re
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
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# prods = list(col.find({'prod_name':'페이지 없음'}))
with open(os.path.join(BASE_DIR, 'onlyWeb.txt'), 'r') as f:
    prods = f.readlines()


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = 'https://www.shoppingntmall.com/display/goods/'

detail_img_api = 'http://www.shoppingntmall.com/display/goods/detail/describe/{prod_id}'

today = datetime.date.today()

total = len(prods)
print('total ',total)

for i, prod in enumerate(prods):
    print(f'\r{i}/{total}', end='')
    prod_id = prod.strip()
    # prod_id = prod['prod_id']
    if col.find_one({'prod_id':prod_id}):
        continue
    else:
        url = url_prefix + prod_id.strip()

        # print(url)
        driver.get(url)
        time.sleep(1)

        try:
            prod_name = driver.find_element_by_css_selector('div.new_good_name > span.tits').text
            # print(prod_name)
        except:
            prod_name = '페이지 없음'
        try:
            benefitPrice = driver.find_element_by_css_selector('span.price_txt > span.num').text
            benefitPrice = re.sub(',','',benefitPrice)
            # print(price)
        except:
            benefitPrice = '0'
        try:
            salePrice = driver.find_element_by_css_selector('span.price_hi').text
            salePrice = re.sub(',','',salePrice)
            # print(salePrice)
        except:
            salePrice = '0'
        try:
            img_url = driver.find_element_by_css_selector('ul.swipe-wrap > li > img').get_attribute('src')
            # print(img_url)
        except:
            img_url = 'https://img.shoppingntmall.com/goods/480/10011480_ss.jpg'
        
        detail_imgs_url = []
        try:
            #goods_describe > div > div:nth-child(3) > img:nth-child(2)
            detail_divs = driver.find_elements_by_css_selector('#goods_describe > div > div')
            detail_imgs = []
            for div in detail_divs:
                detail_imgs += div.find_elements_by_css_selector('img')
            for img in detail_imgs:
                detail_imgs_url.append(img.get_attribute('src'))
        except:
            # print('no detail img')
            pass
        
        try:
        # driver.find_element_by_css_selector('div.star_wrap').click()
        # print('click')
        # score = driver.find_element_by_css_selector('strong#commentTotalScore').text
            score = driver.find_element_by_css_selector('div.star_wrap > div > span').get_attribute('style').split(':')[-1].strip("%;")
            # print(score)
            score_persons = driver.find_element_by_css_selector('div.star_wrap > span.num').text.strip("()")
            # print(score_persons)
        except:
            score = None
            score_persons = 0
        

        db_data = {
            # 'prod_id': prod_id,
            'prod_name': prod_name,
            'salePrice': salePrice,
            'benefitPrice': benefitPrice,
            'priceDcAmt': int(salePrice) - int(benefitPrice),
            'score': score,
            'score_persons': score_persons,
            'img_url':img_url,
            'detail_img_url':detail_imgs_url,
            'reg_date': str(today)
        }

    
        db_data['prod_id'] = prod_id
        col.insert_one(db_data)




driver.quit()
