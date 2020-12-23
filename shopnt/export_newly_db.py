import os
import datetime

from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

today = datetime.date.today()
day_fr = datetime.date(2020,12,20)

prod_list = list(col.find({'reg_date':{'$gt':str(day_fr)}},{'_id':False}))

with open(os.path.join(BASE_DIR, f'newly_onDB_{str(day_fr)}_{str(today)}.tsv'),'w') as f:
    columns = 'prod_id\tprod_name\tprice\tscore\tscore_persons\timg_url\treg_date\tdetail_img_url\tbot_ctg\ttop_ctg\tdesc\tdetail_img_url\n'
    f.write(columns)
    for prod in prod_list:
        for i in prod.values():
            f.write(f'{i}\t')
        f.write('\n')


