import time

import nsmall_api
import nsmall_image_downloader
import nsmall_review
import detail_img_downloader


def main():
    start_t = time.time()
    nsmall_api.main()
    print('api finish')
    nsmall_image_downloader.main()
    print('image download finish')
    nsmall_review.main()
    print('review finish')
    detail_img_downloader.main()
    print('detail image download finish')
    print(f'nsmall runtime >> {round((time.time() - start_t), 4) }')


if __name__ == "__main__" :
    main()