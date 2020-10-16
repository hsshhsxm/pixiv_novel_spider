import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import json

headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "",
            "Connection": "keep-alive",
        }
local_path = os.path.abspath(os.path.dirname(__file__))
result_path = local_path + "/pixiv_novel/"

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("set new floder: pixiv_novel")

mkdir(result_path)

class pixiv_novel():
    def __init__(self):
        self.headers = headers
    
    def cookies(self):
        with open(local_path + "/cookie.txt", 'r') as f:
            cookie = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                cookie[k] = v
            return cookie
    
    def run(self):
        url = "https://www.pixiv.net/novel/show.php?id=13817572"
        #get html
        try:
            req = requests.get(url, headers=self.headers)
            req.raise_for_status()
            req.encoding='utf8'
            html = BeautifulSoup(req.text, "html.parser")
        except:
            s = sys.exc_info()
            print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        #get content
        text_data_str = html.find('meta', id="meta-preload-data")['content']
        text_data_dict = json.loads(text_data_str)['novel']
        key = str(list(text_data_dict.keys())[0])
        text_data_dict = text_data_dict[key]
        title = text_data_dict['title']
        description = text_data_dict['description']
        content = text_data_dict['content']
        #write file
        file_path = result_path + title + ".txt"
        with open(file_path, 'a', encoding='utf8') as f:
            f.writelines(title)
            f.write('\n\n')
            f.writelines(description)
            f.write('\n')
            f.writelines(content)
            f.write('\n')
        print(title + "write success")

if __name__ == "__main__":
    spider = pixiv_novel()
    spider.run()
