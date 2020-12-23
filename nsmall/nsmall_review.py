import os
import time
import sys
import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import config

class ReviewCrawler:

    conf = config.Config()
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    mongo = MongoClient(f"mongodb://{conf.MONGO_REMOTE_IP}:27017")
    # mongo = MongoClient("mongodb://localhost:27017")
    db = mongo['aircode']
    review_col = db['nsmall_reviews_test']
    prod_col = db['nsmall']
    today = datetime.date.today()
    

    
    

    if not os.path.exists(os.path.join(BASE_DIR, f'daily')):
        os.mkdir(os.path.join(BASE_DIR, f'daily'))

    daily_index_dir = os.path.join(BASE_DIR, f'daily/{today}')

    if not os.path.exists(daily_index_dir):
        os.mkdir(daily_index_dir)

    index_file = os.path.join(daily_index_dir, f'{today}_index.txt')

    def __init__(self):
        self.review_dataset = []
        self.index_file = ReviewCrawler.index_file
        options = Options()
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")
        print(self.index_file)


        # return [index_file, start_idx, driver]

    def get_last_page(self, driver):
        try:
            driver.find_element_by_css_selector('a.last').click()
            last_page = driver.find_element_by_css_selector('span#review > strong').text
            if last_page: last_page = int(last_page)
            else: last_page = 0
        except:
            last_page = 0

        return last_page



    def get_start_idx(self):
        index_file = self.index_file
        if not os.path.exists(index_file):
            return 0
        with open(index_file, 'r') as f:
            idxs = f.readlines()
            last_idx = idxs[-1]
            print(f'last_idx >> {last_idx}')
            if 'ok' in last_idx:
                return -1
            # 두번째 실패한 건 skip
            else:
                before_idx = idxs[-2].strip('\n')
                print(f'before:{before_idx}/ last:{last_idx}')
                if before_idx == last_idx:
                    last_idx = int(last_idx) + 1

            return int(last_idx)

    

    def crawl_from(self, start_idx):
        prod_list = list(self.prod_col.find({'reg_date':str(ReviewCrawler.today)}))
        print(len(prod_list))
        with open(self.index_file, 'a') as f:
            f.write('\n')
            # prod_list = self.prod_list
            driver = self.driver
            for prod in prod_list[start_idx:]:
                prod_idx = prod_list.index(prod)
                print(f'\rINDEX {prod_idx}', end='')
                f.write(f'{prod_idx}')
                # if prod['ctg'] != '푸드' and prod['prod_id'] != '29860083':
                if prod['ctg'] != '푸드':
                    url = f'http://www.nsmall.com/ProductDisplay?busChnId=INT&langId=-9&storeId=13001&partNumber={prod["prod_id"]}&menuUri=NSItemDetailView'
                # driver = webdriver.Chrome(executable_path="/Users/ssamko/Downloads/chromedriver")
                # url = 'http://www.nsmall.com/ProductDisplay?busChnId=INT&langId=-9&storeId=13001&partNumber=29793300&menuUri=NSItemDetailView'
                    driver.get(url)
                    last_page = self.get_last_page(driver)
                    
                    if last_page:
                        current_page = driver.find_element_by_xpath('//*[@id="review"]/strong')
                        cur_page_no = int(current_page.text)
                    prod_name = driver.find_element_by_css_selector('span.inform.pr10').text
                    prod_id = driver.find_element_by_css_selector('p.itemNo > span').text.strip()
                    # driver.find_element_by_css_selector('#tbodyReviewList > tr:nth-child(7) > td.tle > div > p > a').click()
                    while last_page != 0 and cur_page_no != 1:
                        current_page = driver.find_element_by_xpath('//*[@id="review"]/strong')
                        cur_page_no = int(current_page.text)
                        # review = driver.find_element_by_css_selector('#trReviewContents_3 > td > div > div.cont > div.txt > p:nth-child(1)').text
                        
                        review_list = driver.find_elements_by_css_selector('tr.reply > td > div > div.cont > div.txt > p:nth-child(1)')
                        review_titles = driver.find_elements_by_css_selector('td.tle > div > p > a')
                        stars = driver.find_elements_by_css_selector('td.star_area > span > em')
                        review_ids = driver.find_elements_by_css_selector('td.fb')
                        # print(len(review_list))
                        print(f'[{prod_id}]{prod_name}')
                        for idx,review in enumerate(review_list):
                            review_titles[idx].click()
                            review_id = review_ids[idx*2].text
                            score = stars[idx].text[:-1]
                            if not score:
                                score = 0
                            score = int(score)
                            # print(f'{idx}({score}) - {review.text}')
                            db_data = {
                                'prod_id':prod['prod_id'],
                                'prod_name':prod_name,
                                'prod_review_id':review_id,
                                'score':score,
                                'review':review.text,
                                'reg_date': str(ReviewCrawler.today)
                            }

                            ReviewCrawler.review_col.insert_one(db_data)
                        if cur_page_no != 1:
                            current_page.find_elements_by_xpath('preceding-sibling::a[@href]')[-1].click()
                f.write(f'\tok\n')
            driver.quit()




def main():
    crawler = ReviewCrawler()
    while True:
        try:
            crawler.start_idx = crawler.get_start_idx()
            crawler.crawl_from(crawler.start_idx)
            print('finish?')
            break
        except Exception as e:
            print(e)
            print('timeout error: stop')
            time.sleep(2)
            crawler.driver.quit()
            options = Options()
            options.page_load_strategy = 'eager'
            crawler.driver = webdriver.Chrome(options=options,executable_path="/Users/ssamko/Downloads/chromedriver")
            crawler.driver.set_window_position(-10000,0)
            crawler.start_idx = crawler.get_start_idx()
            if crawler.start_idx == -1:
                print('finish well')
                break
            continue

if __name__ == "__main__":
    main()