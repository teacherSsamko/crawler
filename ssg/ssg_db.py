import os
import datetime

from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['ssg_prod']

# prod_list = list(col.find())

today = datetime.date.today()

with open(f'crawler/ssg/daily/{today}.txt','r') as f:
    page_list = f.readlines()
    for url in page_list:
        prod_id = url.split("?")[-1].split("=")[1].split("&")[0]
        print(prod_id)
        query = {'prod_id':int(prod_id)}
        new_value = {"$set": { "page_url":url}}
        col.update_one(query, new_value)


# with open(f'crawler/ssg/daily/{today}_reviewed.txt','w') as f:
#     for item in scored_list:
#         page_url = f'http://tv.ssg.com/item/itemView.ssg?itemId={item["prod_id"]}&siteNo=6200&salestrNo=6005'
#         f.write(f'{page_url}\n')