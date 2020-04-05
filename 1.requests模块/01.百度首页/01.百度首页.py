#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 18:11
# @File     : 1.搜狗首页.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import requests

if __name__ == "__main__":
	requestUrl = "https://www.baidu.com/"
	requestResponse = requests.get(url=requestUrl)
	pageText = requestResponse.text
	with open("./百度首页.html", "w", encoding="utf-8") as fp:
		fp.write(pageText)
