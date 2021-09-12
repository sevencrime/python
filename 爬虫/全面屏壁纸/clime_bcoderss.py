#!/usr/bin/env python
# -*- coding: utf-8 -*-


## 全面屏壁纸 网站

import os
import asyncio

import aiohttp
import aiofiles
from bs4 import BeautifulSoup  
from lxml import html
from PIL import Image


template = 'https://m.bcoderss.com/tag/美女/page/{page}/'
dir_file_path = "D:/自媒体素材/壁纸/壁纸_全面屏壁纸网站/"

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}



async def save(session, path, dir_path):
	print("开始请求图片地址 : {}".format(path))
	async with session.get(path) as response:
		if response.status == 200:
			img = await response.read()
			async with aiofiles.open(dir_path, mode='wb') as f:
				await f.write(img)
				await f.close()
		else:
			print("图片请求非200, {}".format(response))


async def get(session, page):
	url = template.format(page=page)
	print("开始请求网页 : {}".format(url))
	resp = await session.get(url)
	if resp.status == 200:
		source_text = await resp.text(encoding='utf-8')
		soup = BeautifulSoup(source_text, "lxml")
		img_tag_list = soup.find_all("img", class_="attachment-thumbnail size-thumbnail wp-post-image")
		for img in img_tag_list:
			img_src = img.get("src")
			img_path = img_src.rsplit("-", 1)[0] + ".jpg"
			dir_path = os.path.join(dir_file_path, img_path.rsplit("/", 1)[1])
			await save(session, img_path, dir_path)
	else:
		print("请求非200, {}".format(resp))



async def main():
	async with aiohttp.ClientSession(headers=headers) as session:
		for page in range(100):
			await get(session, page)


def get_image_size():
	for root, dirs, files in os.walk(dir_file_path):
		count = 1
		#当前文件夹所有文件
		for i in files:
			#判断是否以.jpg结尾
			if i.endswith('.jpg'):
				#如果是就改变图片像素为28 28
				im=Image.open(dir_file_path + i)
				print(im.size)

		print("文件夹图片数量为 : {}".format(files.__len__()))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
get_image_size()