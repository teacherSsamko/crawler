import os
import urllib.request

dir_list = os.listdir("./images")

for directory in dir_list:
    with open(f"./images/{directory}/url_list.txt", 'r') as f:
        urls = f.readlines()
        i = 0
        for url in urls:
            urllib.request.urlretrieve(url, f"./images/{directory}/{i}.jpg")
            i += 1