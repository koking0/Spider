#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 18:22
# @File     : 02.网页采集器.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import requests

if __name__ == '__main__':
	keyword = input("Please input keyword: ")
	requestUrl = "https://www.baidu.com/s"
	requestHeaders = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
	}
	params = {
		"wd": keyword,
	}
	requestResponse = requests.get(url=requestUrl, params=params, headers=requestHeaders)
	pageText = requestResponse.text
	with open("%s采集结果.html" % keyword, "w", encoding="utf-8") as fp:
		fp.write(pageText)
