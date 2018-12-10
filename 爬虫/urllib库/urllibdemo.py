#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-14 21:25:00
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

from urllib import request
import io
import sys
#改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

if __name__ == '__main__':

	# urllib使用使用request.urlopen()打开和读取URLs信息,返回resp
	response = request.urlopen('http://fanyi.baidu.com')
	# 同个read()读取resp
	html = response.read()

	html = html.decode('utf-8')
	print(html)
