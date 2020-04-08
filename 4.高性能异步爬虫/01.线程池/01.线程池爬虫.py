#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/7 12:45
# @File     : 01.线程池爬虫.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import re
import random
import requests
from lxml import etree
from multiprocessing.dummy import Pool


# 使用线程池进行视频数据保存
def save(data):
	fileName = str(random.randint(1, 10000)) + '.mp4'
	print(fileName + '开始存储')
	with open(fileName, 'wb') as fp:
		fp.write(data)
		print(fileName + '已存储')


if __name__ == '__main__':
	# 实例化线程池对象
	pool = Pool()
	url = 'http://www.pearvideo.com/category_1'
	headerList = [
		{"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
		{"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
		{
			"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
	]
	# 获取首页页面数据
	page_text = requests.get(url=url, headers=random.choice(headerList)).text
	# 对获取的首页页面数据中的相关视频详情链接进行解析
	tree = etree.HTML(page_text)
	li_list = tree.xpath('//*[@id="listvideoListUl"]/li')
	detail_urls = []  # 存储二级页面的url
	for li in li_list:
		detail_url = 'http://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
		title = li.xpath('.//div[@class="vervideo-title"]/text()')[0]
		detail_urls.append(detail_url)
	videoUrl = []  # 存储视频的url
	for url in detail_urls:
		page_text = requests.get(url=url, headers=random.choice(headerList)).text
		try:
			vedio_url = re.findall('srcUrl="(.*?)"', page_text, re.S)[0]
			videoUrl.append(vedio_url)
		except Exception as e:
			print(e)
			continue
	# 使用线程池进行视频数据下载
	video_data_list = pool.map(lambda link: requests.get(url=link, headers=random.choice(headerList)).content, videoUrl)
	pool.map(lambda data: save(data), video_data_list)
	pool.close()
	pool.join()
