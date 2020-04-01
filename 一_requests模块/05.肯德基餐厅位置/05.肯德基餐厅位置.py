#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 22:12
# @File     : 05.肯德基餐厅位置.py
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
	data = {}
	requestURL = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
	requestHeader = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
	}
	formData = {
		"cname": "临沂",
		"pid": "",
		"pageIndex": 1,
		"pageSize": 23,
	}
	requestResponse = requests.post(url=requestURL, data=formData, headers=requestHeader).json()
	with open("肯德基餐厅位置.json", "a", encoding="utf-8") as fp:
		json.dump(requestResponse, fp, ensure_ascii=False)
