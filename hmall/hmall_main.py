"""
hmall_prod.py
hmall_get_prod_detail.py
hmall_img_downloader.py
detail_img_downloader.py

"""
import time

import hmall_prod
import hmall_get_prod_detail
import hmall_img_downloader
import detail_img_downloader

def main():
    start_t = time.time()
    hmall_prod.main()
    print(f'get prod finish >> {round((time.time() - start_t), 4)}')
    hmall_get_prod_detail.main()
    print(f'get prod detail finish >> {round((time.time() - start_t), 4)}')
    hmall_img_downloader.main()
    print(f'get image finish >> {round((time.time() - start_t), 4)}')
    detail_img_downloader.main()
    print('get detail image finish')
    print(f'total runtime >> {round((time.time() - start_t), 4)}')

if __name__ == "__main__" :
    main()