import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['ssg_prod']

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

today = datetime.date.today()


with open(f'crawler/ssg/daily/{today}.txt','r') as f:
    lines = f.readlines()
    for idx, url in enumerate(lines):
        print(url)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # prod_id = soup.select_one('p.cdtl_prd_num').text
        # prod_id = int(prod_id.split(":")[-1].strip())
        prod_id = url.split("?")[-1].split("=")[1].split("&")[0]
        prod_id = int(prod_id)
        print(prod_id)
        # prod_name = soup.select_one('h2.cdtl_info_tit').text
        prod_name = soup.select_one('h2.cdtl_info_tit').text
        # print(prod_name)
        try:
            ctg = soup.select('a.lo_menu.lo_arr.clickable')[-1].text
        except:
            ctg = None
        finally:
            # print(ctg)
            pass
        
        price = soup.select_one('em.ssg_price').text
        # print(price)
        img_url = soup.select_one('img#mainImg')['src']
        img_url = 'http:'+img_url
        # print(img_url)
        
        driver.switch_to.frame('_ifr_html')
        #descContents > img:nth-child(3)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        detail_imgs = soup2.select('#descContents > img')
        detail_imgs.extend(soup2.select('#descContents > p > img'))
        detail_img_url = []
        for img in detail_imgs:
            detail_img_url.append(img['src'])
        print(detail_img_url)
        driver.switch_to.parent_frame()


        try:
            score = soup.select_one('span.cdtl_txt').text
            score_persons = soup.select_one('span.count > em').text
        except:
            score = None
            score_persons = 0
        finally:
            # print(f'{score}({score_persons})')
            pass
        db_data = {
            'prod_id': prod_id,
            'prod_name': prod_name,
            'price': price,
            'score': score,
            'score_persons':score_persons,
            'img_url':img_url,
            'detail_img_url':detail_img_url,
            'reg_date':str(today)
        }
        col.insert_one(db_data)
        if idx % 5 == 0:
            time.sleep(7)


driver.quit()




