import os
import time
import datetime
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_schedule']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url = 'http://www.shoppingntmall.com/index?snt=homeCont1#1'

today = datetime.date.today().strftime("%Y/%m/%d")

driver.get(url)
time.sleep(1)
#homeCont1 > div > ol
schedule = driver.find_elements_by_css_selector('#homeCont1 > div > ol > li')
# print(schedule)
onair = False
prev_end_t = ''
next_start_t = ''


for item in schedule:
    box = item.find_element_by_css_selector('.goods_box')
    #homeCont1 > div > ol > li:nth-child(25) > div.goods_box > dl > dt > span.time > em
    on_time = box.find_element_by_css_selector('dl > dt > span.time > em').text
    # handling 'on air'
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
    #     onair = True
    #     on_time = 'on ~ air'


    time_list = on_time.split(" ~ ")
    #homeCont1 > div > ol > li:nth-child(1) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > div.buy_img > a
    # on air
    #homeCont1 > div > ol > li.tvOnair > div.goods_box > dl > dd > div > div.goods_wide > div.goods_img > a

    if item.get_attribute('class') == 'tvOnair':
        onair = True
        on_time = 'on ~ air'
        time_list = on_time.split(" ~ ")
        try:
            prod_id = box.find_element_by_css_selector('dl > dd > div > div.goods_wide > div.goods_img > a').get_attribute('href')
            prod_id = prod_id.split('/')[-1]
        except:
            print('no image link')
            prod_id = 0
        if prod_id:
        #homeCont1 > div > ol > li.tvOnair > div.goods_box > dl > dd > div > div.goods_wide > div.goods_cont > a > span.tits
            prod_name = box.find_element_by_css_selector('dl > dd > div > div.goods_wide > div.goods_cont > a > span.tits').text
        else:
            prod_name = '공익방송'
        try:
        #homeCont1 > div > ol > li.tvOnair > div.goods_box > dl > dd > div > div.goods_wide > div.goods_cont > div.new_good_price > div.price_row2 > span.price_txt > span.num
            prod_price = box.find_element_by_css_selector('dl > dd > div > div.goods_wide > div.goods_cont > div.new_good_price > div.price_row2 > span.price_txt > span.num').text
        except:
            prod_price = 0
        if prod_price:
            prod_price = int(re.sub(',', '', prod_price))
        else:
            prod_price = 0
    else:
        try:
            prod_id = box.find_element_by_css_selector('dl > dd > div > ul:nth-child(1) > li > div.goods > div > div.buy_img > a').get_attribute('href')
            prod_id = prod_id.split('/')[-1]
        except:
            print('no image link')
            prod_id = 0
        #homeCont1 > div > ol > li:nth-child(1) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > a > span
        if prod_id:
            prod_name = box.find_element_by_css_selector('dl > dd > div > ul:nth-child(1) > li > div.goods > div > a > span.tits').text
        else:
            prod_name = '공익방송'
        #homeCont1 > div > ol > li:nth-child(1) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div.goods > div > div.new_good_price > div > span > p
        #homeCont1 > div > ol > li:nth-child(2) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div > div.buy_list_ul_div > div.new_good_price > div.price_row2 > span.price_txt > span.num
        #homeCont1 > div > ol > li:nth-child(7) > div.goods_box > dl > dd > div > ul:nth-child(1) > li > div > div.buy_list_ul_div > div.new_good_price > div.price_row2 > span.price_txt > span.num
        try:
            prod_price = box.find_element_by_css_selector('dl > dd > div > ul:nth-child(1) > li > div > div.buy_list_ul_div > div.new_good_price > div.price_row2 > span.price_txt > span.num').text
        except:
            prod_price = '0'
        if prod_price:
            prod_price = int(re.sub(',', '', prod_price))
        else:
            prod_price = 0
    # print(on_time)
    # print(today)
    # print(prod_id)
    # print(prod_name)
    # print(prod_price)


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
    if not onair:
        prev_end_t = time_list[1]
    # break

driver.quit()