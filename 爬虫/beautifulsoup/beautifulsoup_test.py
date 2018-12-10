#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 20:28:43
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

from bs4 import BeautifulSoup  

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a target="_blank" class="linkto" href="http://new.qq.com/omn/20180515/20180515A0GBK3.html">朝韩明日举办高级别会谈 旨在落实首脑会晤共识</a>
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""  

soup = BeautifulSoup(html)

# print(soup.prettify())	#格式化打印内容

# print('title:',soup.title)	#获取title标签
# print(soup.head)		#获取head标签

# print(soup.a)
print(soup.a.string)	#<a>标签中的注释不见了
# print(type(soup.a.string))

# print(soup.a.get('href'))