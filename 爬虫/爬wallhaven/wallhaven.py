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


def retry(func):
	async def inner(*args, **kwargs):
		try:
			await func(*args, **kwargs)
		except Exception as e:
			time.sleep(5)
			max_retry = 3
			number = 0
			while number < max_retry:
				number += 1
				print(args)
				print("尝试第:{}次".format(number))
				try:
					await func(*args, **kwargs)
					break
				except Exception as e:
					print("重试还是错误了")

	return inner



class Wallhaven(object):
	"""docstring for Wallhaven"""
	def __init__(self):
		super(Wallhaven, self).__init__()
		self.path = "https://wallhaven.cc/toplist"
		self.save_file_path = "D:/自媒体素材/壁纸/wallhaven/"

		self.re_num = 0

	# 随机生成User-Agent
	def get_random_ua(self):
		ua = UserAgent()		# 创建User-Agent对象
		useragent = ua.random
		headers = {"user-agent" : useragent}
		return headers


	async def save(self, session, path, dir_path):
		print("开始请求图片地址 : {}".format(path))
		try:
			async with session.get(path) as response:
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
			time.sleep(3)


	# @retry
	async def get_details(self, session, path):
		response = await session.get(path)
		try:
			assert response.status == 200
		except Exception as e:
			print("图片 : {}  请求非200, {}, 错误信息: {}".format(path, response, e))
			if response.status == 429:
				await asyncio.sleep(60)
				await self.get_details(session, path)

		source_text = await response.text(encoding='utf-8')
		soup = BeautifulSoup(source_text, "lxml")
		img_tag_list = soup.select("img#wallpaper")
		for img in img_tag_list:
			img_src = img.get("src")
			if not img_src:
				img_src = img.get("data-cfsrc")
			img_alt = img.get("alt")
			img_width = img.get("data-wallpaper-width")
			img_height = img.get("data-wallpaper-height")
			if img_src:
				save_path = self.save_file_path + img_src.split("/")[-1]
			else:
				save_path = self.save_file_path + img_alt.replace(" ", "")[-10:] + ".jpg"


			if int(img_height) > int(img_width) :
				print("大小大小大小")
				await self.save(session, img_src, save_path)


	async def get(self, session, page):
		url = self.path + page
		print("开始请求网页 : {}".format(url))
		resp = await session.get(url)
		if resp.status == 200:
			source_text = await resp.text(encoding='utf-8')
			soup = BeautifulSoup(source_text, "lxml")
			tag_list = soup.select("a.preview")
			for tag in tag_list:
				a_href = tag.get("href")
				if a_href:
					await self.get_details(session, a_href)

		else:
			print("请求非200, {}".format(resp))


	async def main(self):
		headers = {
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" , 
		"accept-encoding": "gzip, deflate, br" , 
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
		}
		cookies = {
		    "__cfduid":"d9a8f9c7060b6b0f90c4746864e98abe61620402872",
		    "_pk_id.1.01b8":"baf7dcc64ea51a7b.1620402882.",
		    "cf_clearance":"9b37263eb2b87c4e7da1c7aa5523b03d50b3a554-1620976961-0-250",
		    "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d":"eyJpdiI6IkNDZ0E2VVwvR1hjbm5ZV3J3YUFIenp3PT0iLCJ2YWx1ZSI6IllHd1JtVkVLcnNMbDQ2UEpGZFdSQmFiUVh2RENvajZWQjJcL2R3T1AxY1dySWIyUDg4Z05iRmlcL3dYTlg5b0djSFNyVFNtU0NrRXBydnBBRzJ6WlBTc250SVcxT1wvbzVRdytkbWxmXC9IZGp4Sis2QTlldm4rKzZsRmcrXC9TVndEaFZTUm9iaTNLMzN2NzZnVlRGYjJyemRTUHBERnBlWjJBTHMwTjRWTkZIWGd4MzU0dzBrVlhuM3RhVm1oQXlsb3ZNIiwibWFjIjoiYTIyZmMxNzA4MWRkMjE2MTcxZDk0YjRiNDA1ODYzYWU2ZDBjMmFiZWQ2ZGQ5MTNmODYwNmEwM2U5MjY0MTM5MyJ9",
		    "_pk_ref.1.01b8":"%5B%22%22%2C%22%22%2C1620984222%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D",
		    "_pk_ses.1.01b8":"1",
		    "XSRF-TOKEN":"eyJpdiI6ImRKY0JEaHRRN0UwN0p1WjZSMnRrSmc9PSIsInZhbHVlIjoidkVpaGtLa2M5VHQ3RktyckVxcnBCWCtcLzZUOGxITHFIY3ZaUms4SjNnem1LSFpMeXdMUW1XSDRkc1pWNVk3TnQiLCJtYWMiOiJlNjZmYzhkOGY3YWM4YjNhNzIyNDMwYTk5MGJiOGU0ZTBjOWMwYjZjYzE4NTk5YzRkNTQ0ZDQ0NzM1OTM3MDRkIn0%3D",
		    "wallhaven_session":"eyJpdiI6Ilk5eFc5ZGUrYXU1b2VmWlFyVUhPZnc9PSIsInZhbHVlIjoiSHhjcHNnMWJcL0FrNG9LOHd3Z052eSt0c3haN1k1aktla0lNWTN0M1MwUGcyZVFESlVBeW81VXR2QXpsQTB0VkUiLCJtYWMiOiIwYjNiYThkOTQ1OTYxZjJjOTU4YTAzMTYwMjU0Y2ZlNWEwNGQ4OWM0NTA4ZGNlOTVkMThiNDk4MWQxODQ4Y2M0In0%3D"
		}

		async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
			for page in range(100):
				if page == 0:
					u_path = ""
				else:
					u_path = "?page={}".format(page + 1)
				await self.get(session, u_path)



if __name__ == "__main__":
	obj = Wallhaven()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(obj.main())
