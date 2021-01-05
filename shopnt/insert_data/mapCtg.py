import os
import csv

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, "ctg_prods_2.tsv"), newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    i = 1
    total = 297765
    for row in reader:
        exist = col.find_one({'prod_id':row[4], 'ctg1':{'$exists':True}})
        if exist:
            ctg1 = exist['ctg1']
            ctg2 = exist['ctg2']
            ctg3 = exist['ctg3']
            ctg4 = exist['ctg4']
            doc = {
                'ctg1':ctg1.append(row[0]),
                'ctg2':ctg2.append(row[1]),
                'ctg3':ctg3.append(row[2]),
                'ctg4':ctg4.append(row[3])
            }
            # doc = {
            #     'ctg1':exist['ctg1'].append(row[0]),
            #     'ctg2':exist['ctg2'].append(row[1]),
            #     'ctg3':exist['ctg3'].append(row[2]),
            #     'ctg4':exist['ctg4'].append(row[3])
            # }
            print(doc)
        else:
            doc = {
                'ctg1':[row[0]],
                'ctg2':[row[1]],
                'ctg3':[row[2]],
                'ctg4':[row[3]]
            }
        col.find_one_and_update({'prod_id':row[4]},{'$set':doc})
        print(f'\r{i}/297765', end='')
        i += 1