import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
review_col = db['nsmall_reviews']
prod_col = db['nsmall']

prod_list = list(prod_col.find())[60:70]
review_dataset = []

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

def get_last_page(driver):
    driver.find_element_by_css_selector('a.last').click()
    last_page = driver.find_element_by_css_selector('span#review > strong').text
    if last_page: last_page = int(last_page)
    else: last_page = 0

    return last_page

# if prod['ctg'] != '푸드' and prod['prod_id'] != '29860083':

url = f'http://www.nsmall.com/ProductDisplay?busChnId=INT&langId=-9&storeId=13001&partNumber=29634884&menuUri=NSItemDetailView'
# driver = webdriver.Chrome(executable_path="/Users/ssamko/Downloads/chromedriver")
# url = 'http://www.nsmall.com/ProductDisplay?busChnId=INT&langId=-9&storeId=13001&partNumber=29793300&menuUri=NSItemDetailView'
driver.get(url)

# driver.find_element_by_css_selector('#tbodyReviewList > tr:nth-child(7) > td.tle > div > p > a').click()
last_page = get_last_page(driver)
# //*[@id="review"]/strong
# //*[@id="review"]/preceding-sibling::strong[last()]
print(last_page)
# review = driver.find_element_by_css_selector('#trReviewContents_3 > td > div > div.cont > div.txt > p:nth-child(1)').text
prod_name = driver.find_element_by_css_selector('span.inform.pr10').text
prod_id = driver.find_element_by_css_selector('p.itemNo > span').text.strip()
review_list = driver.find_elements_by_css_selector('tr.reply > td > div > div.cont > div.txt > p:nth-child(1)')
review_titles = driver.find_elements_by_css_selector('td.tle > div > p > a')
stars = driver.find_elements_by_css_selector('td.star_area > span > em')
review_ids = driver.find_elements_by_css_selector('td.fb')
# print(len(review_list))
print(f'[{prod_id}]{prod_name}')
current_page = driver.find_element_by_xpath('//*[@id="review"]/strong')
# print(current_page.find_elements_by_xpath('preceding-sibling::a[@href]')[-1].text)

last_page = int(last_page)
cur_page_no = int(current_page.text)
while cur_page_no != 1:
    current_page = driver.find_element_by_xpath('//*[@id="review"]/strong')
    cur_page_no = int(current_page.text)
    review_list = driver.find_elements_by_css_selector('tr.reply > td > div > div.cont > div.txt > p:nth-child(1)')
    review_titles = driver.find_elements_by_css_selector('td.tle > div > p > a')
    stars = driver.find_elements_by_css_selector('td.star_area > span > em')
    review_ids = driver.find_elements_by_css_selector('td.fb')
    for idx,review in enumerate(review_list):
        review_titles[idx].click()
        review_id = review_ids[idx*2].text
        score = stars[idx].text[:-1]
        if not score:
            score = 0
        score = int(score)
        print(f'{review_id}({score}) - {review.text}')
        db_data = {
            'prod_id':prod_id,
            'prod_name':prod_name,
            'prod_review_id':review_id,
            'score':score,
            'review':review.text
        }
        review_dataset.append(db_data)
    if cur_page_no != 1:
        current_page.find_elements_by_xpath('preceding-sibling::a[@href]')[-1].click()

# driver.quit()

# review_col.insert_many(review_dataset)


