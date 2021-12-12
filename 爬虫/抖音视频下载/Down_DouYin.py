# -*- coding: utf-8 -*-
# 下载抖音无水印视频

import requests
import json
import re
import os



class Douyin(object):
    """docstring for douyin"""
    def __init__(self, path):
        super(Douyin, self).__init__()
        self.path = path                                        # 抖音分享的链接
        self.file_name = re.findall(r':/(.*?) http', path)[0].replace("%", "#").replace(" ", "")       # 视频的名称
        print(self.file_name)
        self.save_path = "/Users/edy/Documents/movie/douyin/{}.mp4".format(self.file_name)      # 文件保存的路径
        self.raw_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"   # 抖音接口, 用于获取无水印地址
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36'}



    def searchDicKV(self, dic, keyword):
        if isinstance(dic, dict):
            for x in range(len(dic)):
                temp_key = list(dic.keys())[x]
                temp_value = dic[temp_key]
                if temp_key == keyword:
                    return_value = temp_value
                    return return_value
                return_value = self.searchDicKV(temp_value, keyword)
                if return_value != None:
                    return return_value
        elif isinstance(dic, list):
            for d in dic:
                return self.searchDicKV(d, keyword)


    def get_playAddr(self):
        ''' 获取无水印视频地址 '''
        url = re.search("http.+/", self.path).group()
        response = requests.get(url, headers=self.headers)

        # 分割url, 找出item_id
        item_id = response.url.rsplit("/", 2)[1]

        params = {"item_ids" : item_id}
        raw_rsp = requests.get(self.raw_url, params=params, headers=self.headers)

        if raw_rsp.status_code == 200:
            playAddr = self.searchDicKV(raw_rsp.json(), "play_addr")
            ori_Addr = self.searchDicKV(playAddr, "url_list")

            return ori_Addr[0].replace("playwm", "play")


    # 下载视频
    def do_load_media(self, url):
        try:
            pre_content_length = 0
            # 循环接收视频数据
            while True:
                # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
                if os.path.exists(self.save_path):
                    self.headers['Range'] = 'bytes=%d-' % os.path.getsize(self.save_path)
                res = requests.get(url, stream=True, headers=self.headers)

                content_length = int(res.headers['content-length'])
                # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
                if content_length < pre_content_length or (
                        os.path.exists(self.save_path) and os.path.getsize(self.save_path) == content_length) or content_length == 0:
                    break
                pre_content_length = content_length

                # 写入收到的视频数据
                with open(self.save_path, 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    print('下载成功：文件大小 : %s  总下载大小:%s' % (self.StrOfSize(os.path.getsize(self.save_path)), self.StrOfSize(content_length)))
        except Exception as e:
            print(e)


    # 文件大小转化
    def StrOfSize(self, size):
        '''
        递归实现，精确为最大单位值 + 小数点后三位
        '''

        def strofsize(integer, remainder, level):
            if integer >= 1024:
                remainder = integer % 1024
                integer //= 1024
                level += 1
                return strofsize(integer, remainder, level)
            else:
                return integer, remainder, level

        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        integer, remainder, level = strofsize(size, 0, 0)
        if level + 1 > len(units):
            level = -1
        return ('{}.{:>03d} {}'.format(integer, remainder, units[level]))


    def main(self):
        self.do_load_media(self.get_playAddr())


if __name__ == "__main__":
    path = ''' 
    8.46 ChB:/ %木星计划 %一首歌走过悲伤 我明白你不明白我明白…  https://v.douyin.com/Rcmj43Q/ 复製此链接，咑开Dou音搜索，矗接观看视频！

    '''

    Douyin(path).main()

