import re

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['shopnt_prod']

prod_list = list(col.find())

options = Options()
options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = 'https://www.shoppingntmall.com/display/goods/'


total = len(prod_list)

for i, prod in enumerate(prod_list):
    print(f'\r{i}/{total}', end='')
    prod_id = prod['prod_id'].strip()
    url = url_prefix + prod_id

    # driver.get(url)
    # WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#goodsDetail')))
    data = requests.get(url)
    
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup.prettify())
    #goodsDetail > div:nth-child(1) > div.new_good_wrap > div.new_good_ht_wrap > div > ul > li:nth-child(2) > span.right
    # priceDcAmt = driver.find_element_by_css_selector('#goodsDetail > div:nth-child(1) > div.new_good_wrap > div.new_good_ht_wrap > div > ul > li:nth-child(2) > span.right').text
    try:
        priceDcAmt = soup.select_one('div.new_good_ht_wrap > div > ul > li:nth-child(2) > span.right').text
        priceDcAmt = re.sub(r"[-, ]",'',priceDcAmt)
    except:
        continue
    #goodsDetail > div:nth-child(1) > div.new_good_wrap > div.new_good_ht_wrap > div > ul > li.first > span.right
    # salesPrice = driver.find_element_by_css_selector('#goodsDetail > div:nth-child(1) > div.new_good_wrap > div.new_good_ht_wrap > div > ul > li.first > span.right').text
    salesPrice = soup.select_one('div.new_good_ht_wrap > div > ul > li.first > span.right').text
    salesPrice = re.sub(r"[-, ]",'', salesPrice)
    # desc_url = f'http://www.shoppingntmall.com/display/goods/detail/describe/{prod_id}?_=1608625933427'
    # desc = requests.get(desc_url).json()
    # deliveryInfo = desc['deliveryInfo']
    # describeNote = deliveryInfo['describeNote']
    # deliveryCharge = describeNote.split(":")
    doc = {
        # "deliveryCharge":deliveryCharge,
        "priceDcAmt":priceDcAmt,
        'salesPrice':salesPrice
    }
    col.find_one_and_update({'prod_id':prod_id},{'$set':doc})

# driver.quit()