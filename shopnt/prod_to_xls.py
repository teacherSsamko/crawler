import os
import datetime

from openpyxl import Workbook, load_workbook
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

today = datetime.date.today()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

prod_xls = Workbook()

rows = []
title_row = ['prod_id','prod_name','price','score','score_persons','img_url']
rows.append(title_row)

data_rows = list(col.find())


for row in data_rows:
    db_row = []
    db_row.append(row['prod_id'])
    db_row.append(row['prod_name'])
    db_row.append(row['price'])
    db_row.append(row['score'])
    db_row.append(row['score_persons'])
    db_row.append(row['img_url'])
    rows.append(db_row)

for row in rows:
    prod_xls.active.append(row)

prod_xls.save(os.path.join(BASE_DIR, f'prods_{today}.xlsx'))