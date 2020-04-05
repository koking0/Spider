#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 23:08
# @File     : 06.国家药监局生产许可证.py
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
	requestIdURL = "http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList"
	requestHeader = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
	}
	for index in range(1, 101):
		idFormData = {
			"on": "true",
			"page": 1,
			"pageSize": "15",
			"productName": "",
			"conditionType": "1",
			"applyname": "",
			"applysn": "",
		}
		for item in requests.post(url=requestIdURL, headers=requestHeader, data=idFormData).json()["list"]:
			requestContentURL = "http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById"
			contentFormData = {
				"id": item["ID"],
			}
			requestResponse = requests.post(url=requestContentURL, headers=requestHeader, data=contentFormData).json()
			data[requestResponse["epsName"]] = requestResponse
	with open("化妆品生产许可证.json", "w", encoding="utf-8") as fp:
		json.dump(data, fp, ensure_ascii=False)
