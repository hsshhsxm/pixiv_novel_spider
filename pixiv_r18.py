import json
import os
import requests
import random
import math
from multiprocessing.dummy import Pool
from lxml import etree
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from time import sleep
from pixiv import pixiv_novel

headers_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
    ]
webdriver_path = os.path.abspath(os.path.dirname(__file__)) + "/chromedriver"

def get_cookie(user_id):  # 使用selenium模块进行模拟登陆
    chrome_options = Options()  # 切换无头浏览器
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    option = ChromeOptions()  # 改参数反爬
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    bro = webdriver.Chrome(executable_path= webdriver_path,
                            chrome_options= chrome_options, options=option)
    url = 'https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2Fen%2Fusers%2F' + user_id + '&lang=en&source=pc&view_type=page'
    bro.get(url)
    username = None
    password = None
    if username is None:
        username = str(input("please input your id: "))
    if password is None:
        password = str(input("please input your passpord: "))
    user_tag = bro.find_element_by_xpath(
        '//*[@id="LoginComponent"]/form/div[1]/div[1]/input')  # 定位按钮
    user_tag.send_keys(username)
    time = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    sleep(random.choice(time))
    pass_tag = bro.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
    pass_tag.send_keys(password)
    bro.find_element_by_xpath('//*[@id="LoginComponent"]/form/button').click()
    sleep(3.5)
    cookie_item = bro.get_cookies()  # 获取cookie
    cookie_str = ''
    bro.quit()

    for item_cookie in cookie_item:  # 拼接cookie
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + ";"
        cookie_str += item_str
    return cookie_str

if __name__ == "__main__":
    user_id = input("please input author id: ")
    cookie = get_cookie(user_id)
    headers = {
    'User-Agent': random.choice(headers_list),
    'referer': 'https://www.pixiv.net',
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    'cookie': cookie,
    }

    url = "https://www.pixiv.net/ajax/user/" + user_id + "/profile/all?lang=zh"
    req = requests.get(url, headers=headers)
    req_dict = json.loads(req.text)
    novel_list = []
    for key in req_dict['body']['novels'].keys():
        novel_list.append(key)
    
    #爬虫
    local_path = os.path.abspath(os.path.dirname(__file__))
    result_path = local_path + "/pixiv_novel/"
    novel_list_spider = pixiv_novel('a', user_id, result_path)
    author_path = novel_list_spider.mkdir_for_author()
    author_name = novel_list_spider.get_author_name()
    total_num = len(novel_list)
    print(author_name + " has " + str(total_num) + "novels") 
    i = 0
    while i < total_num:
        id_num = novel_list[i]
        spider = spider = pixiv_novel('n', id_num, author_path)
        spider.run()
        i = i + 1
        sleep(2)