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

coupang_url = 'https://www.coupang.com'
headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
           'Content-Type': 'text/html; charset=utf-8'
           }

hdr =  {

    'Host': 'www.coupang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'

}

with open(os.path.join(BASE_DIR, 'ctg_url_v3.txt'), 'r') as f:
    data = f.readlines()

for row in data[4:]:
    ctg3, url = row.split("%")
    url = url.strip()
    res = requests.get(url, headers=hdr)
    soup = BeautifulSoup(res.text, 'html.parser')
    uls = soup.select('ul.search-option-items-child')
    for ul in uls:
        lis = ul.select('li')
        if lis:
            for li in lis:
                label = li.select_one('label')
                print(ctg3+'$'+label.text, end='')
                a = li.select_one('a')
                if a:
                    print('%'+coupang_url+li['data-link-uri'])
                else:
                    print()
            break



# for row in data:
#     if row.startswith('http'):
#         url = row.strip()
#         # print(url, end='')
#         res = requests.get(url, headers=hdr)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         uls = soup.select('ul.search-option-items-child')
#         for ul in uls:
#             lis = ul.select('li')
#             if lis:
#                 for li in lis:
#                     label = li.select_one('label')
#                     print(label.text)
#                 break
#     elif not row.startswith('ctg'):
#         ctg_name = row.strip()


# category = soup.select_one('#gnbAnalytics')
# ctg1 = category.select('h3')