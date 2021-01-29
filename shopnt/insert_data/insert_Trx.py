import os

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'unique_purchase.txt'), 'r') as f:
    pids = f.readlines()

for pid in pids:
    col.find_one_and_update({'prod_id':pid.strip()}, {'$set':{'inTrx':1}})
    print(f'\r{pid}', end='')