#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-30 14:52:42
# @Author  : onedi (onedi@qq.com)
# @Link    : ${link}
# @Version : $Id$

import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

url = 'http://192.168.1.200/index.php?s=/5&page_id=532'		#接口文档地址
interface_name = 'addCommodity'		#需要查询的接口名

driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver')

driver.get(url)		#打开页面
# driver.maximize_window()

search_bar = driver.find_element_by_name('keyword')		#搜索输入框
search_btn = driver.find_element_by_class_name('icon-search')		#搜索按钮

search_bar.clear()		#先清空搜索框
search_bar.send_keys(interface_name)		#在搜索框输入要查下的接口名称	
search_btn.click()		#点击搜索按钮

driver.implicitly_wait(10)		#隐式等待
driver.switch_to_frame('page-content')		#进入页面内容iframe

html = driver.page_source	#打印出网站的html

soup = BeautifulSoup(html,'lxml')

tables = soup.select('table:nth-of-type(1) > tbody > tr > td')	#获取页面中table标签下面的tr标签0
# print(len(tables))
# print(tables)


interface_list = []		#存放爬取出来的参数
parameter = []
list1 = []
for i in range(len(tables)):
	# print(tables[i])
	parameter = re.findall('<td.+>(.+?)</td>',str(tables[i]))

	if parameter == '' or parameter == None or parameter == []:	#判断内容是否为空,为空去掉
		continue
	# print(parameter)

	if i != 0 and i%4 == 0 :
		interface_list.append(list1)
		# print("interface_list = %s" %(interface_list))
		list1 = []

	list1.append(parameter)
	# print("list1 = %s" %(list1))

print(interface_list)



time.sleep(5)
print('结束脚本')
driver.quit()








