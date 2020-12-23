"""
상품코드, 상세설명(상세이미지에서 추출한 텍스트)
"""
import csv
import os
import sys
import re
import datetime

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']
today = datetime.date.today()
start_t = datetime.datetime.now()

texts_dir = '/Users/ssamko/Documents/ssamko/TIS/crawler/shopnt/texts'

# txt_file = os.path.join(BASE_DIR, 'prods_txt/shopnt_prods.txt')
txt_list = os.listdir(texts_dir)


result = open(os.path.join(BASE_DIR, 'shopnt_description.tsv'), 'w')

for txt in txt_list:
    prod_id = txt.split('.')[0]
    with open(os.path.join(texts_dir, txt), 'r') as t:
        desc = t.read()
    line = f'{prod_id}\t{desc}\n'
    result.write(line)

# for test
# txt = '10009231.txt'
# txt_file = os.path.join(texts_dir, txt)
# prod_id = txt.split('.')[0]
# with open(txt_file, 'r') as t:
#     desc = t.read()
# line = f'{prod_id},{desc}\n'
# result.write(line)

finish_t = datetime.datetime.now()
runtime = finish_t - start_t
print('finish')
print('running time >> ',runtime)
result.close()