import json
import html

import requests
from bs4 import BeautifulSoup

url = 'http://www.nsmall.com/NSItemDetailGoodsGuide?catalogId=97001&langId=-9&storeId=13001'
data = {
    "cmdType":7,"catentryId":"30200279","busChnId":"CTCOM","deviceChnId":"INT"
}
result = requests.get(url, data)
print(result)
detail_val = result.json()['jsonData']['goodsGuideDataList'][0]['specsInputVal']
print(detail_val)
detail_html = html.unescape(detail_val)
print()
detail_soup = BeautifulSoup(detail_html, 'html.parser')
print(detail_soup.select_one('img')['src'])

def get_detail_img_url(prod_id):
    url = 'http://www.nsmall.com/NSItemDetailGoodsGuide?catalogId=97001&langId=-9&storeId=13001'
    # http://www.nsmall.com/NSItemDetailGoodsGuide?catalogId=97001&langId=-9&storeId=13001
    # "cmdType":7,"catentryId":"30214022","busChnId":"CTCOM","deviceChnId":"INT"
    data = {
        "cmdType":7,"catentryId":f"{prod_id}","busChnId":"CTCOM","deviceChnId":"INT"
    }
    result = requests.get(url, data)
    detail_val = result.json()['jsonData']['goodsGuideDataList'][0]['specsInputVal']
    detail_html = html.unescape(detail_val)
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    return detail_soup.select_one('img')['src']

# #ns_detail > div.area > div.detail_contArea1 > div.det_view.prd_detail > div.dv_left > div.dv_left2 > div.section.zin1 > dl:nth-child(1) > dd > strong
# url = 'http://www.nsmall.com/NSItemDetailGoodsGuide?catalogId=97001&langId=-9&storeId=13001'
# # http://www.nsmall.com/NSItemDetailGoodsGuide?catalogId=97001&langId=-9&storeId=13001
# # "cmdType":7,"catentryId":"30214022","busChnId":"CTCOM","deviceChnId":"INT"
# data = {
#     "cmdType":7,"catentryId":f"{prod_id}","busChnId":"CTCOM","deviceChnId":"INT"
# }
# result = requests.get(url, data)
# detail_val = result.json()['jsonData']['goodsGuideDataList'][0]['specsInputVal']
# detail_html = html.unescape(detail_val)
# detail_soup = BeautifulSoup(detail_html, 'html.parser')
# print()