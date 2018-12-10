#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-18 11:16:19
# @Author  : onedi (onedi@qq.com)
# @Link    : localhost
# @Version : $Id$

import requests
from PIL import Image
from io import BytesIO
import time
url = 'http://pic1.win4000.com/wallpaper/2018-05-17/5afd488a87d34.jpg'

resp = requests.get(url)

image = Image.open(BytesIO(resp.content))

print(image.size)

# 设置图片像素，返回一个特定大小的image对象
resizedim = image.resize((234,180))

print(resizedim.size)

t = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
# print(t)

image.save('E:/郑某人/测试图片/爬虫/%s.jpg' %(t))
# image.show()

resizedim.save('E:/郑某人/测试图片/爬虫/%s.jpg' %(t))


