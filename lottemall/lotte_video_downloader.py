import os
import sys
import urllib.request
import datetime

from pymongo import MongoClient
import requests


mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['lotte_prod']

today = datetime.date.today()
prod_list = list(col.find({"reg_date":str(today)}))

video_dir = f"crawler/lottemall/videos/{today}"
if not os.path.exists(video_dir):
    os.mkdir(video_dir)

# with open(f"crawler/ssg/videos/{directory}/url_list.txt", 'r') as f:
#     urls = f.readlines()
#     i = 0
#     for url in urls:
#         urllib.request.urlretrieve(url, f"./images/{directory}/{i}.jpg")
#         i += 1
total_count = len(prod_list)
current_no = 1
for prod in prod_list:
    try:
        video_url = prod['video_url']
        prod_id = prod['prod_id']
        print(prod_id)
    except:
        continue
    print(f'start download {current_no} / {total_count}')
    # urllib.request.urlretrieve(video_url, f"crawler/lottemall/videos/{prod_id}.mp4")

    

    file_name = f"{video_dir}/{prod_id}.mp4"
    with open(file_name, "wb") as f:
        response = requests.get(video_url, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
    print('\ndownload finished')
    current_no += 1