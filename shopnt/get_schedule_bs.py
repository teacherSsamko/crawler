import os
import time
import datetime
import re

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_schedule']

today = datetime.date.today().strftime("%Y/%m/%d")

url = 'http://www.shoppingntmall.com/broadcast/selectBroadCastList?fromDate='
data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')
box = soup.select('div.scdList > ol > li')
onair = False
prev_end_t = ''
next_start_t = ''

box_count = len(box)
if col.count_documents({'on_date':today}) == box_count:
    isCrwaled = True
    print('already crawled today')
else:
    isCrwaled = False


for item in box:
    if isCrwaled:
        break
    # on_time = soup.select_one('div.scdList > ol > li > div.goods_box > dl > dt > span.time > em').text
    on_time = item.select_one('div.goods_box > dl > dt > span.time > em').text

    if onair:
        next_start_t = on_time.split(" ~ ")[-1]
        data = {
            'start_time':prev_end_t,
            'end_time': next_start_t,
            'play_period': f'{prev_end_t} ~ {next_start_t}'
            }
        col.find_one_and_update({'play_period':'on ~ air'}, {'$set': data})
        print('======onair=======')
        print(data)
        onair = False

    if not on_time:
        on_time = f'{prev_end_t} ~ error'
        print(item['class'])
        if item['class'][0] == 'tvOnair':
            onair = True
            on_time = 'on ~ air'
            time_list = on_time.split(" ~ ")

    if onair:
        try:
            prod_id = item.select_one('div.goods_box > dl > dd > div > div.goods_wide > div.goods_img > a')['href']
            prod_id = prod_id.split('/')[-1]
        except:
            print('no image link')
            prod_id = 0
        if prod_id:
        #homeCont1 > div > ol > li.tvOnair > div.goods_box > dl > dd > div > div.goods_wide > div.goods_cont > a > span.tits
            prod_name = item.select_one('div.goods_box > dl > dd > div > div.goods_wide > div.goods_cont > a > span.tits').text
        else:
            prod_name = '공익방송'
        try:
        #homeCont1 > div > ol > li.tvOnair > div.goods_box > dl > dd > div > div.goods_wide > div.goods_cont > div.new_good_price > div.price_row2 > span.price_txt > span.num
            prod_price = item.select_one('div.goods_box > dl > dd > div > div.goods_wide > div.goods_cont > div.new_good_price > div.price_row2 > span.price_txt > span.num').text
        except:
            prod_price = 0
        if prod_price:
            prod_price = int(re.sub(',', '', prod_price))
        else:
            prod_price = 0
    else:
        try:
            prod_id = item.select_one('div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > div.buy_img > a')['href']
            prod_id = prod_id.split('/')[-1]
        except:
            print('no image link')
            prod_id = 0
        #homeCont1 > div > ol > li:nth-child(1) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > a > span
        if prod_id:
            prod_name = item.select_one('div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > a > span.tits').text
        else:
            prod_name = '공익방송'
        #homeCont1 > div > ol > li:nth-child(1) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > div.new_good_price > div > span > p
        #homeCont1 > div > ol > li:nth-child(2) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div > div.buy_list_ul_div > div.new_good_price > div.price_row2 > span.price_txt > span.num
        #homeCont1 > div > ol > li:nth-child(7) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div > div.buy_list_ul_div > div.new_good_price > div.price_row2 > span.price_txt > span.num
        try:
            prod_price = item.select_one('div.goods_box > dl > dd > div > ul:nth-child(1) > li > div > div.buy_list_ul_div > div.new_good_price > div.price_row2 > span.price_txt > span.num').text
        except:
            prod_price = '0'
        if prod_price:
            prod_price = int(re.sub(',', '', prod_price))
        else:
            prod_price = 0

    print(on_time)
    time_list = on_time.split(" ~ ")

    data = {
            'on_date': today,
            'start_time': time_list[0],
            'end_time': time_list[1],
            'play_period': on_time,
            'prod_id': int(prod_id),
            'prod_name': prod_name,
            'prod_price': prod_price,

        }
    print(data)
    col.insert_one(data)
    

# print(prod_id)
# print(len(box))
# print(prod_id)