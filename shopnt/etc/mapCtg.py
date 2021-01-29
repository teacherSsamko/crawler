import os
import csv

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, "multiCtg_ids.txt"), 'r') as f:
    data = f.readlines()
    i = 1
    total = len(data)

with open(os.path.join(BASE_DIR, 'notInProd.txt'), 'w') as f:
    for row in data:
        count, prod_id, ctg = row.split('\t')
        doc = {
            'ctg': ctg.strip()
        }
        if not col.find_one_and_update({'prod_id':prod_id},{'$set':doc}):
            f.write(f'{prod_id}\n')
        print(f'\r{i}/{total}', end='')
        i += 1