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
col = db['shopnt_prod']

today = datetime.date.today()

prod_list = list(col.find({'detail_imgs_url':{'$exists':False}, 'prod_name':{'$not':re.compile("페이지 없음")}}))

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")

url_prefix = 'https://www.shoppingntmall.com/display/goods/'

s