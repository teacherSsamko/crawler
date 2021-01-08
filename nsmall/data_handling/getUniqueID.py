import os
import csv
import re

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['nsmall']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

uniques = list(map(str, col.distinct('prod_id')))

with open(os.path.join(BASE_DIR, 'unique_ids.txt'), 'w') as f:
    f.write('\n'.join(uniques))