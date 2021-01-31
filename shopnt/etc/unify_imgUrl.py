from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

data = list(col.find({'goodsImage':{'$exists': True }}))

ids = []
for x in data:
    image = x['goodsImage'].split(',')[0].strip("[']")
    ids.append((x['prod_id'],image))

print('step1', len(ids))

for x in ids:
    pid = x[0]
    img = x[1]
    col.find_one_and_update({'prod_id':pid}, {'$set': { 'img_url': img}})