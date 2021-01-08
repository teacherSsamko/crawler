import os
import csv
import re

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'img_urls.txt'), 'w') as f:
    urls = list(col.find({'prod_name':{'$not':re.compile('페이지 없음')}, 'img_url':{'$exists':True}}, {'_id':0, 'img_url':1}))

    

    for url in urls:
        f.write(f'{url["img_url"]}\n')

with open(os.path.join(BASE_DIR, 'img_urls2.txt'), 'w') as f:
    other_urls = col.find({'prod_name':{'$not':re.compile('페이지 없음')}, 'goodsImage':{'$exists':True}}, {'_id':0, 'goodsImage':1})

    for url in other_urls:
        url = url["goodsImage"].split(",")[0].strip("[']")
        f.write(f'{url}\n')