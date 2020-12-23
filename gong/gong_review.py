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
review_col = db['gong_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open('crawler/gong/prod_id_list.txt','r') as f:
    prods = f.readlines()[719:]

url_prefix = "https://www.gongyoungshop.kr/goods/selectGoodsDetail.do?prdId="

total = len(prods)
current = 1

for url in prods:
    print(f"{current} / {total}")
    prod_id = url.replace("\n","")
    url = url_prefix + url
    driver.get(url)
    time.sleep(1)
    try:
        prod_name= driver.find_element_by_css_selector('strong.goodsName').text
    except:
        continue
    


    review_id = 0

    print(prod_id)
    print(prod_name)
    print()

    while True:
        
        review_list = driver.find_elements_by_css_selector('#dataListGoodsReview > tr')
        for review in review_list:
            if len(review_list) == 1: break
            if review.get_attribute('class') == 'q':
                score = review.find_element_by_css_selector('td > div.starRatingTitle > div > span').text.split("/")[0][:-1]
                print(score)
            elif review.get_attribute('class') == 'a':
                # review = review.find_element_by_css_selector('td > div > div.revTxtArea > p')
                review = review.find_element_by_css_selector('td > div > div.revTxtArea > p').get_attribute('innerHTML')
                review = review.replace("&nbsp;"," ")
                review = review.replace("<br>","\n")
                #answer27 > td > div > div.revTxtArea > p
                db_data = {
                    'prod_id': int(prod_id),
                    'prod_name':prod_name,
                    'prod_review_id':review_id,
                    'score':int(score),
                    'review':review
                }
                # print(review.text)
                print(review)
                review_col.insert_one(db_data)
                review_id += 1
            
        try:
            current_page = driver.find_element_by_css_selector('#pagingBoxGoodsReview > div > strong')
            current_page.find_elements_by_xpath('following-sibling::a')[0].click()
            # driver.find_elements_by_css_selector('div#allGoodsPager > button')[-1].click()
            print('next page')
            time.sleep(1)
        except:
            break
        

    
    # review_id += 1
    current += 1
    
    # col.insert_one(db_data)


driver.quit()