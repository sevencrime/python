#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-17 17:11:40
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

import io
import sys
#改变标准输出的默认编码
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
import os
import requests 
from bs4 import BeautifulSoup	#BeautifulSoup：HTML的解析库
from PIL import Image
from io import BytesIO
import time
from multiprocessing import Pool

def get_href():

	url = 'http://www.win4000.com/zt/xinggan.html'

	resp = requests.get(url).text
	soup = BeautifulSoup(resp,'lxml')
	# print(soup)

	# 寻找图片标签
	title_url = soup.select('div.tab_box > * > ul.clearfix > li > a')
	# print(title_url)


	return title_url

def get_img(href):

	# for i in title_url:
	# 	# print(i)
	# 	href = i['href']
	# 	if not href.find('http://www.win4000.com/'):
	# 		# print(href)
	# 		# get_img_index(href)

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

# 新建目录,且判断目录是否存在
def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False


def save_img(title,data_src):

	resp = requests.get(data_src)
	image = Image.open(BytesIO(resp.content))
	# print(data['title'])

	t = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
	print("正在爬取图片")

	image.save('D:/郑某人/测试图片/爬虫/%s.jpg' %(title+t))

	# 自定义像素
	# width = '234'
	# height = '180'

	# 设置图片像素，返回一个特定大小的image对象
	# resizedim = image.resize((int(width),int(height)))

	#判断文件夹是否存在,不存在则创建
	# mkpath = 'D:/郑某人/测试图片/爬虫/%s' %(width+'×'+height)
	# mkdir(mkpath)
	# resizedim.save(mkpath+'/%s.jpg' %(title+t))


if __name__ == '__main__' :
	title_url = get_href()


	p = Pool(8)
	for i in title_url:
		href = i['href']
		if not href.find('http://www.win4000.com/'):
			# get_img(href)
			p.apply_async(get_img,args=(href,))

	p.close()
	p.join()

