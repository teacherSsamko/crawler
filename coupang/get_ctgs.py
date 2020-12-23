import os

import requests
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

url = 'https://www.coupang.com'

with open(os.path.join(BASE_DIR, 'coupang_main.html'), 'r') as html:
    page = html.readlines()

page = ''.join(page)
# res = requests.get(url)
soup = BeautifulSoup(page, 'html.parser')

category = soup.select_one('#gnbAnalytics')
# ctg1 = category.select('h3')
# print('ctg1')
# for c in ctg1:
#     print(c.text.strip())

# ctg1 = category.select()

ctg1 = category.select('ul.shopping-menu-list')
# print('ctg2-',end='')
# print(category.select_one('li.fashion-sundries > a').text.strip())
first_ctg2 = category.select('li.fashion-sundries')
for c1 in ctg1:
    ctg1_name = c1.select_one('li > a').text.strip()
    ctg2 = c1.select('li.second-depth-list')
    for c2 in ctg2:
        # print(ctg2_name)
        ctg2_name = c2.select_one('a').text.strip()
        ctg3 = c2.select('div.third-depth-list > ul > li')
        # print('ctg3')
        for c in ctg3:
            a = c.select_one('a')
            ctg3_name = a.text.strip()
            print(ctg1_name+'$'+ctg2_name+'$'+ctg3_name, end='%')
            print(url + a['href'])

