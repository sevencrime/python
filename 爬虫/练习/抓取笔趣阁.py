#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-18 22:39:31
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


# 获取小说的url
def get_url():
	url = 'http://www.biquge.com.tw/'
	page = requests.get(url)
	tree = html.fromstring(page.content)

	# print(tree)

	temp = tree.xpath('//a')

	data = []

	for t in temp:
		s = {}
		if not t.get('href').find('http://www.biquge.com.tw'):
			if not t.text == '笔趣阁' :
				if not t.text == None :

					s = {
						'text' : t.text,
						'href' : t.get('href')
					}
					data.append(s)

	print(data)
	return data

	# 下一步：爬取其中一部小说

def save_sql(title,author,updates,lately,intro):
	pass


# 获取章节url
def get_chapter(data,title):
	# https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
	# 上面的链接可以对字典列表去重
	# print([dict(t) for t in set([tuple(d.items()) for d in data])])

	resp = requests.get(data['href'])
	resp.encoding = 'gbk'
	tree = html.fromstring(resp.content)

	chapter = tree.xpath('//div[@id="list"]/dl/dd/a')

	soup_info = BeautifulSoup(resp.text,'lxml')
	info = soup_info.select('#wrapper .box_con #maininfo #info p')
	author = info[0].text.replace("\u00a0", " ") 	#作者，需要去掉&nbsp
	updates = info[2].text.replace("最后更新：","") 	#更新时间
	lately = info[3].text 	#最新章节
	intro = soup_info.select('#wrapper .box_con #maininfo #intro')[0].text.strip()	#小说简介
	
	# print(title,author,updates,lately,intro)
	# save_sql(title,author,updates,lately,intro)
	conn = mysql.connector.connect(user='root', password='123456', database='fiction', use_unicode=True)
	cursor = conn.cursor()
	cursor.execute("insert into novel_info (title,author,update1,lately,intro)\
	values (%s, %s, %s, %s, %s)", [title,author,updates,lately,intro])
	conn.commit()
	cursor.close()
	conn.close()

	# num = 0  #用来判断是否再开头写入txt信息
	# for c in chapter:		#遍历出每一章节的URL

	# 	s = {}
	# 	s = {
	# 		'book_href' : data['href'] , 
	# 		'name' : c.text ,
	# 		'chapter_href' : c.get('href')

	# 	}	
	# 	print('正在爬取 ： %s\r' %(s['name']))

	# 	books_href = s['book_href'][:-10]+s['chapter_href']		#获取每一章的href
	# 	# print(books_href)


	# 	r = requests.get(books_href)	#请求每一章节
	# 	r.encoding = 'gbk'		#设置response编码

	# 	soup = BeautifulSoup(r.text,'lxml')

	# 	content = soup.select('div #content')
	# 	#去除&nbsp和<br/>
	# 	a = str(content).replace("\u00a0", " ").replace("<br/>","")
	# 	#正则去除html标签
	# 	dr = re.compile(r'.<[^>]+>.',re.S)
	# 	text = dr.sub('', a)	#章节的正文
	# 	# print(text)


	# 	path = 'D:/Documents/Pictures/小说爬虫'
	# 	with open(path+'/%s.txt' %(title), 'a+' , encoding = 'utf-8') as f :
	# 		if num == 0:
	# 			f.write('书名：%s\n' %title)
	# 			f.write('作者：%s\n' %author)
	# 			f.write('更新时间：%s\n' %updates)
	# 			f.write('最新章节：%s\n' %lately)
	# 			f.write('小说简介:\n%s\n' %intro)
	# 		f.write(s['name']+'\n\r\n')
	# 		f.write(text+'\n\r\n')
	# 		f.close()

	# 	num += 1

if __name__ == '__main__' :
	data = get_url()

	# conn = mysql.connector.connect(host='localhost', port='3306', \
	# 	user='root', password='123456', database='fiction', charset='utf8')
	# cursor = conn.cursor()

	p = Pool(16)
	for d in [dict(t) for t in set([tuple(d.items()) for d in data])] :
		print('当前爬取的小说为：%s' %(d['text']))
		p.apply_async(get_chapter, args = (d,d['text']))
	p.close()
	p.join()



	# cursor.close()
	# conn.close()

	
