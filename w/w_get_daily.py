import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient


options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url = "http://www.w-shopping.co.kr/broadcast/main"

today = datetime.date.today()

driver.get(url)

# video_btns = driver.find_elements_by_css_selector('#onairShow > div.schedule_left > a')
titles = driver.find_elements_by_css_selector('#onairShow > div.schedule_right > ul > li > div.item_info.type1')

# for btn in video_btns:
#     btn.click()
#     time.sleep(1)
#     video_url = driver.find_elements_by_css_selector('video#video').get_attribute('src')
#     driver.find_elements_by_css_selector('#layerPopupVodVideo > section > a').click()

ids = set()

with open(f'crawler/w/daily/{today}.txt','w') as f:
    for title in titles:
        prod_id = title.get_attribute('onclick').split("/")[-1].split("'")[0]
        print(prod_id)
        ids.add(prod_id)

    for prod_id in ids:
        f.write(f'{prod_id}\n')

driver.quit()