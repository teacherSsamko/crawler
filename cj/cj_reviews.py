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
col = db['cj_prod']
review_col = db['cj_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open(f'crawler/cj/daily/{today}/url_list.txt','r') as f:
    prods = f.readlines()

total_count = len(prods)
current = 1

for url in prods:
    prod_id = url.split("?")[0].split("/")[-1]
    driver.get(url)
    time.sleep(2)
    
    prod_name= driver.find_element_by_css_selector('h3.prd_tit').text.strip()
    
    # driver.find_element_by_css_selector('ul#ProTab > li:nth-child(2) > a').click()

    review_id = 0

    print(prod_id)
    print(prod_name)
    print()
    # reviews = [review_premiums, review_lines]

    while True:
        review_premiums = driver.find_elements_by_css_selector('div.review_premium > ul.review_lst > li')
        
        for review in review_premiums:
            try:
                score = review.find_element_by_css_selector('div.star_default > span.star_score').get_attribute('style').split(":")[-1].split("%")[0]
                review = review.find_element_by_css_selector('div.review_inner > div.review_cont > a').text
            except:
                continue
            db_data = {
                'prod_id': int(prod_id),
                'prod_name':prod_name,
                'prod_review_id':review_id,
                'score':int(score),
                'review':review
            }
            print(score,review)
            review_col.insert_one(db_data)
            review_id += 1
        try:
            premium_btn = driver.find_element_by_css_selector('div.review_premium > div.u_pagination> div > a.btn_pn_next')
            premium_btn.click()
            time.sleep(0.5)
        except:
            break

    while True:
        review_lines = driver.find_elements_by_css_selector('div.review_line > ul.review_lst > li')
        for review in review_lines:
            try:
                score = review.find_element_by_css_selector('div.star_default > span.star_score').get_attribute('style').split(":")[-1].split("%")[0]
                review = review.find_element_by_css_selector('div.review_cont > div > p').text
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
            line_btn = driver.find_element_by_css_selector('div.review_line > div.u_pagination> div > a.btn_pn_next')
            line_btn.click()
            time.sleep(0.5)
        except:
            break
    
    # review_id += 1
    print(f"{current} / {total_count}")
    current += 1
    
    # col.insert_one(db_data)


driver.quit()