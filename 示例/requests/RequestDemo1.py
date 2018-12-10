#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import io


# response = requests.get('http://httpbin.org/get')
# print(type(response.text))
# print(response.json())
# print(type(response.json()))
# print(response.text)


# 带参数的GET请求
# response = requests.get('http://httpbin.org/get?name=jyx&age=18')
# print(response.text)


# 带参数的GET请求2
# param = {
#     'name':'jyx',
#     'age' : 19
# }
# response = requests.get('http://httpbin.org/get',params=param)
# print(response.text)


# 添加headers
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
# }
# response = requests.get('https://www.zhihu.com/explore',headers=headers)
# #改变标准输出的默认编码
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') 
# print(response.text)

# 响应 response

response = requests.get('http://www.jianshu.com/')

# 获取响应状态码
print(type(response.status_code),response.status_code)
# 获取响应头信息
print(type(response.headers),response.headers)
# 获取响应头中的cookies
print(type(response.cookies),response.cookies)
# 获取访问的url
print(type(response.url),response.url)
# 获取访问的历史记录
print(type(response.history),response.history)






