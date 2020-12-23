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
review_col = db['w_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = "http://www.w-shopping.co.kr/display/goods/"

today = datetime.date.today()


prods = list(col.find())

total_count = len(prods)
current = 1

for prod in prods:
    prod_id = prod['prod_id']
    url = url_prefix + prod_id
    driver.get(url)
    
    prod_name= prod['prod_name']
    
    score_persons = driver.find_element_by_css_selector('li.d_tab_select:nth-child(3) > a > span').text.strip("()")
    driver.find_element_by_css_selector('ul.item_detail_tab > li.d_tab_select:nth-child(3) > a').click()
    time.sleep(1)
    prod['score_persons'] = score_persons

    review_id = 0

    print(prod_id)
    print(prod_name)
    print(score_persons)
    print()

    while True:
        if int(score_persons) == 0:
            break
        current_page = driver.find_element_by_css_selector('span.current')
        review_list = driver.find_elements_by_css_selector('ul.review_list > li')
        for review in review_list:
            try:
                score = review.find_element_by_css_selector('span.star_rating > em').get_attribute('style').split(":")[-1].split("%")[0]
                review = review.find_element_by_css_selector('div.txt_review_cont').text
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
            current_page.find_elements_by_xpath('following-sibling::a')[0].click()
            time.sleep(1)
        except:
            break

    
    # review_id += 1
    print(f"{current} / {total_count}")
    current += 1
    
    # col.insert_one(db_data)


driver.quit()