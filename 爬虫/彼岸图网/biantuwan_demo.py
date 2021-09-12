#!/usr/bin/env python
# -*- coding: utf-8 -*-


## 全面屏壁纸 网站

import os
import asyncio
import time

import aiohttp
import aiofiles
from bs4 import BeautifulSoup  
from lxml import html
from PIL import Image
from fake_useragent import UserAgent



path_index = 'https://pic.netbian.com/'
path_mn = 'https://pic.netbian.com/shoujibizhi/'
dir_file_path = "D:/自媒体素材/壁纸/彼岸图网/"

path_img = "https://pic.netbian.com"

async def save(session, path, dir_path):
	print("开始请求图片地址 : {}".format(path))
	try:
		async with session.get(path, headers=get_random_ua()) as response:
			if response.status == 200:
				img = await response.read()
				async with aiofiles.open(dir_path, mode='wb') as f:
					await f.write(img)
					await f.close()
			else:
				print("图片请求非200, {}".format(response))
	except Exception as e:
		print("请求图片时错误")
		print(e)
		time.sleep(10)


async def get_details(session, path, name):
	print("详情页")
	response = await session.get(path, headers=get_random_ua())
	if response.status == 200:
		source_text = await response.text()
		soup = BeautifulSoup(source_text, "lxml")
		img_tag_list = soup.find_all("img", alt=name)
		for img in img_tag_list:
			img_detail_url = path_img + img.get("src")
			dir_path_folder = dir_file_path + ''.join(e for e in name if e.isalnum()) + ".jpg"
			await save(session, img_detail_url, dir_path_folder)

	else:
		print("图片请求非200, {}".format(response))



async def get(session, page):
	url = path_mn + page
	print("开始请求网页 : {}".format(url))
	resp = await session.get(url, headers=get_random_ua())
	print(resp.status)
	if resp.status == 200:
		source_text = await resp.text()
		soup = BeautifulSoup(source_text, "lxml")
		ul_tag = soup.select("ul.clearfix > li > a")
		for tag in ul_tag:
			img_details = tag.get("href")
			img_name = tag.select("img")[0].get("alt")

			await get_details(session, path_index + img_details, img_name)


	else:
		print("请求非200, {}".format(resp))

# 随机生成User-Agent
def get_random_ua():
	ua = UserAgent()        # 创建User-Agent对象
	useragent = ua.random
	headers = {"user-agent" : useragent}
	return headers


async def main():
	headers = get_random_ua()
	async with aiohttp.ClientSession(headers=headers) as session:
		for page in range(100):
			if page == 0:
				u_path = ""
			else:
				u_path = "index_{}.html".format(page + 1)
			await get(session, u_path)



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
