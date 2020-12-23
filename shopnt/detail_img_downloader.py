import os
import datetime
import urllib.request

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']


today = datetime.date.today()
prod_list = list(col.find({'reg_date':str(today)}))

if not os.path.exists(os.path.join(BASE_DIR, 'detail')):
    os.mkdir(os.path.join(BASE_DIR, 'detail'))

if not os.path.exists(os.path.join(BASE_DIR, f'detail/{today}')):
    os.mkdir(os.path.join(BASE_DIR, f'detail/{today}'))

total = len(prod_list) - 1
for prod in prod_list:
    print(f'{prod_list.index(prod)}/{total}')
    img_urls = prod['detail_img_url']
    prod_id = prod['prod_id']
    i = 0
    for url in img_urls:
        ext = url.split(".")[-1]
        if ext == 'gif': continue
        try:
            urllib.request.urlretrieve(url, os.path.join(BASE_DIR,f"detail/{today}/{prod_id}_{i}.{ext}"))
        except Exception as e:
            print(e)
            print(url)
            continue
        i += 1