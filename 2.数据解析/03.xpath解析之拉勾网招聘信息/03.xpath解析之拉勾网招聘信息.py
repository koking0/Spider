#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/7 9:40
# @File     : 03.xpath解析之拉勾网招聘信息.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import json
import time
import random

import requests
from lxml import etree

if __name__ == '__main__':
	headerList = [
		{"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
		{"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
		{
			"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
	]
	allData = {}
	for index in range(1, 31):
		print("正 在 爬 取 第 %d 页......" % index)
		firstUrl = "https://www.lagou.com/zhaopin/Python/%d/" % index
		pageHtml = requests.get(url=firstUrl, headers=random.choice(headerList), timeout=500).text
		firstTree = etree.HTML(pageHtml)
		liList = firstTree.xpath('//*[@id="s_position_list"]/ul/li')
		for li in liList:
			secondUrl = li.xpath('.//div[1]/div[1]/div[1]/a/@href')[0]
			detailHtml = requests.get(url=secondUrl, headers=random.choice(headerList), timeout=500).text
			secondTree = etree.HTML(detailHtml)
			liData = {
				"positionName": li.xpath('./@data-positionname')[0],
				"company": li.xpath('./@data-company')[0],
				"salary": li.xpath('./@data-salary')[0],
				"address": li.xpath('.//div[1]/div[1]/div[1]/a/span/em/text()'),
				"experience": li.xpath('.//div[1]/div[1]/div[2]/div/text()'),
				"companyProfile": li.xpath('.//div[1]/div[2]/div[2]/text()'),
				"detailUrl": secondUrl,
				"describe": secondTree.xpath('//*[@id="job_detail"]/dd[@class="job_bt"]/div[@class="job-detail"]//text()')
			}
			allData["%s-%s" % (liData["company"], liData["positionName"])] = liData
			time.sleep(1)
	with open("拉勾网Python职位信息.json", "w", encoding="utf-8") as fp:
		json.dump(obj=allData, fp=fp, ensure_ascii=False)
