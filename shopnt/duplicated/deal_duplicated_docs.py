import os
from bson.objectid import ObjectId

from pymongo import MongoClient, DESCENDING, ASCENDING


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# 5f6d555c29be48f7e50ea68e
# print(col.find_one({'_id':ObjectId('5f6d555c29be48f7e50ea68e')}))

# remove docs
def remove_docs():
    with open(os.path.join(BASE_DIR, 'toBeDeletedID.txt'),'r') as f:
                data = f.readlines()

    for x in data:
        col.delete_one({'_id':ObjectId(x.strip()), 'desc':{'$exists':False}})

# check empty desc of objectId
def valid_objectId():
    with open(os.path.join(BASE_DIR, 'toBeDeletedID.txt'),'r') as f:
            data = f.readlines()

    for x in data:
        print(col.find_one({'_id':ObjectId(x.strip()), 'desc':{'$exists':True}}))

def find_objectId():
    with open(os.path.join(BASE_DIR, 'duplicated_pids.txt'),'r') as f:
        data = f.readlines()

    for pid in data[:]:
        # print(pid)
        result = col.find({'prod_id':pid.strip()})
        # result = col.find({'prod_id':pid.strip()}).limit(1).sort('$natural',DESCENDING)
        result = list(result)
        # print(len(result))
        if len(result) > 1:
            print(result[-1]['_id'])
        # for x in result:
        #     # print(x)
        #     print(x["_id"])



# # get duplicated pids from unique_pids

# with open('shopnt/unique_pids.txt','r') as f:
#     pids = f.readlines()

# pids.pop(0)
# n = 0
# with open('shopnt/duplicated_pids.txt','w') as f:
#     for pid in pids:
#         # print(pid)
#         # print(type(pid))
#         pid = pid.strip()
#         result = list(col.find({"prod_id":pid}))
#         # print(result)
#         if len(result) > 1:
#             f.write(f'{pid}\n')
#             n += 1
#         # break

#     print(n)

