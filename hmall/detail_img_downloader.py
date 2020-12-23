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

    dir_name = 'detail_imgs'

    if not os.path.exists(os.path.join(BASE_DIR, dir_name)):
        os.mkdir(os.path.join(BASE_DIR, dir_name))

    if not os.path.exists(os.path.join(BASE_DIR, f'{dir_name}/{today}')):
        os.mkdir(os.path.join(BASE_DIR, f'{dir_name}/{today}'))


    total = len(prod_list) - 1
    for prod in prod_list:
        now = prod_list.index(prod)
        print(f'\r{now}/ {total}',end='')
        prod_id = prod['prod_id']
        img_urls = prod['detail_img_url']
        i = 0
        for url in img_urls:
            try:
                urllib.request.urlretrieve(url, os.path.join(BASE_DIR,f"{dir_name}/{today}/{prod_id}_{i}.jpg"))
                i += 1
            except:
                print('bad image')
                i += 1
                continue
        
if __name__=='__main__':
    main()