import os
import csv

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

url = 'http://localhost:5000/rec_prod'

# params = '엘리자베스아덴 선글라스 쥬얼에디션'

with open(os.path.join(BASE_DIR, 'unique_val_items.csv'), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.__next__()
    for row in reader:
        params = {'prod':row[0].strip()}
        pid = row[1].strip(' []')
        res = requests.get(url, params=params).json()
        goods = res['goods_code']

        data = []
        for p in goods:
            data.append(p['prod_id'])

        print(f'{pid},{",".join(data)}')


