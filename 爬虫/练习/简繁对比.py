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

    alls_url = []

    def __init__(self, url_dict):
        # 请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.proxies = {
            'http': '192.168.218.246:8628'
        }

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
            self.Analysis(set(str_herf), [v for v in url_dict.values()])

    # 解析()
    def Analysis(self, herf, url_list):

        temp = []  #存放筛选后的数据,暂不能全局
        # 存放所有的链接
        for i in herf:
            # 筛选出所有herf
            if i['href'] != '#' and i['href'] != '#top' and \
            i['href'] != self.path+self.address and i['href'] != self.address \
            and i['href'] not in url_list and self.path+i['href'] not in url_list:
            #判断i['href'] 是否与原始链接一致
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

        # print("这是temp信息", set(temp))
        for i in set(temp):
            if i != self.path + self.address and i.find('@') == -1 :

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
    # url_zh_CN = 'https://www.eddidholdings.com/zh-hans/'  # 简体
    # url_zh_CN = 'https://www.eddidtrust.com/zh-hans/'  # 简体
    # url_zh_TW = 'https://www.eddidholdings.com/zh-hant/'  # 繁体

    url_dict = {
        'url_zh_CN': 'https://www.eddidholdings.com/zh-hans/',
        'url_zh_TW': 'https://www.eddidholdings.com/zh-hant/',
    }

    cr = Contrast_reptile(url_dict)
    cr.get_Url(url_dict)
