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

class pixiv_novel():
    def __init__(self,url,result_path):
        self.headers = headers
        self.url = url
        self.path = result_path
    
    def cookies(self):
        with open(local_path + "/cookie.txt", 'r') as f:
            cookie = {}
            for row in f.read().split(';'):
                k, v = row.strip().split('=', 1)
                cookie[k] = v
            return cookie
    
    def mkdir(self):
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            print("set new floder: pixiv_novel")

    def run(self):
        #get html
        try:
            req = requests.get(self.url, headers=self.headers)
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
        description = description.replace("<br />","\n")
        content = text_data_dict['content']
        content = content.replace("[newpage]","")
        #write file
        file_path = result_path + title + ".txt"
        with open(file_path, 'a', encoding='utf8') as f:
            f.write('title\n')
            f.writelines(title:)
            f.write('\n\n')
            f.write('description\n')
            f.writelines(description:)
            f.write('\n\n')
            f.write('content\n')
            f.writelines(content:)
            f.write('\n\n')
        print(title + " write success!")

if __name__ == "__main__":
    try:
        id_num = sys.argv[1]
        total_num = len(os.sys.argv)
        i = 1
        while i < total_num:
            id_num = sys.argv[i]
            url = "https://www.pixiv.net/novel/show.php?id=" + id_num
            result_path = local_path + "/pixiv_novel/"
            spider = pixiv_novel(url,result_path)
            spider.mkdir()
            spider.run()
            i = i + 1
    except:
        print("please input novel id after \'python3 pixiv.py\' ")

