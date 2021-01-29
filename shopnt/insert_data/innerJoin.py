import os
import csv

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

innerId = []
onlyPurchase = []
with open(os.path.join(BASE_DIR, 'unique_purchase.txt'), 'r') as f:
    ids = f.readlines()
    for pid in ids:
        if col.find_one({"prod_id":pid.strip()}):
            innerId.append(pid)
        else:
            onlyPurchase.append(pid)

with open(os.path.join(BASE_DIR, 'innerJoin.txt'), 'w') as f:
    f.write(''.join(innerId))


with open(os.path.join(BASE_DIR, 'onlyPurchase.txt'), 'w') as f:
    f.write(''.join(onlyPurchase))

