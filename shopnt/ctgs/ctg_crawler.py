import os
import csv
import datetime
import time

import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

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

start = datetime.datetime.now()

with open(os.path.join(BASE_DIR, 'final_ctg_3.tsv'), newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    reader.__next__()
    reader = list(reader)

total = len(reader)
with open(os.path.join(BASE_DIR, 'ctg_prods_3.tsv'), 'w') as f:
    for i, row in enumerate(reader):
        # print(row)
        
        ctg_code = row[0]
        n_prod = row[1] if int(row[1]) < 100 else 100
        ctg = row[2].strip()
        startcount = 0
        while True:
            res = requests.post(api_url, data=init_form(category_code=ctg_code, pagesize=n_prod, startcount=startcount)).json()
            # print(res["RESULT"])
            
            prods = res["RESULT"]
            if not prods:
                break
            for prod in prods:
                # print(f'{ctg}', end='\t')
                # print(prod["GOODS_CODE"], end='\t')
                # print(prod["GOODS_NAME"])
                f.write(f'{ctg}\t')
                f.write(f'{prod["GOODS_CODE"]}\t{prod["GOODS_NAME"]}\n')
            startcount += int(n_prod)
        print(f'\r{i + 1} / {total} runtime >> {datetime.datetime.now() - start}',end='')

        time.sleep(5)

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
