import os
import datetime
import sys
import urllib.request

from pymongo import MongoClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import config

def main():
    conf = config.Config()

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
    db = mongo['aircode']
    col = db['hmall_prod']


    today = datetime.date.today()
    prod_list = list(col.find({"reg_date":str(today)}))

    if not os.path.exists(os.path.join(BASE_DIR, 'images')):
        os.mkdir(os.path.join(BASE_DIR, 'images'))

    if not os.path.exists(os.path.join(BASE_DIR, f'images/{today}')):
        os.mkdir(os.path.join(BASE_DIR, f'images/{today}'))

    i = 0
    for prod in prod_list:
        img_url = prod['img_url']
        urllib.request.urlretrieve(img_url, os.path.join(BASE_DIR,f"images/{today}/{i}.jpg"))
        i += 1

if __name__=='__main__':
    main()