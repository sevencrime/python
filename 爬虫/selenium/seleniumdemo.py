#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options

# 建立browsermobproxy服务, 需指定browsermob-proxy, 类似chromedriver
server = Server("D:/下载/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat")
server.start()
# 创建代理
proxy = server.create_proxy()

chrome_options = Options()
# 为chrome启动时设置代理
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
# 静默模式, 不显示浏览器
chrome_options.add_argument('headless')
driver = webdriver.Chrome(executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe', chrome_options=chrome_options)

# base_url = "https://www.iesdouyin.com/share/user/63174596206"
# 需要解析的链接
base_url = "https://www.kpl052.com/Watch-online/146998-1-1.html"

# HTTP Archive format(HAR文件)，是用来记录浏览器加载网页时所消耗的时间的工具。
# 这设置了要记录的新HAR
proxy.new_har(ref="HAR啦", options={'captureHeaders': True, 'captureContent': True}, title="标题")
driver.get(base_url)

# 获取HAR
result = proxy.har
print(result)
m3u8UrlSet = set()
for entry in result['log']['entries']:
    _url = entry['request']['url']
    # 根据URL找到数据接口
    if "m3u8" in _url:
        m3u8UrlSet.add(_url)
        print(_url)

    # 判断响应是否存在error
    if "_error" in entry['response'].keys():
        print("Url : {} 响应报错信息为 error : {}".format(_url, entry["response"]["_error"]))


# print(m3u8UrlSet)
# 代理需要关闭
server.stop()
driver.quit()