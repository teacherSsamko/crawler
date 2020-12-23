import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient


def main():
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

    url = "http://www.hyundaihmall.com/front/tvPlusShopMainR.do?_IC_=tab3"

    driver.get(url)
    WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.moreCateItem')))
    driver.find_element_by_css_selector('#cateItemListIn > div.moreCateItem > a.product_more').click()
    # time.sleep(1)
    prod_items = driver.find_elements_by_css_selector('#cateItemListIn > div.pl_itemlist_wrap > ul > li > a')

    today = datetime.date.today()

    urls = set()

    with open(f'crawler/hmall/daily/{today}.txt','w') as f:
        for prod in prod_items:
            item_url = prod.get_attribute('href')
            # item_url = prod.find_element_by_css_selector('a').get_attribute('href')
            # print(item_url)
            urls.add(item_url)

        for url in urls:
            f.write(f'{url}\n')

    driver.quit()

if __name__=='__main__':
    main()