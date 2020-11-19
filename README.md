# Pixiv novel spider
一个用于爬取pixiv小说的爬虫  
a spider to crawl novels on pixiv.net

## Usage
example link:   
https://www.pixiv.net/novel/show.php?id=11384598  
https://www.pixiv.net/novel/show.php?id=13896538  
https://www.pixiv.net/users/11/novels
```shell
#下载单篇小说/download a novel
python3 pixiv.py n 11384598
#下载多篇小说/download novels
python3 pixiv.py n 11384598 13896538
#下载一个作者的全部非R-18小说/download all novels by one author except r-18 novels
python3 pixiv.py a 11
#下载一个作者的全部小说/download all novels by one author including r-18 novels
python3 pixiv_r18.py #然后根据提示输入作者ID、用户名、密码/then input author's id, your id,your password
```

## Reference
[kougamishinnya](https://github.com/kougamishinnya/Pixiv_new_spider)
