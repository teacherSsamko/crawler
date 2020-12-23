import os
import logging

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

logging.basicConfig(
    format='%(message)s',
    filename='crawler/shopnt/unknown.txt', level=logging.INFO)

n_unk = 0
n_known = 0

with open(os.path.join(BASE_DIR, 'unknowndata_201223.txt'), 'r') as f:
    data = f.readlines()
    for row in data:
        prod_id = row.strip()
        result = list(col.find({'prod_id':prod_id}))
        if result:
            # for d in result:
                # print(f"{d['prod_id']}\t{d['prod_name']}")
                # logging.info(f"{d['prod_id']}\t{d['prod_name']}")
            n_known += 1
        else:
            n_unk += 1
            logging.info(f'{prod_id}')

print("known", n_known)
print("unk", n_unk)