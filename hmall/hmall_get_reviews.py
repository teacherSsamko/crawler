import datetime
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

from ...config import Config

conf = Config()

mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
db = mongo['aircode']
col = db['hmall']
review_col = db['hmall_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

# def get_last_page(driver):
#     try:
#         driver.find_element_by_css_selector('a._navs._goLast').click()
#         time.sleep(0.3)
#     except:
#         pass
#     try:
#         last_page = driver.find_element_by_css_selector('a._goPage._active').text
#     except:
#         return False
#     print('last btn clicked: ',last_page)

#     # last_page = driver.find_element_by_css_selector('#comment_navi_area > strong').text
#     if last_page: last_page = int(last_page)
#     else: last_page = 0

#     return last_page

def  get_review(driver, review_id):
    try:
        current_page = driver.find_element_by_css_selector('a._goPage._active').text
    except:
        print("no current page")
        return False
    review_list = driver.find_elements_by_css_selector('#section_cont_2 > div.itemOptEvalInfo > div.photoList > ul > li')
    #section_cont_2 > div.itemOptEvalInfo > div.photoList > ul > li:nth-child(8)
    
    # stars = driver.find_elements_by_css_selector('td.star_area > span > em')
    # review_ids = driver.find_elements_by_css_selector('td.fb')
    for idx,item in enumerate(review_list):
        # print(review_id)
        try:
            score = item.find_element_by_css_selector('div.review-header > span.starScore > span').get_attribute("class").split("-")[-1]
        except:
            score = 8
        # print(score)
        try:
            review = item.find_element_by_css_selector('div.review-text').text.strip('" ')
            print(f'{review_id}({score}) - {review}')
        except:
            print("no review")
            return False

        db_data = {
            'prod_id': int(prod_id),
            'prod_name':prod_name,
            'prod_review_id':review_id,
            'score':int(score),
            'review':review
        }
        review_col.insert_one(db_data)
        review_id += 1
    
    return review_id

with open(f'crawler/hmall/daily/{today}.txt','r') as f:
    urls = f.readlines()
    
    for idx, url in enumerate(urls):
        review_id = 0
        print('idx: ', review_id)
        prod_id = url.split("=")[1].split("&")[0][1:]
        driver.get(url)
        prod_name = driver.find_element_by_css_selector('h3.pdtTitle').text.strip()
        # print('total pages: ',get_last_page(driver))
        try:
            current_page = driver.find_element_by_css_selector('a._goPage._active')
            print('current page: ',current_page.text)
        except:
            continue
        review_id = get_review(driver, review_id)
        # if get_review(driver):
        # while int(current_page.text) != 1:
        while True:
            try:
                current_page.find_elements_by_xpath('following-sibling::a')[0].click()
            except:
                print('page out')
                break
            time.sleep(0.5)
            current_page = driver.find_element_by_css_selector('a._goPage._active')
            review_id = get_review(driver, review_id)
            time.sleep(0.5)
            # if not get_review(driver):
                # print('review out')
                # break
        # else:
        #     continue

            # break
        # break
        # time.sleep(1)
        