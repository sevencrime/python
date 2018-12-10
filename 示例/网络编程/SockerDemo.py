#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

# 创建一个socker
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 建立连接
s.connect(('www.sina.com.cn', 80))

# 发送数据
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# 接收数据
buffer = []

while True:
    d = s.recv(1024)    #调用recv(max)方法，一次最多接收指定的字节数
    if d :
        buffer.append(d)
    else :
        break

data = b''.join(buffer)
# print(data)
s.close()

header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))

with open('sina.html' , 'wb') as f :
    f.write(html)

