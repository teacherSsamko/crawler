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
# driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url = "http://tv.ssg.com"

# driver.get(url)

# prod_list = driver.find_elements_by_css_selector('ul.cunit_thmb_lst > li')

today = datetime.date.today()

# with open(f'crawler/ssg/daily/{today}.txt','w') as f:
    
#     for idx, prod in enumerate(prod_list):
#         item_url = prod.find_element_by_css_selector('div.thmb > a').get_attribute('href')
#         print(f'{idx} - {item_url}')
#         f.write(f'{item_url}\n')

# driver.quit()

data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')

prod_list = soup.select('ul.cunit_thmb_lst > li')

with open(f'crawler/ssg/daily/{today}.txt','w') as f:
    for prod in prod_list:
        item_url = prod.select_one('div.thmb > a')['href']
        item_url = f'http://tv.ssg.com{item_url}'
        print(item_url)
        f.write(f'{item_url}\n')