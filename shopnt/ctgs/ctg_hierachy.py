import os
import csv
import re

import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# api_url = 'http://www.shoppingntmall.com/category/g-list-cate/20000220'

# res = requests.get(api_url)
# soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())

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

with open(os.path.join(BASE_DIR, 'ctg_codes_2.txt'), 'r') as f:
    txt = f.readlines()[188:]

total = 1178
i = 188
with open(os.path.join(BASE_DIR, 'final_ctg.tsv'), 'w') as f:
    f.write('ctg_code\tn_prod\tctg\n')
    for r in txt:
        ctg_code, ctg_name = r.split("|")
        ctg_name = ctg_name.strip()
        res = requests.post(api_url, data=init_form(category_code=ctg_code, pagesize=1, startcount=startcount)).json()
        # print(ctg_name, end='\t')
        n_prod = 0
        
        try:
            upper = res["CATEGORY_DEPTH_GROUP_3"]
            upper = upper.split(",")[0]
            n_prod = upper.split("|")[-1].split(":")[0]
            upper = re.sub("[{0-9}|]","",upper)
            upper = upper.split("|")[-1]
            ctgs = upper.split(":")
            if ctgs[1] != ctg_name and ctgs[2] != ctg_name:
                f.write(f'{ctg_code}\t{n_prod}\t{upper}:{ctg_name}\n')
        except:
            print(ctg_code, "nothing")
        
        print(f'\r{i}/1178',end='')
        i += 1