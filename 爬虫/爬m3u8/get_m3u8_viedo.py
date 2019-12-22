#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import os
import time
import random
import re
import m3u8
import sqlite3
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options


class ViedeoCrawler():

    MYSQL = False

    def __init__(self, url=""):
        self.url = url
        self.down_path = r"D:\\private\\爬虫"
        self.final_path = r"D:\\private"
        try:
            self.name = re.findall(r'/[A-Za-z]*-[0-9]*',self.url)[0][1:]
        except:
            self.name = "uncensord"
        self.headers = {
            # 'Connection': 'Keep-Alive',
            'Connection': 'close',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        requests.adapters.DEFAULT_RETRIES = 5


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

    def get_uri_from_m3u8(self, cursor):
        print("正在解析真实下载地址...")
        torrentNamelist = []

        # 遍历torrent 未保存成文件的数据
        for data in cursor.execute("SELECT * FROM torrent WHERE isGet != 1"):
            print(data)
            torrentName = ''.join(re.findall(r'[A-Za-z]+-\d+', data[1])).replace('-', '_')
            cursor.execute("CREATE TABLE IF NOT EXISTS {torrentName} (id INTEGER PRIMARY KEY AUTOINCREMENT, Url VARCHAR(255) NOT NULL, isGet INT NOT NULL);".format(torrentName=torrentName))

            with open(torrentName+'.m3u8', 'wb') as file:
                file.write(requests.get("".join(data[2])).content)

            m3u8Obj = m3u8.load(torrentName+'.m3u8')
            print("解析完成.")
            # return m3u8Obj.segments
            # 创建表, 判断是否重复IF NOT EXISTS
            # c = self.cursor.execute("select count(*) from sqlite_master where type='table' and name = 'temp';")
            print("m3u8Obj的长度为 : {}".format(len(m3u8Obj.segments)))
            # 提取URL连接地址
            path = ''.join(re.findall(r".*(?=\/)/", "".join(data[2])))
            for key in m3u8Obj.segments:
                tsurl = path + key.uri
                # 插入记录
                # self.cursor.execute("INSERT OR IGNORE INTO temp (id, Url, isGet) VALUES (?, ?, ?);", (None, tsurl, 0))
                cursor.execute("INSERT OR IGNORE INTO {torrentName} (id, Url, isGet) VALUES (?, ?, ?);".format(torrentName=torrentName), (None, tsurl, 0))

            # 改变torrent表的isGet, 表示已爬取过
            cursor.execute("UPDATE torrent set isGet = 1 where id={}".format(data[0]))
            torrentNamelist.append(torrentName)

            # 删除m3u8文件
            try:
                os.remove(torrentName +'.m3u8')
            except:
                pass

        # 提交事务
        conn.commit()


    def get_viedo_downURL(self, cursor):
        print("开始请求资源网站")
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

        driver = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
            chrome_options=chrome_options)

        # driver.set_script_timeout(3)

        # 这设置了要记录的新HAR(HTTP Archive format(HAR文件)，是用来记录浏览器加载网页时所消耗的时间的工具)
        proxy.new_har(ref="HAR啦", options={'captureHeaders': True, 'captureContent': True}, title="标题")
        driver.get(self.url)
        title = driver.title
        torrentName = ''.join(re.findall(r'[A-Za-z]+-\d+', title)).replace('-', '_')
        # 获取HAR
        result = proxy.har
        print(result)

        # m3u8UrlSet = set()
        # 把爬取的链接和标题存入数据库
        cursor.execute("CREATE TABLE IF NOT EXISTS torrent(id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(255) NOT NULL, fileUrl VARCHAR(255) NOT NULL, isGet INT NOT NULL);")
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # 根据URL找到数据接口
            if "m3u8" in _url:
                print("找到M3U8文件了")
                print(_url)
                cursor.execute("INSERT INTO torrent(id, title, fileUrl, isGet) VALUES (?, ?, ?, ?);", (None, title, _url, 0))
                # m3u8UrlSet.add(_url)
                return torrentName

            # 判断响应是否存在error
            if "_error" in entry['response'].keys():
                print("Url : {} 响应报错信息为 error : {}".format(_url, entry["response"]["_error"]))

        # print(m3u8UrlSet)
        # 代理需要关闭
        print("已经要关闭啦!!!!")
        server.stop()
        driver.quit()

        return torrentName


    def run(self, cursor):
        print("开始执行程序")
        os.chdir(self.down_path)

        torrentName = ''
        # # 开始请求资源网站
        # torrentName = self.get_viedo_downURL(cursor)
        # # 解析M3U8文件
        # self.get_uri_from_m3u8(cursor)

        self.ip_list = self.get_ip_list()
        self.proxies = self.get_random_ip(self.ip_list)

        return torrentName


    def generateFile(self, key, s):

        if key[0] % 20 == 0:
            print("休眠10s")
            time.sleep(10)
        if key[0] % 50 == 0:
            print("更换代理IP")
            self.proxies = self.get_random_ip(self.ip_list)
        try:
            resp = s.get(key[1], headers=self.headers, proxies=self.proxies, timeout=(3,10))
        except Exception as e:
            print(e, "文件 {} 没有下载, 报错状态码为: {}".format(key[0], resp.status_code))
            return True

        name = 'clip_{}.ts'.format(str(key[0]).zfill(6))
        print('开始下载{}'.format(name))
        with open(name, 'wb') as f:
            f.write(resp.content)
            # f.flush()
            # os.fsync(f)

    def mergeFile(self, torrentName, start_time= 0):
        print("下载完成！总共耗时 %d s" % (time.time()-start_time))
        import pdb; pdb.set_trace()
        os.chdir(self.down_path)
        print("接下来进行合并……")
        os.system('copy/b %s\\*.ts %s\\%s.ts' % (self.down_path,self.final_path, torrentName))
        print("合并完成，请您欣赏！")
        # y = input("请检查文件完整性，并确认是否要删除碎片源文件？(y/n)")
        # if y=='y':
        #     files = os.listdir(self.down_path)
        #     for filena in files:
        #         del_file = self.down_path + "\\" + filena
        #         os.remove(del_file)
        #     print("碎片文件已经删除完成")
        # else:
        #     print("不删除，程序结束。")


if __name__=='__main__':
    url = r"https://www.kpl052.com/Watch-online/146998-1-1.html"
    crawler = ViedeoCrawler(url)
    conn = sqlite3.connect("viedo_ts.db")
    cursor = conn.cursor()

    torrentName = crawler.run(cursor)
    torrentName = 'SDMU_638'
    s = requests.session()
    p = Pool(40)
    start = time.time()
    for key in cursor.execute("SELECT * FROM {}".format(torrentName)):
        p.apply_async(crawler.generateFile, args=(key, s, ))

    p.close()
    p.join()
    # 改变torrent表的isGet, 表示已爬取过
    cursor.close()
    conn.close()
    crawler.mergeFile(torrentName, start)


