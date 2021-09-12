# -*- coding: utf-8 -*-


# 引入必要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re
from bs4 import BeautifulSoup  
from lxml import html
import aiohttp
import aiofiles
import asyncio
from fake_useragent import UserAgent



def get_driver():
    try:
        return webdriver.PhantomJS()
    except Exception:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
        return webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver', chrome_options=chrome_options)


# 得到登录的cookie
def login_cookie():

    try:
        f = open('D:/projectdemo/python/爬虫/爬知乎图片_selenium/zhihu.txt')
        cookies = f.read()
        return True
    except Exception as e:
        raise e

    driver = get_driver()    
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    time.sleep(20)
    cookies = driver.get_cookies()
    jsonCookies = json.dumps(cookies)
    #下面的文件位置需要自己改
    with open('D:/projectdemo/python/爬虫/爬知乎图片_selenium/zhihu.txt','w') as f:
        f.write(jsonCookies)
    driver.quit() 

# 再次登录
def login():    
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    time.sleep(5)
    #下面的文件位置需要自己改，与上面的改动一致
    f = open('D:/projectdemo/python/爬虫/爬知乎图片_selenium/zhihu.txt')
    cookies = f.read()
    jsonCookies = json.loads(cookies)
    for co in jsonCookies:
        driver.add_cookie(co)
    driver.refresh()
    time.sleep(5)

# 爬取某问题下的所有答案
def get_answers(question_url):
    img_list = []
    driver.get(question_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    img_tag = soup.select("figure img")
    for img in img_tag:
        img_original_url = img.get("data-original")
        img_list.append(img_original_url)

    print(img_list.__len__())
    return img_list


def get_random_ua():
    ua = UserAgent()        # 创建User-Agent对象
    useragent = ua.random
    headers = {"user-agent" : useragent}
    return headers

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


async def main(img_list):
    dir_path_folder = 'D:/自媒体素材/壁纸/知乎/'
    headers = get_random_ua()
    img_list = list(img_list)
    async with aiohttp.ClientSession(headers=headers) as session:
        for url in img_list:
            if url:
                dir_path = dir_path_folder + str(img_list.index(url)) + ".jpg"
                await save(session, url, dir_path)

if __name__ == "__main__":
    # 设置你想要搜索的问题
    question_url = 'https://www.zhihu.com/question/453323523/answer/1821676921'
    login_cookie()
    driver = get_driver() 
    login()
    img_list = get_answers(question_url)
    driver.quit()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(set(img_list)))