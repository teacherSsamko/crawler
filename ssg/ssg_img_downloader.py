import os
import datetime
import urllib.request

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['ssg_prod']

prod_list = list(col.find())

today = datetime.date.today()

if not os.path.exists(os.path.join(BASE_DIR, 'images')):
    os.mkdir(os.path.join(BASE_DIR, 'images'))

if not os.path.exists(os.path.join(BASE_DIR, f'images/{today}')):
    os.mkdir(os.path.join(BASE_DIR, f'images/{today}'))

i = 0
for prod in prod_list:
    img_url = prod['img_url']
    urllib.request.urlretrieve(img_url, os.path.join(BASE_DIR,f"images/{today}/{i}.jpg"))
    i += 1