import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")


# driver = webdriver.Chrome(executable_path="/Users/ssamko/Downloads/chromedriver")
url = 'http://www.ssg.com'
driver.get(url)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(f'./ssg'):
    os.makedirs('./ssg')

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# time.sleep(2)
# driver.find_elements_by_css_selector("#skip_gnb > div > ul > li:nth-child(1) > div > div > div.nav_sub_colgroup.notranslate > div:nth-child(1) > ul > li:nth-child(2) > a")[0].click()
driver.find_elements_by_css_selector("a.nav_top_lnk")[0].click()
top_menu_count = len(driver.find_elements_by_css_selector("a.nav_top_lnk"))
print('top menu count =>',top_menu_count) # 11
sub_menu_count = len(driver.find_elements_by_css_selector("a.nav_sub_lnk"))
print('sub menu count =>',sub_menu_count) # 50

with open('crawler/ssg/ctg/ctgId.txt','a') as f:
    for sub in range(5):
        driver.find_elements_by_css_selector("a.nav_top_lnk")[0].click()
        sub_menu = driver.find_elements_by_css_selector("a.nav_sub_lnk")[sub]
        menu_name = sub_menu
        sub_menu.click()
        url = driver.current_url
        ctgId = url.split("=")[-1]
        print(ctgId)
        time.sleep(1)
#skip_gnb > div > ul > li:nth-child(1) > div > div > div.nav_sub_colgroup.notranslate > div:nth-child(1) > ul > li:nth-child(2) > a
# time.sleep(2)
# driver.quit()