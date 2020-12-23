import os
import re

from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

# prod_list = list(col.find())

inTexts = list(os.walk('crawler/shopnt/texts'))[0]
ROOT_DIR = inTexts[0]
texts = inTexts[2]

print('/'.join([ROOT_DIR,texts[0]]))
total = len(texts)
for i, text in enumerate(texts):
    print(f'\r{i}/{total}', end='')
    with open(os.path.join(ROOT_DIR,text), 'r') as f:
        desc = f.readlines()
        desc = '\n'.join(desc)
    prod_id = text.split('.')[0]
    col.find_one_and_update({'prod_id':prod_id}, {'$set':{'desc':desc}})
