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
import asyncio

import aiohttp
import aiofiles
import brotli
from Crypto.Cipher import AES
from bs4 import BeautifulSoup


class Download_Viedo():

    # 传入一个m3u8地址, 一个名字(可选)
    def __init__(self, downUrl, filename="Test", iskey=False):
        self.downUrl = downUrl
        self.filename = filename.replace(" ", "")
        print(self.filename)
        self.torrentName = ''.join(re.findall(r'[A-Za-z]+-\d+', self.filename)).replace('-', '_') or "viedom3u8"
        self.down_viedo = r"D:\\private\\video"     # 存放最后完整的视频
        self.down_torrent = r"D:\\private\\m3u8file"    # 存放保存的m3u8文件
        self.down_final = r"D:\\private\\final"     # 存放爬取的视频分段

        self.headers = {
            # 'connection': 'keep-alive',
            'connection': 'close',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            # "Connection": "Upgrade",
            # "Upgrade": "HTTP/1.1",
            'Accept-Encoding': 'gzip, deflate, br'
        }
        # requests.adapters.DEFAULT_RETRIES = 5
        self.iskey = iskey
        self.conn = sqlite3.connect("viedo_ts.db")
        self.cursor = self.conn.cursor()

    def get_ip_list(self):
        # print("正在获取代理列表...")
        url = 'http://www.xicidaili.com/nn/'
        html = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        ips = soup.find(id='ip_list').find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        # print("代理列表抓取成功.")
        return ip_list

    def get_random_ip(self,ip_list):
        print("正在设置随机代理...")
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        # 从序列中随机选取一个元素
        proxy_ip = random.choice(proxy_list)
        # self.proxies = {'http': proxy_ip}
        # print("代理设置成功.")
        return proxy_ip

    def get_downUrl_m3u8(self):
        # 请求m3u8文件地址
        resp = requests.get(self.downUrl)
        # 把文件保存到本地
        with open(self.filename + '.m3u8', 'wb') as file:
            file.write(resp.content)

        print("m3u8文件下载成功")
        # 解析m3u8文件
        m3u8Obj = m3u8.load(self.filename + '.m3u8')
        m3u8_len = len(m3u8Obj.segments)
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

        torrentName = self.torrentName

        print("torrentName : {}".format(torrentName) )
        # 创建数据表
        self.cursor.execute("DROP TABLE IF EXISTS {};".format(torrentName))
        '''
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {torrentName} (id INTEGER PRIMARY KEY AUTOINCREMENT, URI VARCHAR(255) NOT NULL, keyUri VARCHAR(255) NOT NULL, long VARCHAR(20) NOT NULL);".format(torrentName=torrentName))
         '''

        self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS {torrentName} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    URI VARCHAR(255) NOT NULL,
                    keyUri VARCHAR(255) NOT NULL,
                    long VARCHAR(20) NOT NULL,
                    isDown BOOLEAN NOT NULL
                );
                """.format(torrentName=torrentName)
            )

        # 遍历m3u8文件
        for ts in m3u8Obj.segments:
            try:
                uri = ts.uri[ts.uri.rindex('/') + 1 : len(ts.uri)] 
                # print(uri)
            except Exception as e:
                uri = ts.uri
            tsurl = path + uri
            # 查询是否重复, 不重复则存入数据库
            if [d for d in self.cursor.execute("SELECT * FROM {0} WHERE URI='{1}';".format(torrentName, tsurl))] == []:
                self.cursor.execute("INSERT OR IGNORE INTO {torrentName} (id, URI, keyUri, long, isDown) VALUES (?, ?, ?, ?, ?);".format(
                    torrentName=torrentName), (None, tsurl, key_bytes, m3u8_len, 0))


    async def download(self, s, key):
        # async with s.request("get", key[1], headers=self.headers, verify_ssl=False, timeout=60) as ts:
        data = b''    
        try:
            async with s.get(key[1], headers=self.headers, verify_ssl=False, timeout=300) as ts:

                # while not ts.content.at_eof():
                #     try:
                #         data = await ts.content.read()
                #     except Exception as e:
                #         print(e)
                #     finally:
                #         return data

                empty_bytes = b''
                data = empty_bytes
                while True:
                    chunk = await ts.content.read(497556)
                    if chunk == empty_bytes:
                        break
                    data += chunk

        except Exception as e:
            print(e)
            # print(data)
        finally:            
            return data

    async def download_ViedoFile(self, semaphore, key):
        # if key[0] % 20 == 0:
        #     # print("休眠10s")
        #     asyncio.sleep(10)
            
        if key[0] % 50 == 0:
            pass
            # print("更换代理IP")
            # self.proxies = self.get_random_ip(self.get_ip_list())

        if self.iskey:
            # 解析m3u8的key
            sprytor = AES.new(key[2], AES.MODE_CBC, IV=key[2])

        start = time.time()
        async with semaphore:
            connector = aiohttp.TCPConnector(limit=100)
            async with aiohttp.ClientSession(connector=connector) as s:
            # async with aiohttp.ClientSession() as s:
                data = await self.download(s, key)
                # print("正在保存 {}".format(key[1]))
                if not data:
                    return False

            while len(data) % 16 != 0:
                data += b"0"

            name = 'clip_{}.ts'.format(str(key[0]).zfill(6))
            # print('开始下载{}'.format(name))
            async with aiofiles.open(name, 'wb') as f:
                if not self.iskey:
                    await f.write(data)
                else:
                    await f.write(sprytor.decrypt(data))

                await f.close()


            print("{} 下载完成".format(name))


    def mergeFile(self, start_time=0):
        print("下载完成！总共耗时 %d s" % (time.time()-start_time))
        os.chdir(self.down_viedo)

        m3u8_len = [_d for _d in self.cursor.execute("SELECT long FROM {} WHERE id=1".format(self.torrentName))][0]
        # 通过m3u8文件长度, 创建一个全list, 用于判断缺少的数
        m3u8list = ['clip_{}.ts'.format(str(n+1).zfill(6)) for n in range(int("".join(m3u8_len)))]
        # 已经下载的文件列表
        dirlist = os.listdir(self.down_final)
        # 求两个list的差集, 校验文件是否缺少
        difflist = [item for item in m3u8list if not item in dirlist]
        samelist = [int(re.sub(r"\D", "", same)) for same in dirlist]   # 已经下载的id
        difflist_id = [int(re.sub(r"\D", "", diff)) for diff in difflist]   # 已经下载的id
        for same in samelist:
            self.cursor.execute("UPDATE {} SET isDown=1 WHERE id={}".format(self.torrentName, int(same)))
        for diff in difflist_id:
            self.cursor.execute("UPDATE {} SET isDown=0 WHERE id={}".format(self.torrentName, int(diff)))

        self.conn.commit()

        if len(difflist) != 0:
            print("还有 {} 个文件没下载".format(len(difflist)))
            # for i in difflist:
            #     print("缺少片段 : {}".format(i))
            
            print("等待10秒继续下载")
            time.sleep(5)
            return self.aio_run()

        print("接下来进行合并……")
        print('copy/b {0}\\*.ts {1}\\{2}.ts'.format(self.down_final, self.down_viedo, self.filename))
        os.system('copy/b {0}\\*.ts {1}\\{2}.ts'.format(self.down_final, self.down_viedo, self.filename))

        print("合并完成，请您欣赏！")

        # 循环从0开始, 固要+1
        # 删除片段
        # for filename in dirlist:
        #     del_file = self.down_final + "\\" + filename
        #     os.remove(del_file)
        # print("视频片段已全部删除")


    def del_file(self, path_data):
        # 删除文件夹下的所有文件
        for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
            file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
            if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
                os.remove(file_data)
            else:
                del_file(file_data)


    def aio_run(self):
        # 读取数据库, 请求ts, 并保存到本地
        os.chdir(self.down_final)

        start = time.time()
        print("创建tasks")
        tasks = []
        _task_time = time.time()
        semaphore = asyncio.Semaphore(60)  # 协程池
        for key in self.cursor.execute("SELECT * FROM {} WHERE isDown=0;".format(self.torrentName)):
            tasks.append(asyncio.ensure_future(self.download_ViedoFile(semaphore, key)))
        print("create tasks time : {}".format(time.time() - _task_time))

        loop = asyncio.get_event_loop()
        try:
            _start = time.time()

            # result = loop.run_until_complete(asyncio.gather(*tasks))
            # for i in result:
            #     print(i)

            doneSet, pendingSet = loop.run_until_complete(asyncio.wait(tasks, timeout=100))
            if pendingSet:
                print(len(pendingSet))
                for pending in pendingSet:
                    pending.cancel()

        except Exception as e:
            print("此次的时间为 : {}".format(time.time() - _start))
            print("Error >>>  {}".format(e))

            # asynci.gather()时用
            # all_tasks = asyncio.Task.all_tasks()
            # for task in all_tasks:
            #     # 将task 取消 返回布尔值
            #     task.cancel()
        finally:
            print("开始合并")
            # 合并ts文件, 并删除ts
            self.mergeFile(start)    



    def run(self):

        # 获取代理IP列表
        # ip_list = self.get_ip_list()
        # 设置随机代理
        # self.proxies = self.get_random_ip(ip_list)


        os.chdir(self.down_torrent)

        # 如果文件不存在或表为空, 则创建
        # count = int([_ for _ in self.cursor.execute("SELECT COUNT(*) FROM {}".format(self.torrentName))][0][0])
        if not os.path.isfile(self.filename + '.m3u8'):
            # 请求m3u8文件, 并保存到本地
            # 解析m3u8文件, 并把加密key和ts存入数据库, 返回一个数据表的名字
            self.get_downUrl_m3u8()
            self.conn.commit()  # 存入数据库后提交事务
            self.del_file(self.down_final)  # 清空视频片段文件
            self.aio_run()
        else:
            self.mergeFile()

        # 删除表数据
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise e



if __name__ == '__main__':
    url = r"https://videocdn.dlyilian.com:8091/20190201/IBJU3RWK177/1000kb/hls/index.m3u8"
    # url = r"https://www.gentaji.com:65/20200302/Eq55Wrvp/1200kb/hls/index.m3u8")
    # http://ttlu70.com/index.php/vod/play/id/25059/sid/1/nid/1.html
    # url = r"https://youku.haokzy-tudou.com/ppvod/4yf2LZrW.m3u8")
    name = "IPX-177 让高傲自大的妹妹穿上过膝袜，产生只属于我的绝对领域，并让她变成了喜欢我的癡女。 相泽南"
    dv = Download_Viedo(url, name, iskey=True)

    dv.run()

    # difftup = dv.mergeFile()
    # print(tuple(difftup))

    
# https://videocdn.dlyilian.com:8091/20190723/HUNTA-558_CH_SD/1000kb/hls/index.m3u8     true
