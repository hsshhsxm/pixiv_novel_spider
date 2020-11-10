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
    def __init__(self,judge,id_num,result_path):
        self.headers = headers
        self.path = result_path
        if judge == 'n':
            self.url = "https://www.pixiv.net/novel/show.php?id=" + id_num
        elif judge == 'a':
            self.url = "https://www.pixiv.net/ajax/user/" + id_num + "/profile/all?lang=zh"
            self.author_url = "https://www.pixiv.net/users/" + id_num
    
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

    def get_author_name(self):
        try:
            req = requests.get(self.author_url, headers=headers)
            req.raise_for_status()
            req.encoding='utf8'
            html = BeautifulSoup(req.text, "html.parser")
        except:
            s = sys.exc_info()
            print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return html.title.text[:-8]
    
    def mkdir_for_author(self):
        name = self.get_author_name()
        author_path = self.path + name +'/'
        folder = os.path.exists(author_path)
        if not folder:
            os.makedirs(author_path)
            print("set new floder: pixiv_novel/" + name)
        return author_path

    def get_author_novel_list(self):
        try:
            req = requests.get(self.url, headers=headers)
            req.raise_for_status()
            req_dict = json.loads(req.text)
            novel_list = []
            for key in req_dict['body']['novels'].keys():
                novel_list.append(key)
            return novel_list
        except:
            s = sys.exc_info()
            print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))

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
        file_path = self.path + title + ".txt"
        with open(file_path, 'a', encoding='utf8') as f:
            f.write('title\n')
            f.writelines(title)
            f.write('\n\n')
            f.write('description\n')
            f.writelines(description)
            f.write('\n\n')
            f.write('content\n')
            f.writelines(content)
            f.write('\n\n')
        print(title + " write success!")

if __name__ == "__main__":
    try:
        judge = sys.argv[1]
        result_path = local_path + "/pixiv_novel/"
        if judge == 'n':
            id_num = sys.argv[2]
            total_num = len(os.sys.argv)
            i = 2
            while i < total_num:
                id_num = sys.argv[i]
                url = "https://www.pixiv.net/novel/show.php?id=" + id_num
                spider = pixiv_novel('n', id_num, result_path)
                spider.mkdir()
                spider.run()
                i = i + 1
                time.sleep(1)
        elif judge == 'a':
            userid = sys.argv[2]
            novel_list_spider = pixiv_novel('a', userid, result_path)
            novel_list = novel_list_spider.get_author_novel_list()
            author_path = novel_list_spider.mkdir_for_author()
            total_num = len(novel_list)
            print(str(total_num) + "novels") 
            i = 0
            while i < total_num:
                id_num = novel_list[i]
                spider = spider = pixiv_novel('n', id_num, author_path)
                spider.run()
                i = i + 1
                time.sleep(1)
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        print("please input novel id after \'python3 pixiv.py n \' or user id after \'python3 pixiv.py a \' ")

