import os
import sys
import datetime
import html
import re

import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import config

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

def main():
    conf = config.Config()
    # mongo = MongoClient(f"mongodb://localhost:27017")
    mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
    db = mongo['aircode']
    collection = db['nsmall']

    pCatalogId = '72001'
    pCatgroupIdChild = '1259564'
    # pListId는 카테고리
    parent_dom = requests.get(url='http://www.nsmall.com/NSTvThemeView?storeId=13001&langId=-9&catalogId=72001&catgroupId=1174555')
    # for pPage in range(1,7):
    parent_soup = BeautifulSoup(parent_dom.text, 'html.parser')
    db_dataset = []
    with open('crawler/nsmall/item_list.txt','w') as f:
        for pListId in range(1,5):
        # for pListId in range(1,2):
            ctg_name = parent_soup.select_one(f'#themeTempCat{pListId}').text
            f.write(f'[ {ctg_name} ]\n\n')
            
            for pPage in range(1,7):
                
                # pListId = 1
                # pPage = 1
                data = { 'catalogId' : pCatalogId, 'catgroupIdChild' : pCatgroupIdChild, 'listId' : pListId, 'page' : pPage }
                result = requests.post(url="http://www.nsmall.com/TvThemePrdtList?storeId=13001&langId=-9", data=data)
                # print(result)
                soup = BeautifulSoup(result.text, 'html.parser')
                # print(f'#themeTempCat{pListId}')
                
                print(ctg_name)
                
                item_list = soup.select('#List > ul')
                for ul in item_list:
                    for item in ul.select('li'):
                        # print(f'page {pPage}')
                        prod_name = item.select_one('dt').text
                        print(prod_name)
                        f.write(f"{prod_name}\n")
                        # db_data['prod_name'] = prod_name
                        # print(f'{item.a["href"]}')
                        item_href = 'http://www.nsmall.com'+item.a["href"][1:]
                        f.write(f'{item_href}\n')
                        # db_data['prod_detail_url'] = item_href
                        # item detail page
                        item_detail = requests.get(url=item_href)
                        detail_soup = BeautifulSoup(item_detail.text, 'html.parser')
                        # print(detail_soup)
                        prod_id = item_href.split("=")[4].split("&")[0]
                        f.write(f'id: {prod_id}\n')
                        # db_data['prod_id'] = int(prod_id)
                        price = detail_soup.select_one('strong.save_price > em').text.strip()
                        price = re.sub(r'[,]','',price)
                        #ns_detail > div.area > div.detail_contArea1 > div.det_view.prd_detail > div.dv_left > div.dv_left2 > div.section.zin1 > dl:nth-child(1) > dd > strong
                        try:
                            salesPrice = detail_soup.select_one('strong.price_before').text.strip()
                            salesPrice = re.sub(r'[,원]','',salesPrice)
                        except:
                            salesPrice = price
                        priceDcAmt = int(salesPrice) - int(price)
                        #dvGoodsGuideDataList > p > img
                        # detail_p = detail_soup.select('#dvGoodsGuideDataList')
                        # print(detail_p)
                        # for p in detail_p:
                        #     img = p.select('img')
                        #     while img:
                        #         detail_img_url.append(img.pop()['src'])
                        detail_img_url = []
                        detail_img_url.append(get_detail_img_url(prod_id))


                        print(detail_img_url)
                        f.write(f'price: {price}\n')
                        # db_data['prod_price'] = price
                        try:
                            score = detail_soup.select_one('span.str_count > strong').text
                            score_persons = detail_soup.select_one('span.str_count > span').text.strip("()")
                        except:
                            score, score_persons  = 'None', 'None'
                        f.write(f'score: {score}\n')
                        # db_data['score'] = score
                        f.write(f'score_persons: {score_persons}\n')
                        # db_data['score_persons'] = score_persons
                        # detail_img = detail_soup.select_one('#dvGoodsGuideDataList > p:nth-child(2)').img['src']
                        # print(detail_img)
                        # f.write(f'detail_img: {detail_img}\n')
                        # print(f"http:{item.img['src']}")
                        f.write(f"http:{item.img['src']}\n")
                        today = datetime.date.today()
                        # db_data['img_url'] = item.img['src']
                        f.write('\n')
                        #ns_detail > div.area > div.detail_contArea1 > div.det_view.prd_detail > div.dv_left > div.dv_left2 > div:nth-child(3) > dl > dd > em
                        # freeOfInterestText = detail_soup.select_one('div.section2 > dl > dd > em').text
                        # creditCardDc = 

                        db_data = {
                            'ctg':ctg_name,
                            'prod_id':int(prod_id),
                            'prod_name':prod_name,
                            'prod_price':price,
                            'salesPrice':salesPrice,
                            'priceDcAmt':priceDcAmt,
                            'score':score,
                            'score_persons':score_persons,
                            'img_url':f'http:{item.img["src"]}',
                            'detail_img_url':detail_img_url,
                            'reg_date':str(today)
                        }
                        db_dataset.append(db_data)
            #             break
            #         break
            #     break
            # break
    

    collection.insert_many(db_dataset)


if __name__=='__main__':
    main()