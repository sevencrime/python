#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-29 19:33:33
# @Author  : onedi (onedi@qq.com)
# @Link    : ${link}
# @Version : $Id$


import urllib.request
import requests

str1 = '{"address":"广东省深圳市南山区桑达科技大厦","agentAccount":11111111,"balance":0.0,"city":"深圳市","colorBlue":0,"colorGreen":0,"colorRed":255,"comment":"这是注释信息","country":"China","email":"17620446727@163.com","equity":300000000000.0,"freeMargin":300000000000.0,"group":"demo\\test","id":"307051066","isEnabled":true,"isEnabledChangePassword":true,"isReadOnly":false,"leverage":500,"login":266586,"margin":0.0,"name":"接口测试","password":null,"passwordInvestor":null,"phone":"15089514626","phonePassword":"","sendReports":true,"state":"广东省","status":"NR","zipCode":"665856"}'




str2 = str1.replace("=", ":")	#把'='替换为':'

str4 = urllib.request.unquote(str2)	#urldecode解码

arr1 = str4.split('&')	#切割字符串,保存到arr中
# print(arr1)

dict1 = {}	#存放dict格式参数

for i in range(len(arr1)):
	index = arr1[i].find(':')
	# print("********",arr1[i][index+1:])
	try:
		dict1[arr1[i][0:index]] = int(arr1[i][index+1:])
	except Exception as e:
		dict1[arr1[i][0:index]] = arr1[i][index+1:]

print("请求参数的长度为:  ",len(dict1))
print("请求的参数内容为:\r",dict1)


for k,v in dict1.items():
	# print(k,v)
	if v == '' or v == None :
		print("参数的 %s 字段值为空 " %(k))

	elif v == 0 :
		print("参数的 %s 字段值为0" %(k))


# dict1['loginPwd'] = 'ss123456'
resp = requests.post('http://192.168.1.3:8081/RmarketShop/account/userLogin.html',data=dict1).json()
print(resp)

