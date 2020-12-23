import os
import time
import datetime

from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']

# malls = ['cj','hmall','lotte','w','sk','gong','gs','nsmall','ssg']
malls = ['shopnt']

for mall in malls:
    col = db[f'{mall}_prod']

    today = datetime.date.today()

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    prods = list(col.find())

    with open(os.path.join(BASE_DIR,f"prods_txt/{mall}_prods.txt"),'w') as f:
        for prod in prods:
            f.write(f"{prod['prod_id']}\t")
            f.write(f"{prod['prod_name']}\t")
            if mall == 'nsmall':
                f.write(f"{prod['prod_price']}\t")
            else:
                f.write(f"{prod['price']}\t")
            f.write(f"{prod['score']}\t")
            f.write(f"{prod['score_persons']}\n")
        
