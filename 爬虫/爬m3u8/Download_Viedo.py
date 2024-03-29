#!/usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
import random
import sqlite3
import time
import m3u8
import requests
import os
import re

from Crypto.Cipher import AES
from bs4 import BeautifulSoup


class Download_Viedo():

    # 传入一个m3u8地址, 一个名字(可选)
    def __init__(self, downUrl, filename="Test", iskey=False):
        self.downUrl = downUrl
        self.filename = filename
        self.down_viedo = r"D:\\private\\video"     # 存放最后完整的视频
        self.down_torrent = r"D:\\private\\m3u8file"    # 存放保存的m3u8文件
        self.down_final = r"D:\\private\\final"     # 存放爬取的视频分段

        self.headers = {
            # 'Connection': 'Keep-Alive',
            'Connection': 'close',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        # requests.adapters.DEFAULT_RETRIES = 5
        self.iskey = iskey

    def get_ip_list(self):
        print("正在获取代理列表...")
        url = 'http://www.xicidaili.com/nn/'
        html = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        ips = soup.find(id='ip_list').find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        print("代理列表抓取成功.")
        return ip_list

    def get_random_ip(self,ip_list):
        print("正在设置随机代理...")
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        # 从序列中随机选取一个元素
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        print("代理设置成功.")
        return proxies


    def get_downUrl_m3u8(self, cursor):
        # 请求m3u8文件地址
        resp = requests.get(self.downUrl)
        # 把文件保存到本地
        with open(self.filename + '.m3u8', 'wb') as file:
            file.write(resp.content)

        print("m3u8文件已经保存")
        # 解析m3u8文件
        m3u8Obj = m3u8.load(self.filename + '.m3u8')
        self.m3u8_len = len(m3u8Obj.segments)
        print("M3U8文件的长度为 : {}".format(len(m3u8Obj.segments)))

        # 正则提取下载地址
        path = ''.join(re.findall(r".*(?=\/)/", self.downUrl))
        key_bytes = ''
        if self.iskey:
            # 正则提取m3u8文件加密的地址key_uri
            key_uri = path + ''.join(re.findall(r'AES.+URI="(.*key)', resp.text))
            print("m3u8文件的keyURI为 : {}".format(key_uri))
            # 获取key的16位bytes
            key_bytes = requests.get(key_uri).content
            print("key 为: {}".format(key_bytes))
        torrentName = ''.join(re.findall(r'[A-Za-z]+-\d+', self.filename)).replace('-', '_')
        if torrentName == "":
            torrentName = "viedom3u8" 

        print("torrentName : {}".format(torrentName) )
        # 创建数据表
        cursor.execute("DROP TABLE IF EXISTS {};".format(torrentName))
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS {torrentName} (id INTEGER PRIMARY KEY AUTOINCREMENT, URI VARCHAR(255) NOT NULL, keyUri VARCHAR(255) NOT NULL );".format(torrentName=torrentName))

        # 遍历m3u8文件
        for ts in m3u8Obj.segments:
            try:
                uri = ts.uri[ts.uri.rindex('/') + 1 : len(ts.uri)] 
                # print(uri)
            except Exception as e:
                uri = ts.uri
            tsurl = path + uri
            # 查询是否重复, 不重复则存入数据库
            if [d for d in cursor.execute("SELECT * FROM {0} WHERE URI='{1}';".format(torrentName, tsurl))] == []:
                cursor.execute("INSERT OR IGNORE INTO {torrentName} (id, URI, keyUri) VALUES (?, ?, ?);".format(
                    torrentName=torrentName), (None, tsurl, key_bytes))

        return torrentName

    def download_ViedoFile(self, key, s, ip_list, proxies):
        if key[0] % 20 == 0:
            # print("休眠10s")
            time.sleep(10)
        if key[0] % 50 == 0:
            # print("更换代理IP")
            proxies = self.get_random_ip(ip_list)

        if self.iskey:
            # 解析m3u8的key
            sprytor = AES.new(key[2], AES.MODE_CBC, IV=key[2])

        start = time.time()
        while True:
            try:
                ts = s.get(key[1], headers=self.headers, proxies=proxies, timeout=(3,10))
            except requests.exceptions.ConnectionError:
                ts.status_code = "Connection refused"
                if time.time() - start > 300:
                    print("文件 {} 没有下载, 报错状态码为: Connection refused".format(key[0]))
                    break
                time.sleep(30)
                continue

            except Exception as e:
                ts.status_code = "Connection refused"
                if time.time() - start > 300:
                    print(e, "文件 {} 没有下载, 报错状态码为: {}".format(key[0], ts.status_code))
                    break
                time.sleep(30)
                continue

            while len(ts.content) % 16 != 0:
                ts += b"0"

            name = 'clip_{}.ts'.format(str(key[0]).zfill(6))
            # print('开始下载{}'.format(name))
            with open(name, 'wb') as f:
                if not self.iskey:
                    f.write(ts.content)
                else:
                    f.write(sprytor.decrypt(ts.content))

            # 能走到这里, 直接退出循环
            break

    def mergeFile(self, start_time= 0):
        print("下载完成！总共耗时 %d s" % (time.time()-start_time))
        os.chdir(self.down_viedo)

        # self.m3u8_len = 7502
        # 通过m3u8文件长度, 创建一个全list, 用于判断缺少的数
        m3u8list = ['clip_{}.ts'.format(str(n+1).zfill(6)) for n in range(self.m3u8_len)]
        # 获取文件夹中的所有文件, list
        dirlist = os.listdir(self.down_final)
        # 求两个list的差集, 校验文件是否缺少
        difflist = [item for item in m3u8list if not item in dirlist]
        if len(difflist) != 0:
            difftup = []
            for i in difflist:
                print("缺少片段 : {}".format(i))
                difftup.append(int(i[5:-3]))

            self.run(difftup)

        print("接下来进行合并……")
        os.system('copy/b {0}\\*.ts {1}\\{2}.ts'.format(self.down_final, self.down_viedo, self.filename))

        print("合并完成，请您欣赏！")

        # 循环从0开始, 固要+1
        # 删除片段
        # for filename in dirlist:
        #     del_file = self.down_final + "\\" + filename
        #     os.remove(del_file)
        # print("视频片段已全部删除")


    def run(self, difftup=[]):

        # 获取代理IP列表
        ip_list = self.get_ip_list()
        # 设置随机代理
        proxies = self.get_random_ip(ip_list)

        conn = sqlite3.connect("viedo_ts.db")
        cursor = conn.cursor()
        os.chdir(self.down_torrent)
        # 请求m3u8文件, 并保存到本地
        # 解析3eu8文件, 并把加密key和ts存入数据库, 返回一个数据表的名字
        self.torrentName = self.get_downUrl_m3u8(cursor)
        conn.commit()

        # 读取数据库, 请求ts, 并保存到本地
        os.chdir(self.down_final)

        poollist = []
        s = requests.session()
        # 创建进程池
        p = multiprocessing.Pool(70)

        if len(difftup) > 0:
            # 查询数据库
            start = time.time()
            print("开始下载视频")
            if len(difftup) == 1:
                self.download_ViedoFile([key for key in cursor.execute("SELECT * FROM {} WHERE id = {};".format(self.torrentName, difftup[0]))][0], s, ip_list, proxies)
            else:
                print("SELECT * FROM {} WHERE id in {};".format(self.torrentName, tuple(difftup)))
                for key in cursor.execute("SELECT * FROM {} WHERE id in {};".format(self.torrentName, tuple(difftup))):
                    # self.download_ViedoFile(key, s)
                    p.apply_async(self.download_ViedoFile, args=(key, s, ip_list, proxies))
                    # poollist.append(p.apply_async(self.download_ViedoFile, args=(key, s, ip_list, proxies)))            
        else:
            # 查询数据库
            start = time.time()
            print("开始下载视频")
            # for key in cursor.execute("SELECT * FROM {}".format(self.torrentName)):
            for key in cursor.execute("SELECT * FROM {};".format(self.torrentName)):
                # self.download_ViedoFile(key, s)
                p.apply_async(self.download_ViedoFile, args=(key, s, ip_list, proxies))
                # poollist.append(p.apply_async(self.download_ViedoFile, args=(key, s, ip_list, proxies)))

        # for i in poollist:
        #     print(i.get() or '')

        p.close()
        p.join()
        cursor.close()
        conn.close()

        # 合并ts文件, 并删除ts
        self.mergeFile(start)



if __name__ == '__main__':
    url = r"https://videozm.whqhyg.com:8091/20200518/1xuDAJ9J/1000kb/hls/index.m3u8"
    # http://ttlu70.com/index.php/vod/play/id/25059/sid/1/nid/1.html
    # url = r"https://youku.haokzy-tudou.com/ppvod/4yf2LZrW.m3u8")
    name = "ADN-138"
    dv = Download_Viedo(url, name, iskey=False)
    dv.run()
    # dv.mergeFile(time.time())


