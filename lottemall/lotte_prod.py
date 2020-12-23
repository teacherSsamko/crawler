import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient


options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url = "http://www.lotteimall.com/main/viewMain.lotte?dpml_no=16&tlog=a1001_2"

today = datetime.date.today()

driver.get(url)
time.sleep(2)
# thumb_path = '#contents > div > div.rn_tv_conwrap > div.rn_ts_section > div > div > div.rn_tschdule_slide > div.rn_tschedule_item > div > div.rn_tsitem_wrap.rn_tsitem_left.rn_tsitem_highright.rn_tstiem_today > div > div.rn_tsitem_con > div.rn_tsitem_top > div.rn_tsitem_view > a'
thumb_path = 'div.rn_tsitem_con > div.rn_tsitem_top > div.rn_tsitem_view > a'
thumb_list = driver.find_elements_by_css_selector(thumb_path)

ids = set()

with open(f'crawler/lottemall/daily/{today}.txt','w') as f:
    for thumb in thumb_list:
        prod_id = thumb.get_attribute('onclick').split(":")[1].split()[0]
        print(prod_id)
        ids.add(prod_id)

    for prod_id in ids:
        f.write(f'{prod_id}\n')

# driver.execute_script("fn_goodsCheckAdult({goods_no:12640323 , infw_disp_no_sct_cd:'40' , infw_disp_no:0 , conr_no:0 , select_goods_no:0 , cart_sn:'' , target:'', action:'OneAndOne', byr_age_lmt_cd:0 , login_yn:'N' , mbr_age:0 , allViewYn:'N'} , 'llog=O1006_2');")

driver.quit()