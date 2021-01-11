import re

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

def rename(fr, to):
    col.update_many({fr:{'$exists': True }, to:{'$exists': False }, 'prod_name':{'$not':re.compile("페이지 없음")}}, {'$rename':{fr:to}})
    # data = list(col.find({fr:{'$exists': True }, to:{'$exists': False }, 'prod_name':{'$not':re.compile("페이지 없음")}}))


def setup():
    data = list(col.find({'goodsName':{'$exists': True }, 'prod_name':{'$exists': False }}))

    for x in data:
        pid = x['prod_id']
        col.find_one_and_update({"prod_id":pid}, {'$set': { 'prod_name': x['goodsName']}})

if __name__=='__main__':
    rename('salesPrice', 'salePrice')
    # setup()