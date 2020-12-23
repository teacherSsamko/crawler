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
col = db['sk_prod']

options = Options()
# options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")
driver = webdriver.Chrome(executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()

url = "http://www.skstoa.com/tv_shopping"
# url = "http://www.skstoa.com/"

with open("crawler/sk/ctg_list.txt", 'r') as f:
    ctg_list = f.readlines()

url_prefix = "http://www.skstoa.com/category/goods-list/"

with open("crawler/sk/prod_id_list.txt", 'w') as f:
    for ctg in ctg_list:
        url = url_prefix + ctg
        print(url)
        driver.get(url)
        time.sleep(2)
        while True:
            items = driver.find_elements_by_css_selector('div#goodsBox > article > a.tit_area')
            for item in items:
                page_url = item.get_attribute('onclick').split("(")[-1][:-1]
                print(page_url)
                f.write(f'{page_url}\n')
            current_page = driver.find_element_by_css_selector('div#allGoodsPager > ul > li.on')
            try:
                current_page.find_elements_by_xpath('../following-sibling::button')[-1].click()
                # driver.find_elements_by_css_selector('div#allGoodsPager > button')[-1].click()
                print('next page')
                time.sleep(1)
            except:
                break



# driver.find_element_by_css_selector('div.center.clearfix > ul.clearfix > li > a').click()
# time.sleep(2)
# ctg_list = driver.find_elements_by_css_selector('ul.normal_nav.no_border > li')



driver.quit()
