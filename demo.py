#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-08 19:27:23
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$


import xlrd
import json

path = 'D:/NewType/123.xlsx'


workbook = xlrd.open_workbook(path)
table = workbook.sheets()[0]

nrows = table.nrows
print(nrows)
ncols = table.ncols
print(ncols)

interface = {}

for i in range(nrows):
    if i > 1:
        interface[(table.row_values(i)[0])] = table.row_values(i)[2]
        # print(interface)

print(json.dumps(interface,ensure_ascii=False, encode ='UTF-8'))


