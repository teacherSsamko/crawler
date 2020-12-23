"""
전체 쇼핑몰 데이터 모아서 하나의 csv파일로 정리
쇼핑몰, 상품코드, 상품명, 상품가격, 평점, 평점수, image_url

쇼핑몰 = (cj, gong, gs, hmall, lotte, ns, shopnt, sk, ssg, w)
평점, 평점 수는 없으면 0
"""
import csv
import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
txt_files_dir = os.path.join(BASE_DIR, 'prods_txt')
txt_list = os.listdir(txt_files_dir)
# print(txt_list)
# print(type(txt_list[0]))

result = open(os.path.join(BASE_DIR, 'all_prods.csv'), 'w')

shop_list = {
    'cj':'cj',
    'gong':'gong',
    'gs':'gs',
    'hmall':'hmall',
    'lotte':'lotte',
    'nsmall':'ns',
    'shopnt':'shopnt',
    'sk':'sk',
    'ssg':'ssg',
    'w':'w'
}


for txt in txt_list:
    shop = txt.split('_')[0]
    if shop == 'shopnt' or shop == 'sk':
        continue
    # print(shop)
    shop_name = shop_list[shop]
    txt_path = os.path.join(txt_files_dir, txt)
    # print(txt_path)
    with open(txt_path, 'r') as f:
        doc = f.readlines()
        for line in doc:
            # 가격에서 ',' 제거
            tmp = re.sub(',','',line) 
            # change tsv to csv
            tmp = re.sub('\t',',', tmp)
            row = f'{shop_name},{tmp}'
            # print(row)
            result.write(row)
            # break

result.close()