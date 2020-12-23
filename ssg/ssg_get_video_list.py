import os
import datetime
import time

import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['ssg_prod']

prod_list = list(col.find())[60:]

today = datetime.date.today()

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")


for item in prod_list:
    try:
        driver.get(item['page_url'])
    except:
        continue
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        video_url = soup.select_one('#videoBox > video')['src']
    except:
        continue
    # print(video_url)
    query = {'prod_id':item['prod_id']}
    new_val = {'$set': {'video_url':video_url}}
    col.update_one(query, new_val)
    time.sleep(4)

driver.quit()