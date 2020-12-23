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
review_col = db['gs_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open('crawler/gs/url_list.txt','r') as f:
    prods = f.readlines()

total_count = len(prods)
current = 1

for url in prods:
    prod_id = url.split("=")[1].split("&")[0]
    driver.get(url)
    
    prod_name= driver.find_element_by_css_selector('p.product-title').text
    
    driver.find_element_by_css_selector('ul#ProTab > li:nth-child(2) > a').click()
    time.sleep(1)

    review_id = 0

    print(prod_id)
    print(prod_name)
    print()

    while True:
        
        review_list = driver.find_elements_by_css_selector('section#reveiw-list > article')
        for review in review_list:
            try:
                score = review.find_element_by_css_selector('header > div > span.star-rate > em').get_attribute('style').split(":")[-1].split("%")[0]
                review = review.find_element_by_css_selector('main > p.review-desc').text
            except:
                continue
            db_data = {
                'prod_id': int(prod_id),
                'prod_name':prod_name,
                'prod_review_id':review_id,
                'score':int(score),
                'review':review
            }
            print(review)
            review_col.insert_one(db_data)
            review_id += 1
        try:
            btn = driver.find_element_by_css_selector('button.gui-btn.small.outline.go-next')
            if 'disabled' in btn.get_attribute('class'):
                break
            btn.click()
            time.sleep(1)
        except:
            break

    
    # review_id += 1
    print(f"{current} / {total_count}")
    current += 1
    
    # col.insert_one(db_data)


driver.quit()