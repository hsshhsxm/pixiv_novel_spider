# Pixiv novel spider
一个用于爬取pixiv小说的爬虫

## Usage
example link:   
https://www.pixiv.net/novel/show.php?id=11384598  
https://www.pixiv.net/novel/show.php?id=13896538  
https://www.pixiv.net/users/11/novels
```shell
#下载单篇小说
python3 pixiv.py n 11384598
#下载多篇小说
python3 pixiv.py n 11384598 13896538
#下载一个作者的全部非R-18小说
python3 pixiv.py a 11
#下载一个作者的全部小说
python3 pixiv_r18.py #然后根据提示输入作者ID、用户名、密码
```
