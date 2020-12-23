import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

options = Options()
options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url = 'https://www.coupang.com'

with open(os.path.join(BASE_DIR, 'coupang_main.html'), 'r') as html:
    page = html.readlines()

page = ''.join(page)
# res = requests.get(url)
soup = BeautifulSoup(page, 'html.parser')
#gnbAnalytics > ul.menu.shopping-menu-list > li.fashion-sundries > div > div > ul > li:nth-child(1) > div > ul > li:nth-child(1) > a
category = soup.select_one('#gnbAnalytics')
ctg1 = category.select('h3')
print('ctg1')
for c in ctg1:
    print(c.text.strip())

ctg2 = category.select('.fashion-sundries ~ li')
# print('ctg2-',end='')
# print(category.select_one('li.fashion-sundries > a').text.strip())
first_ctg2 = category.select('li.fashion-sundries')
for c in first_ctg2:
    ctg2_name = c.select_one('a').text.strip()
    # print(ctg2_name)
    ctg3 = c.select('div.third-depth-list > ul > li')
    # print('ctg3')
    for c in ctg3:
        a = c.select_one('a')
        ctg3_name = a.text.strip()
        print(ctg2_name+'$'+ctg3_name, end='%')
        print(url + a['href'])

for c in ctg2:
    # print('ctg2-',end='')
    ctg2_name = c.select_one('a').text.strip()
    # print(ctg2_name)
    ctg3 = c.select('div.third-depth-list > ul > li')
    # print('ctg3')
    for c in ctg3:
        a = c.select_one('a')
        ctg3_name = a.text.strip()
        print(ctg2_name+'$'+ctg3_name, end='%')
        print(url + a['href'])

# ctg3 = category.select('div.third-depth-list > ul > li')
# for c in ctg3:
#     print(c.select_one('a').text.strip())