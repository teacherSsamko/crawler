import os
import time
import datetime

from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['cj_prod']

today = datetime.date.today()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

prods = list(col.find())

with open(os.path.join(BASE_DIR,"prods.txt"),'w') as f:
    for prod in prods:
        f.write(f"{prod['prod_id']}\t")
        f.write(f"{prod['prod_name']}\t")
        f.write(f"{prod['price']}\t")
        f.write(f"{prod['score']}\t")
        f.write(f"{prod['score_persons']}\n")
    
