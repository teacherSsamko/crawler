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
col = db['gs_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

url = "https://with.gsshop.com/shop/tv/tvShopMain.gs"
driver.get(url)
more = driver.find_element_by_css_selector('#moreBtn')

while True:
    try:
        more.click()
        time.sleep(0.5)
    except:
        break

url_prefix = "http://with.gsshop.com/"

with open("crawler/gs/url_list.txt", 'w') as f:
    prod_list = driver.find_elements_by_css_selector('ul#deal_list > li > a')
    for prod in prod_list:
        page_url = prod.get_attribute('href')
        print(page_url)
        f.write(f'{page_url}\n')
        



# driver.find_element_by_css_selector('div.center.clearfix > ul.clearfix > li > a').click()
# time.sleep(2)
# ctg_list = driver.find_elements_by_css_selector('ul.normal_nav.no_border > li')



driver.quit()


#moreBtn

#deal_list > li:nth-child(1245) > a