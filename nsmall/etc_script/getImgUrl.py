import os
import csv
import re

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['nsmall']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, 'unique_ids.txt'), 'r') as f:
    pids = f.readlines()

with open(os.path.join(BASE_DIR, 'img_urls.txt'), 'w') as f:
    for pid in pids:
        data = col.find_one({'prod_id':int(pid)})

        
        # f.write(f'{data}\n')
        f.write(f'{data["img_url"]}\n')
