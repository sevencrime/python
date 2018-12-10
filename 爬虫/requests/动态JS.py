#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-16 21:37:42
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

import requests
import json
import io
import sys
#改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')



url = 'https://www.toutiao.com/api/pc/focus/'

resp = requests.get(url).text

data = json.loads(resp)		#将resp转换为dict类型

news = data['data']['pc_feed_focus'] 	#返回一个list
# print(news)

for n in news:		#遍历news
	# print(n)
	title = n['title']
	img_url = n['image_url']
	new_url = n['display_url']

	news_url = 'https://www.toutiao.com'+new_url

	print('标题：%s ,新闻地址：%s ,新闻图片:%s ,' %(title,news_url,img_url))



