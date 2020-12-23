import os
import urllib.request
import datetime
import sys

from pymongo import MongoClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import config


def main():
    conf = config.Config()
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
    db = mongo['aircode']
    # review_col = db['nsmall_reviews']
    prod_col = db['nsmall']
    today = datetime.date.today()

    prod_list = list(prod_col.find({'reg_date':str(today)}))

    if not os.path.exists(os.path.join(BASE_DIR, f'images/{today}')):
        os.mkdir(os.path.join(BASE_DIR, f'images/{today}'))

    img_dir = os.path.join(BASE_DIR, 'images')

    total = len(prod_list)
    i = 1

    for prod in prod_list:
        print(f'\r{i}/{total}', end='')
        prod_id = prod['prod_id']
        img_url = prod['img_url']
        urllib.request.urlretrieve(img_url, f"{img_dir}/{today}/{prod_id}.jpg")
        i += 1

if __name__ == "__main__":
    main()