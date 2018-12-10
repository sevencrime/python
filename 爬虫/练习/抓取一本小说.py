#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-20 20:42:48
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

import io
import sys
#改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

import requests 
from bs4 import BeautifulSoup
from lxml import html
from multiprocessing import Pool
import re
import mysql.connector
url = 'https://www.biquge5200.cc/52_52542/'

resp = requests.get(url)
soup = BeautifulSoup(resp.text,'lxml')

name = soup.select('div .bookname > h1')

bookname = str(re.findall('(?<=<h1>).+(?=</h1>)', str(name)))
content = soup.select('div #content > p')
text = str(content).replace('<p>','\r\n').replace('</p>,','')

info = soup.select('#wrapper .box_con #maininfo #info p')
author = info[0].text.replace("\u00a0", " ") 	#作者，需要去掉&nbsp
# print(author)
update = info[2].text.replace("最后更新：","") 	#更新时间
print(update)
intro = soup.select('#wrapper .box_con #maininfo #intro')[0].text.strip()	#小说简介

conn = mysql.connector.connect(user='root', password='123456', database='fiction', use_unicode=True)
cursor = conn.cursor()
cursor.execute("insert into novel_info (title,author,update1,lately,intro)\
	values (%s, %s, %s, %s, %s)", ["222",author,update,"555",intro])

# print(cursor.rowcount)
conn.commit()
cursor.close()

cursor = conn.cursor()
cursor.execute('select * from novel_info')
values = cursor.fetchall()
print(values)

# path = 'D:/Documents/Pictures/小说爬虫'
# with open(path+'/%s.txt' %(bookname[3:-2]), 'a+' , encoding = 'utf-8' ) as f :
# 	f.write(bookname[3:-2])
# 	f.write(text[2:-5])
# 	f.close()


