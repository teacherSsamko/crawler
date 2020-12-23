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

options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['hmall_prod']

# prod_list = list(col.find())

today = datetime.date.today()
video_src_dir = f'crawler/hmall/videos/src/{today}'

with open(f'crawler/hmall/daily/{today}.txt','r') as f:
    urls = f.readlines()

for url in urls:
    prod_id = url.split("=")[1].split("&")[0]
    if not os.path.exists(f'{video_src_dir}/{prod_id}'):
        os.makedirs(f'{video_src_dir}/{prod_id}')

    # data = requests.get(url)
    driver.get(url)
    # soup = BeautifulSoup(data.text, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        playlist = soup.select_one('video.vjs-tech > source')['src']
    except:
        continue
    print(playlist)
    urllib.request.urlretrieve(playlist, f'{video_src_dir}/{prod_id}/playlist.m3u8')
    url_prefix = playlist.split("/")[1:-1]
    url_prefix = "/".join(url_prefix)
    print(url_prefix)
    with open(f'{video_src_dir}/{prod_id}/playlist.m3u8','r') as f:
        chunk = f.readlines()[-1].replace('\n','')
        print(chunk)
        chunk_url = "https:/" + url_prefix + "/" + chunk
        # print(chunk_url)
    urllib.request.urlretrieve(chunk_url, f'{video_src_dir}/{prod_id}/{chunk}')
    with open(f'{video_src_dir}/{prod_id}/{chunk}','r') as f:
        lines = f.readlines()
        for line in lines:
            if ".ts" in line:
                line = line.replace('\n','')
                print(line)
                ts_url = "https:/" + url_prefix + "/" + line
                urllib.request.urlretrieve(ts_url, f'{video_src_dir}/{prod_id}/{line}')


    # merge files with ffmpeg
    # in_file = ffmpeg.input(f'crawler/hmall/videos/{prod_id}/{chunk}')
    # # stream = ffmpeg.output(f'crawler/hmall/videos/{prod_id}/{prod_id}.mp4')
    # (
    #     ffmpeg
    #     .input(in_file)
        
    #     .output(f'crawler/hmall/videos/{prod_id}/{prod_id}.mp4', c='copy', bsf='a acc_adtstoasc')
    #     .run()
    # )
    # ffmpeg -i {m3u8} -bsf:a acc_adtstoasc -c copy {target_path}

    # result = subprocess.Popen(['ffmpeg', '-i', f'crawler/hmall/videos/{prod_id}/{chunk}', '-bsf:a', 'acc_adtstoasc', '-c', 'copy', f'crawler/hmall/videos/{prod_id}/{prod_id}.mp4'])
    # print(result)
        
    # break
driver.quit()

