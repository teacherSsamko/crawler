import os
import re

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def rename(fr, to):
    col.update_many({fr:{'$exists': True }, to:{'$exists': False }, 'prod_name':{'$not':re.compile("페이지 없음")}}, {'$rename':{fr:to}})
    # data = list(col.find({fr:{'$exists': True }, to:{'$exists': False }, 'prod_name':{'$not':re.compile("페이지 없음")}}))


def setup():
    data = list(col.find({'goodsName':{'$exists': True }, 'prod_name':{'$exists': False }}))

    for x in data:
        pid = x['prod_id']
        col.find_one_and_update({"prod_id":pid}, {'$set': { 'prod_name': x['goodsName']}})

def extract_fr_txt():
    with open(os.path.join(BASE_DIR, 'multiCtg_ids.txt'), 'r') as f:
        data = f.readlines()

    onWeb = []
    for row in data:
        pid = row.split('\t')[1]
        onWeb.append(pid.strip())

    with open(os.path.join(BASE_DIR, 'onWebPids.txt'), 'w') as f:
        f.write('\n'.join(onWeb))

def compare_web_with_db():
    with open(os.path.join(BASE_DIR, 'onWebPids.txt'), 'r') as f:
        onWeb = f.readlines()

    onWeb = set(onWeb)
    prods = list(col.find({}))
    onDB = []

    for prod in prods:
        pid = prod['prod_id']
        onDB.append(pid.strip())

    with open(os.path.join(BASE_DIR, 'onDBPids.txt'), 'w') as f:
        f.write('\n'.join(onDB))

    onDB = set(onDB)

    onlyWeb = onWeb - onDB
    onlyWeb = list(onlyWeb)

    with open(os.path.join(BASE_DIR, 'onlyWeb.txt'), 'w') as f:
        f.write(''.join(onlyWeb))

def update():
    data = col.find({'benefitPrice':{'$exists':False}, 'salePrice':{'$exists':True}})

    for x in data:
        pid = x['prod_id']
        saleP = x['salePrice']
        col.find_one_and_update({'prod_id':pid}, {'$set':{'benefitPrice':saleP}})

if __name__=='__main__':
    # rename('salesPrice', 'salePrice')
    # setup()
    update()