#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-04 11:09:29
# @Author  : Onedi (Onedi@qq.com)
# @Link    : ***
# @Version : $Id$

from hanziconv import HanziConv
from bs4 import BeautifulSoup
import requests
import re


class Contrast_reptile:

    def __init__(self):
        # 请求头
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.proxies = {
            'http': '192.168.218.246:8628'
        }
        # url主题
        self.path = ''
        # print("path = ", self.path)
        # url主页面
        self.url_zh_TW = 'https://www.eddidholdings.com/zh-hant/'  # 繁体

    def Request(self, url):

        resp = requests.get(
            url,
            headers=self.headers,
            # proxies=self.proxies
        ).text

        # BeautiFulSoup解析
        soup = BeautifulSoup(resp, 'lxml')
        # print("title:",soup.title)
        return soup

    # 请求
    def get_Url(self, url_dict):
        for self.key, url in url_dict.items():

            self.path = re.search(".+com", url).group()
            self.address = url[len(self.path):]

            print("正在请求页面 :", url)
            soup = self.Request(url)
            # print(content_list)
            # 对比
            self.comparison(soup)

            # 提取所有a标签
            str_herf = soup.select("a")
            # print(set(str_herf))
            self.Analysis(set(str_herf))

    # 解析()
    def Analysis(self, herf):
        # import pdb
        # pdb.set_trace()
        temp = []
        # 存放所有的链接
        for i in herf:
            # 筛选出所有herf
            if i['href'] != '#' and i['href'] != '#top':
                if str(i['href']).find(self.path):
                    # print("N0: ",i['href'])
                    temp.append(self.path + i['href'])
                    # print("正在请求子链接 :", self.path + i['href'])
                    # soup = self.Request(self.path + i['href'])
                else:
                    # print("YES",i['href'])
                    temp.append(i['href'])
                    # print("正在请求子链接 :", i['href'])
                    # soup = self.Request(i['href'])

        for i in set(temp):
            if i != self.path + self.address and i.find('@') == -1 and i != self.url_zh_TW:

                print("正在请求子链接 :", i)

                soup = self.Request(i)
                print("title:", soup.title)

                # print(content_list)
                # 对比
                self.comparison(soup)

                # 子页面所有的a标签
                link_herf = soup.select("a")

                # 两个list相交,所有的herf
                diff_herf = self.process(herf, link_herf)

                if len(diff_herf) != 0:
                    Analysis(diff_herf)

    # 处理数据
    def process(self, all_herf, link_herf):
        alls = []
        links = []
        for i in all_herf:
            if i['href'] != '#' and i['href'] != '#top':
                if str(i['href']).find(self.path):
                    alls.append(self.path + i['href'])
                else:
                    alls.append(i['href'])

        for j in all_herf:
            if j['href'] != '#' and j['href'] != '#top':
                if str(j['href']).find(self.path):
                    links.append(self.path + j['href'])
                else:
                    links.append(j['href'])

        diff_herf = list(set(links).difference(set(alls)))
        print("diff_herf:", diff_herf)
        print("diff", len(diff_herf))

        return diff_herf

    # 对比
    def comparison(self, soup):

        # 获取页面所有文字
        text = re.findall("[\u4e00-\u9fa5]", soup.get_text())
        print("执行对比")
        # 判断是否简体繁体
        if self.key == 'url_zh_CN':
            # 转简体
            Conversion = HanziConv.toSimplified(text)
        elif self.key == 'url_zh_TW':
            # 转繁体
            Conversion = HanziConv.toTraditional(text)
        for i in range(len(text)):

            if text[i] not in Conversion[i]:
                print("简体: %s , 繁体: %s" % (text[i], Conversion[i]))


if __name__ == '__main__':
    url_zh_CN = 'https://www.eddidholdings.com/zh-hans/'  # 简体
    # url_zh_CN = 'https://www.eddidtrust.com/zh-hans/'  # 简体
    # url_zh_TW = 'https://www.eddidholdings.com/zh-hant/'  # 繁体

    url_dict = {
        'url_zh_CN': 'https://www.eddidholdings.com/zh-hans/',
        'url_zh_TW': 'https://www.eddidholdings.com/zh-hant/'
    }

    cr = Contrast_reptile()
    cr.get_Url(url_dict)
