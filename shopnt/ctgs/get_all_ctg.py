import os
import csv
import re

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

with open(os.path.join(BASE_DIR, 'ctg_links.tsv'), newline='') as tsvfile:
    reader = list(csv.reader(tsvfile, delimiter='\t'))

total = len(reader)
with open(os.path.join(BASE_DIR, 'ctg_prods.txt'), 'w') as f:
    for i, row in enumerate(reader):
        # print(row)
        top_ctg = row[0]
        bot_ctg = row[1]
        ctg_code = row[2].split('/')[-1]
        startcount = 0
        # f.write(f'{top_ctg}/{bot_ctg}\n')
        print(f'\r{i}/{total}',end='')
        while True:
            res = requests.post(api_url, data=init_form(category_code=ctg_code, pagesize=1, startcount=startcount)).json()
            # print(res)
            # print(res["CATEGORY_GROUP"])
            # print(res['TOTALCOUNT'])
            # print(res["RESULT"])
            # print(res["CATEGORY_DEPTH_GROUP_3"])
            txt = res["CATEGORY_DEPTH_GROUP_4"]
            f.write(re.sub('[:,]','\n',txt))
            break
            try:
                prods = res["RESULT"]
            except:
                break
            for prod in prods:
                print(f'{top_ctg}\t{bot_ctg}', end='\t')
                print(prod["GOODS_CODE"], end='\t')
                print(prod["GOODS_NAME"])
            
            startcount += 1
        # break
