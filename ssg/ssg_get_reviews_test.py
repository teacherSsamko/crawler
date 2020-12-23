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
col = db['ssg']
review_col = db['ssg_reviews']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

def get_last_page(driver):
    driver.find_element_by_css_selector('a.btn_last').click()
    time.sleep(0.1)
    last_page = driver.find_element_by_css_selector('#comment_navi_area > strong').text
    print('last btn clicked: ',last_page)

    last_page = driver.find_element_by_css_selector('#comment_navi_area > strong').text
    if last_page: last_page = int(last_page)
    else: last_page = 0

    return last_page

def  get_review(driver):
    current_page = driver.find_element_by_css_selector('#comment_navi_area > strong').text
    review_list = driver.find_elements_by_css_selector('tbody#cdtl_cmt_tbody > tr')
    review_titles = driver.find_elements_by_css_selector('#cdtl_cmt_tbody > tr > td > div > div.desc')
    # stars = driver.find_elements_by_css_selector('td.star_area > span > em')
    # review_ids = driver.find_elements_by_css_selector('td.fb')
    for idx,item in enumerate(review_list):
        if idx % 2 == 0:
            review_id = item.find_element_by_css_selector('td.number > div').text.strip()
            # print(review_id)
            score = item.find_element_by_css_selector('td.star > div > span > span').get_attribute("style").split(":")[-1].strip()[:-2]
            # print(score)
        else:
            review = item.find_element_by_css_selector('td > div > div.desc')
            print(f'{review_id}({score}) - {review.get_attribute("innerHTML")}')

            db_data = {
                'prod_id': int(prod_id),
                'prod_name':prod_name,
                'prod_review_id':review_id,
                'score':int(score),
                'review':review.text
            }
            review_col.insert_one(db_data)


url = "http://tv.ssg.com/item/itemView.ssg?itemId=1000042058535&siteNo=6200&salestrNo=6005"
prod_id = url.split("?")[-1].split("=")[1].split("&")[0]
driver.get(url)
prod_name = driver.find_element_by_css_selector('h2.cdtl_info_tit').text
print('total pages: ',get_last_page(driver))
current_page = driver.find_element_by_css_selector('#comment_navi_area > strong')
print('current page: ',current_page.text)
get_review(driver)
while int(current_page.text) != 1:
    
    # review_dataset.append(db_data)
    if int(current_page.text) != 1:
        print(current_page.find_elements_by_xpath('preceding-sibling::a')[-1].text)
        current_page.find_elements_by_xpath('preceding-sibling::a')[-1].click()

        time.sleep(0.1)
        current_page = driver.find_element_by_css_selector('#comment_navi_area > strong')
        get_review(driver)
    print('page end')
    # break
# break
time.sleep(1)
    