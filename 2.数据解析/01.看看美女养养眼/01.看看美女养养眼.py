#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/1 11:56
# @File     : 01.看看美女养养眼.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import os
import re
import requests

if __name__ == '__main__':
	requestHeaders = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
	}
	if not os.path.exists("images/看看美女养养眼"):
		os.mkdir("images/看看美女养养眼")
	# 首先使用 for 循环遍历第 1 页到第 22 页，将页码与 URL 进行拼接；
	for pageIndex in range(1, 23):
		pageURL = "http://wuming3175.lofter.com/?page=%d" % pageIndex
		# 然后爬取每个页面的所有元素，并使用正则表达式过滤 img 的 src 属性同时简化其 URL；
		requestPageResponse = requests.get(url=pageURL, headers=requestHeaders).text
		regex = '<div class="block photo">.*?<img src="(.*?)?imageView.*?</div>'
		imagesURLList = re.findall(regex, requestPageResponse, re.S)
		for imageURL in imagesURLList:
			imageName = imageURL.split("/")[-1].strip("?")
			# 最后通过 URL 获取图片二进制数据并保存到本地。
			imageData = requests.get(url=imageURL, headers=requestHeaders).content
			with open("images/看看美女养养眼/%s" % imageName, "wb") as fp:
				fp.write(imageData)
		print("第 %d 页爬取完毕！" % pageIndex)
