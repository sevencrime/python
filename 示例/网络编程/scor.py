#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect(('127.0.0.1', 9090));
print(s.recv(1024).decode('utf-8'));
for data in [b'lk', b'aa', b'bb']:
    s.send(data);
    print(s.recv(1024).decode('utf-8'));
s.send(b'exit');
s.close();
