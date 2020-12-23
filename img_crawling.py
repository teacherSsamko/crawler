import os

import requests
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(f'./images'):
    os.makedirs('./images')

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

"""
2020.8.12. 11:58
http://www.ssg.com/robots.txt

User-agent: *
Allow: /
Disallow: /comm/ajaxHistoryList
Disallow: /event/getIssuedCpnQty
Disallow: /search/image
Disallow: /search
"""

# ctgId
# 6000053772 = watch
# 5500000068 = female jumper
# 6000070784 = female onepiece
# 5500000445 = fashion shoes
# 5500000354 = carrier baggage
# 5500000341 = male bag
# 6000053776 = earing
# 6000053777 = ring
ctgId = 6000053777
data = requests.get(f'http://www.ssg.com/disp/category.ssg?ctgId={ctgId}',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
item_list = soup.select('#ty_thmb_view > ul')

if not os.path.exists(f'./images/{ctgId}'):
    os.makedirs(f'./images/{ctgId}')

with open(f"./images/{ctgId}/url_list.txt", 'w') as f:
    for item in item_list:
        for i in range(80):
            # #ty_thmb_view > ul > li:nth-child(2) > div.cunit_prod > div.thmb > a > img
            img = item.select_one(f'li:nth-child({i+1}) > div.cunit_prod > div.thmb > a > img')
            url = f"http://{img['src'][2:]}"
            print(f'{i+1} =>', url)
            i += 1
            f.write(f'{url}\n')
            