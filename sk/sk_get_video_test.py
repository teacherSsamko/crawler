import datetime
import time
import os
import urllib.request

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import ffmpeg
import subprocess



"""
pseudo code for downloading video from Hmall

bs4 - detail view
playlist.m3u8 = get video.vjs-tech → source [‘src’]
urlretrive(playlist.m3u8)
chunklist = open(playlist).readlines()[-1]
chunklist download url
urlretrive(chunklist.m3u8)
ts_list = []
chunklist = open(chunklist).readlines()
  it = 6번째줄(idx==5)부터 한 줄씩 건너가며 read() 없으면 break
  ts_list.append(it)
for ts in ts_list:
  urlretrive(chunklist.m3u8)
"""

data = requests.get('http://www.skstoa.com/display/goods/21974542/describe')
print(data.text)

