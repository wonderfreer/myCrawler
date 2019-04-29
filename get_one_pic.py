import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",'Referer':'http://www.mzitu.com'}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://jandan.net/pic/page-222#comments'  ##开始的URL地址
start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
#print(start_html.text) ##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)
Soup = BeautifulSoup(start_html.text, 'lxml') ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）


img_url = 'http://i.meizitu.net/2018/02/02b01.jpg'
name = img_url[-9:-4] ##取URL 倒数第四至第九位 做图片的名字
img = requests.get(img_url, headers=headers)
f = open(name+'.jpg', 'ab')##写入多媒体文件必须要 b 这个参数！！必须要！！
f.write(img.content) ##多媒体文件要是用conctent哦！
f.close()

# li_list = Soup.find_all('div',class_='row') ##使用BeautifulSoup解析网页过后就可以用找标签呐！（find_all是查找指定网页内的所有标签的意思，find_all返回的是一个列表。）
# for li in li_list: ##这个不解释了。看不懂的小哥儿回去瞅瞅基础教程
# 	pp=li.find('p')
# 	print(pp)
# 	print("\n\n\n")


