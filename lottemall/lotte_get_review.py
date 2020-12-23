import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
prod_col = db['lotte_prod']
review_col = db['lotte_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

with open(f'crawler/lottemall/daily/{today}_details.txt', 'r') as f:
    urls = f.readlines()[8:]

idx = 0
for url in urls:
    print('url idx: ',idx)
    driver.get(url)
    time.sleep(0.5)
    driver.find_element_by_css_selector('div.division_product_tab > div.tab_detail > ul > li.tab3 > a').click()
    time.sleep(1)
    try:
        total_score = driver.find_element_by_css_selector('div.grade_total > div.txt > strong').text
    except:
        # 리뷰가 없는 경우.
        continue
    score_persons = driver.find_element_by_css_selector('span#gdasTotalCnt_1').text.strip("()")
    prod_id = url.split("=")[1].split("&")[0]
    prod_name = driver.find_element_by_css_selector('h3.title_product > span.tit').text.strip()
    prod_col.find_one_and_update({'prod_id':prod_id}, {'$set':{'total_score':total_score, 'score_persons':score_persons}})

    review_id = 0
    while True:
        reviews = driver.find_elements_by_css_selector('ul.list_comment > li')
        if reviews[0].get_attribute('class') == 'food_medical':
            break
        # print(reviews)
        for review in reviews:
            
            # score => s00, s05, s10, s15 .... s50 
            score = review.find_element_by_css_selector('div.info_list > div > div').get_attribute('class')
            score = score.split()[-1][1:]
            score = int(score) * 2
            # print(score)
            review = review.find_element_by_css_selector('div.cont > a > span').text
            print(f'{review_id}({score}) - {review}')
            db_data = {
                'prod_id': int(prod_id),
                'prod_name':prod_name,
                'prod_review_id':review_id,
                'score':score,
                'review':review
            }
            review_col.insert_one(db_data)
            review_id += 1
        try:
            current_page = driver.find_element_by_css_selector('div.paging_detail > a.on')
            current_page.find_elements_by_xpath('following-sibling::a')[0].click()
            time.sleep(0.7)
        except:
            break



driver.quit()