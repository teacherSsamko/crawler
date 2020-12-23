from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']



# get duplicated pids from unique_pids
"""
with open('unique_pids.txt','r') as f:
    pids = f.readlines()
    pids.pop(0)
    n = 0
    for pid in pids:
        # print(pid)
        # print(type(pid))
        pid = pid.strip()
        result = list(col.find({"prod_id":pid}))
        # print(result)
        if len(result) > 1:
            print(pid)
            n += 1
        # break

    print(n)
"""

