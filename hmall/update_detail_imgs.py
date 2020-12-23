import os
import time
import datetime

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

mongo = MongoClient("mongodb://localhost:27017")
db = mongo['aircode']
col = db['hmall_prod']

prod_list = list(col.find({}))

url_prefix = 'https://www.shoppingntmall.com/display/goods/'

today = datetime.date.today()

# with open(os.path.join(BASE_DIR,'prod_id_list08.txt'), 'r') as f:
#     prods = f.readlines()
#     total = len(prods)
total = len(prod_list)
current = 1
for prod in prod_list:
    prod_id = prod['prod_id']
    url = url_prefix + prod_id

    print(f'{current}/{total}')
    print(url)
    driver.get(url)
    time.sleep(1)

    #goods_describe > div > div > p > img:nth-child(1)

    # try:
        # prod_name = driver.find_element_by_css_selector('div.new_good_name > span.tits').text
        # print(prod_name)
        # price = driver.find_element_by_css_selector('span.price_txt > span.num').text
        # print(price)
        # img_url = driver.find_element_by_css_selector('ul.swipe-wrap > li > img').get_attribute('src')
        # print(img_url)
    # except:
    #     prod_name = '페이지 없음'
    #     price = '0'
    #     img_url = 'https://img.shoppingntmall.com/goods/480/10011480_ss.jpg'
    try:
        detail_imgs = driver.find_elements_by_css_selector('#goods_describe > div > div > p > img')
        detail_imgs_url = []
        for img in detail_imgs:
            detail_imgs_url.append(img.get_attribute('src'))
    except:
        print(f'prod id: {prod_id} is not available now')
        current += 1
        continue


    
    print('img urls: ',detail_imgs_url)
    col.find_one_and_update({'prod_id':prod_id}, {'$set':{'detail_imgs_url':detail_imgs_url}})

    
    current += 1
    # if current == 3:
    #     break

driver.quit()

###########





for url in urls:
    print(url)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    # with open('crawler/hmall/page_sample.txt','w') as sample:
    #     sample.write(data.text)
    try:
        prod_id = soup.select_one('div.pdtCode > span:nth-child(1)').text.split(":")[-1].strip()
        prod_id = int(prod_id)
        print(prod_id)
        prod_name = soup.select_one('h3.pdtTitle').text.strip()
        print(prod_name)
        price = soup.select_one('p.finalPrice.number.hasDC > strong').text.strip()
        print(price)
    except:
        continue
    try:
        score = soup.select_one('em.scoreMount').text.strip()
        print(score)
        score_persons = soup.select_one('p.scoreNum').text[1:].split()[0]
        print(score_persons)
    except:
        print('No score excists')
        score = None
        score_persons = 0
    img_url = soup.select_one('#prd_ipzoom > img')['src']
    # prd_ipzoom > div._frm_magnifier > div > img
    print(img_url)
    # 3 types of img path
    t1 = soup.select('#guidance > table > tbody > tr > td > p')
    t2 = soup.select('#deal_unit_d1 > dt > p')
    t3 = soup.select('#section_cont_1 > div.prod_detail_view.open > div > table > tbody > tr > td > p')

    if t1:
        print("t1 >>",t1)
        detail_imgs_p = t1
    elif t2:
        print("t2 >>",t2)
        detail_imgs_p = t2
    elif t3:
        print("t3 >>",t3)
        detail_imgs_p = t3
    else:
        print(t1, t2, t3)
        print('weird type error')
        continue
    detail_urls = []
    for p in detail_imgs_p:
        detail_img = p.select_one('img')
        if not detail_img:
            continue
        # print('detail >>', detail_img['src'])
        # detail_img_url = detail_img['src']
        # print(type(detail_img_url))
        detail_urls.append(detail_img['src'])
        # print(detail_urls)
    
    
    db_data = {
        'prod_id': prod_id,
        'prod_name': prod_name,
        'price': price,
        'score': score,
        'score_persons':score_persons,
        'img_url':img_url,
        'detail_img_url':detail_urls,
        'reg_date':str(today)
    }
    col.insert_one(db_data)
        