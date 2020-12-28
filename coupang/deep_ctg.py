import os
import datetime

import requests
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

coupang_url = 'https://www.coupang.com'

hdr =  {

    'Host': 'www.coupang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'

}

# with open(os.path.join(BASE_DIR, 'ctg_level5_v3.txt'), 'r') as f:
with open(os.path.join(BASE_DIR, 'level4_5url_v3.txt'), 'r') as f:
# with open(os.path.join(BASE_DIR, 'ctg_url_v5.txt'), 'r') as f:
    data = f.readlines()[8897:]

total = len(data)
start = datetime.datetime.now()
with open(os.path.join(BASE_DIR, 'catgs.txt'), 'a') as f:
    for i, row in enumerate(data[:]):
        if '%' in row:
            ctg4, url = row.split("%")
            url = url.strip()
            res = requests.get(url, headers=hdr)
            soup = BeautifulSoup(res.text, 'html.parser')
            uls = soup.select('ul.search-option-items-child')
            for ul in uls:
                lis = ul.select('li')
                if lis:
                    for li in lis:
                        lv5_lis = li.select('li')
                        for li5 in lv5_lis:
                            label = li5.select_one('label')
                        # print(ctg4+'$'+label.text, end='')
                            # print(ctg4+'$'+label.text)
                            f.write(ctg4+'$'+label.text+'\n')
                            now = datetime.datetime.now()
                            print(f'\r{i} / {total} >> runtime: {now - start}', end='')
                        # a = li.select_one('a')
                        # if a:
                        #     print('%'+coupang_url+li['data-link-uri'])
                        # else:
                        #     print()
                    break
        else:
            f.write(row)
            now = datetime.datetime.now()
            print(f'\r{i} / {total} >> runtime: {now - start}', end='')


# for row in data:
#     if '%' in row:
#         print(row, end='')

# for row in data:
#     ctg3, url = row.split("%")
#     url = url.strip()
#     res = requests.get(url, headers=hdr)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     uls = soup.select('ul.search-option-items-child')
#     for ul in uls:
#         lis = ul.select('li')
#         if lis:
#             for li in lis:
#                 label = li.select_one('label')
#                 print(ctg3+'$'+label.text, end='')
#                 a = li.select_one('a')
#                 if a:
#                     print('%'+coupang_url+li['data-link-uri'])
#                 else:
#                     print()
#             break



# for row in data:
#     if row.startswith('http'):
#         url = row.strip()
#         # print(url, end='')
#         res = requests.get(url, headers=hdr)
#         soup = BeautifulSoup(res.text, 'html.parser')
#         uls = soup.select('ul.search-option-items-child')
#         for ul in uls:
#             lis = ul.select('li')
#             if lis:
#                 for li in lis:
#                     label = li.select_one('label')
#                     print(label.text)
#                 break
#     elif not row.startswith('ctg'):
#         ctg_name = row.strip()


# category = soup.select_one('#gnbAnalytics')
# ctg1 = category.select('h3')