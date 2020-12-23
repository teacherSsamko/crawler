import os
import urllib.request
import datetime
import time

from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['w_prod']

today = datetime.date.today()
prod_list = list(col.find({"reg_date":str(today)}))


if not os.path.exists(f'crawler/w/images/{today}'):
    os.mkdir(f'crawler/w/images/{today}')

for prod in prod_list:
    url = prod['img_url']
    urllib.request.urlretrieve(url, f"crawler/w/images/{today}/{prod['prod_id']}.jpg")