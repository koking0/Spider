#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 20:31
# @File     : 04.豆瓣电影.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import json

import requests

if __name__ == '__main__':
	requestURL = "https://movie.douban.com/j/chart/top_list"
	requestHeader = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
	}
	queryStringParameters = {
		"type": "25",
		"interval_id": "100:90",
		"action": "",
		"start": "0",
		"limit": "100",
	}
	requestResponse = requests.get(url=requestURL, headers=requestHeader, params=queryStringParameters)
	data = requestResponse.json()
	with open("豆瓣电影.json", "w", encoding="utf-8") as fp:
		json.dump(data, fp, ensure_ascii=False)
