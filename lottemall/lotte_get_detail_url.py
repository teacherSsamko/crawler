import datetime

today = datetime.date.today()


with open(f'crawler/lottemall/daily/{today}.txt', 'r') as f:
    lines = f.readlines()
    with open(f'crawler/lottemall/daily/{today}_details.txt', 'w') as n:
        for line in lines:
            prod_id = line.replace('\n','')
            url = f'http://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no={prod_id}&infw_disp_no_sct_cd=40&infw_disp_no=0&llog=O1006_2&allViewYn=N'
            n.write(f'{url}\n')