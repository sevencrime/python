#!/usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
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

    def __init__(self, url, func):
        self.url = url
        self.code = code
        self.down_path = r"D:\\private\\爬虫"
        self.final_path = r"D:\\private"
        try:
            self.name = re.findall(r'/[A-Za-z]*-[0-9]*',self.url)[0][1:]
        except:
            self.name = "uncensord"
        self.headers = {
            'Connection': 'Keep-Alive',
            # 'Connection': 'close',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

        # 连接数据库, 不存在则自动创建
        self.conn = sqlite3.connect("viedo_ts.db")
        # 创建游标cursor
        self.cursor = self.conn.cursor()

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

    def get_uri_from_m3u8(self):
        print("正在解析真实下载地址...")
        torrentNamelist = []

        # 遍历torrent 未保存成文件的数据
        for data in self.cursor.execute("SELECT * FROM torrent WHERE isGet=0"):
            print(data)
            torrentName = ''.join(re.findall(r'[A-Za-z]+-\d+', data[1])).replace('-', '_')
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {torrentName} (id INTEGER PRIMARY KEY AUTOINCREMENT, Url VARCHAR(255) NOT NULL, isGet INT NOT NULL);".format(torrentName=torrentName))

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
                self.cursor.execute("INSERT OR IGNORE INTO {torrentName} (id, Url, isGet) VALUES (?, ?, ?);".format(torrentName=torrentName), (None, tsurl, 0))

            # 改变torrent表的isGet, 表示已爬取过
            self.cursor.execute("UPDATE torrent set isGet = 1 where id={}".format(data[0]))
            torrentNamelist.append(torrentName)

        # 提交事务
        self.conn.commit()
        # 删除m3u8文件
        try:
            os.remove(torrentName +'.m3u8')
        except:
            pass


    def get_viedo_downURL(self):
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
        # chrome_options.add_argument('headless')

        driver = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
            chrome_options=chrome_options)

        # driver.set_script_timeout(3)

        # 这设置了要记录的新HAR(HTTP Archive format(HAR文件)，是用来记录浏览器加载网页时所消耗的时间的工具)
        proxy.new_har(ref="HAR啦", options={'captureHeaders': True, 'captureContent': True}, title="标题")
        driver.get(self.url)
        title = driver.title
        # 获取HAR
        result = proxy.har
        print(result)
        # m3u8UrlSet = set()
        # 把爬取的链接和标题存入数据库
        self.cursor.execute("CREATE TABLE IF NOT EXISTS torrent(id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(255) NOT NULL, fileUrl VARCHAR(255) NOT NULL, isGet INT NOT NULL);")
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # 根据URL找到数据接口
            if "m3u8" in _url:
                print("找到M3U8文件了")
                print(_url)
                self.cursor.execute("INSERT INTO torrent(id, title, fileUrl, isGet) VALUES (?, ?, ?, ?);", (None, title, _url, 0))
                # m3u8UrlSet.add(_url)

            # 判断响应是否存在error
            if "_error" in entry['response'].keys():
                print("Url : {} 响应报错信息为 error : {}".format(_url, entry["response"]["_error"]))

        # print(m3u8UrlSet)
        # 代理需要关闭
        print("已经要关闭啦!!!!")
        server.stop()
        driver.quit()

        torrentName = ''.join(re.findall(r'[A-Za-z]+-\d+', title)).replace('-', '_')

        return torrentName

    def get_viedo(self, key, ip, proxies):
        import pdb; pdb.set_trace()

        if key[0] % 20 == 0:
            print("休眠10s")
            time.sleep(10)
        if key[0] % 50 == 0:
            print("更换代理IP")
            proxies = self.get_random_ip(ip)
        try:
            # 存入数据库
            resp = requests.get(key[1], headers=self.headers, proxies=proxies)
        except Exception as e:
            print(e, "222222222")
            return

        name = ('clip_{}.ts'.format(key[0]))
        print('开始下载{}'.format(name))
        with open(name, 'wb') as f:
            f.write(resp.content)
            # f.flush()
            # os.fsync(f)


    def run(self):
        print("Start!")
        start_time = time.time()
        os.chdir(self.down_path)

        fileUrlSet = ""

        ip_list = self.get_ip_list()
        proxies = self.get_random_ip(ip_list)

        # isFile = True
        # for i in os.listdir(self.down_path):
        #     if os.path.splitext(i)[1].find("m3u8") != -1:
        #         isFile = False
        #
        # if isFile:
        # torrentName = self.get_viedo_downURL()
        # self.get_uri_from_m3u8()
        # i = 1   # count
        torrentName = "SDMU_638"
        # datalist = self.cursor.execute('SELECT * FROM {}'.format(torrentName))
        datalist = self.cursor.execute('SELECT * FROM {}'.format(torrentName))
        results = []
        p = multiprocessing.Pool(4)
        for key in datalist:
            print("开始进入线程池_{}".format(key))
            # p.apply_async(self.get_viedo, args=(key, ip_list, proxies, ))
            results.append(p.apply_async(self.get_viedo, args=(key, ip_list, proxies, )))

        for res in results:
            print(res.get())

        p.close()
        p.join()
        self.cursor.close()
        self.conn.close()

        print("下载完成！总共耗时 %d s" % (time.time()-start_time))
        print("接下来进行合并……")
        os.system('copy/b %s\\*.ts %s\\%s.ts' % (self.down_path,self.final_path, self.name))
        print("合并完成，请您欣赏！")
        y = input("请检查文件完整性，并确认是否要删除碎片源文件？(y/n)")
        if y=='y':
            files = os.listdir(self.down_path)
            for filena in files:
                del_file = self.down_path + "\\" + filena
                os.remove(del_file)
            print("碎片文件已经删除完成")
        else:
            print("不删除，程序结束。")


def long_time_task_wrapper(cls_instance, i):
    return cls_instance.get_viedo(i)


if __name__=='__main__':
    url = r"https://www.kpl052.com/Watch-online/146998-1-1.html"
    code = "hello12200"
    crawler = ViedeoCrawler(url)
    crawler.run()
