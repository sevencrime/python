#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello')
def hello():
    return 'PYTHON'


if __name__ == '__main__':
    # app.run()
    # 参数host:外部可访问的服务器
    app.run(host='0.0.0.0',debug=True)


