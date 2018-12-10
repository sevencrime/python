#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 19:46:45
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

import requests 
from bs4 import BeautifulSoup	#BeautifulSoup：HTML的解析库

import io
import sys
#改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

url = 'http://news.qq.com/'
resp = requests.get(url).text
#对获取到的HTML进行解析
soup = BeautifulSoup(resp,'lxml')

# soup.select():同个CSS选择器来筛选，返回一个list
news_titles = soup.select('div.text > em.f14 > a.linkto')
# print(news_titles)

for n in news_titles:
	#遍历列表news_tiutles
	title = n.get_text()	#get_text()方法标签的text
	link = n.get('href')
	data = {
		'标题' : title,
		'链接' : link
	}
	print(data)
