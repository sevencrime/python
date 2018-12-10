#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-17 17:11:40
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

import io
import sys
#改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

import requests 
from bs4 import BeautifulSoup	#BeautifulSoup：HTML的解析库
from PIL import Image
from io import BytesIO
import time
from multiprocessing import Pool

def get_href(i):
	# https://www.nvshens.com/
	url = 'http://www.win4000.com/zt/xinggan.html'

	resp = requests.get(url).text
	soup = BeautifulSoup(resp,'lxml')
	# print(soup)

	# 寻找图片标签
	title_url = soup.select('div.tab_box > * > ul.clearfix > li > a')
	# print(title_url)

	for i in title_url:
		# print(i)
		href = i['href']
		if not href.find('http://www.win4000.com/'):
			# print(href)
			# get_img_index(href)
			get_img(href)


def get_img(href):

	resp = requests.get(href).text
	soup = BeautifulSoup(resp,'lxml')

	img_url = soup.select('div.scroll-img-cont > ul#scroll > li > a > img')
	# print(len(img_url))

	for i in img_url:
		title = i['title']
		# print(i)
		data_original = i['data-original']
		data_src = data_original[:-11]+'.jpg'
		# print(data_original[:-11]+'.jpg')
		# data = {
		# 	'title' : title,
		# 	'src' : data_original[:-11]+'.jpg'
		# }
		# print(data)

		save_img(title,data_src)

def save_img(title,data_src):

	resp = requests.get(data_src)
	image = Image.open(BytesIO(resp.content))
	# print(data['title'])

	t = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))

	image.save('D:/Documents/Pictures/爬虫/%s.jpg' %(title+t))

if __name__ == '__main__' :
	# get_href()

	p = Pool(4)
    for i in range(5):
        p.apply_async(get_href, args=(i,))
    p.close()
    p.join()
