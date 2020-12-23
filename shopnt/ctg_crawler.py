import os
import csv

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

api_url = 'http://www.shoppingntmall.com/static/search/searchAPI.jsp?'
"""form = {
    'startcount':'0',
    'pagesize':'10',
    'sort':'SORT_POPGOODS/DESC',
    'usecate_yn':'y',
    'category_code':'90000352',
    'order_media_flag':'61'
}
"""
startcount = '0'
pagesize = '10'
category_code = '90000352'
def init_form(category_code, startcount=0, pagesize=10):
    form = {
        'startcount':startcount,
        'pagesize':pagesize,
        'sort':'SORT_POPGOODS/DESC',
        'category_code':category_code,
    }
    return form

with open(os.path.join(BASE_DIR, 'ctg_links.tsv'), newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        # print(row)
        top_ctg = row[0]
        bot_ctg = row[1]
        ctg_code = row[2].split('/')[-1]
        startcount = 0
        while True:
            res = requests.post(api_url, data=init_form(category_code=ctg_code, pagesize=100, startcount=startcount)).json()
            # print(res["RESULT"])
            try:
                prods = res["RESULT"]
            except:
                break
            for prod in prods:
                print(f'{top_ctg}\t{bot_ctg}', end='\t')
                print(prod["GOODS_CODE"], end='\t')
                print(prod["GOODS_NAME"])
        # break

"""
# get link from links page
with open(os.path.join(BASE_DIR, 'snt_mall_category.html'), 'r') as f:
    page = f.read()

soup = BeautifulSoup(page, 'html.parser')

top_ctgs = soup.select('li.top_name')

for ctg in top_ctgs:
    # print(ctg.ul)
    try:
        bot_ctgs = ctg.ul.select('li')
    except:
        continue
    for b_btg in bot_ctgs:
        print(ctg.button.text, end='\t')
        a = b_btg.a
        print(a.text, end='\t')
        print(a['href'])
"""
