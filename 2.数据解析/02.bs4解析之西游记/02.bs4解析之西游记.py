#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/1 17:50
# @File     : 02.bs4解析之西游记.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
	requestHeaders = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36",
	}
	requestPageURL = "http://www.eywedu.com/Xiyou/01/index.htm"
	responsePage = requests.get(url=requestPageURL, headers=requestHeaders).content.decode("gb2312", "ignore")
	pageSoup = BeautifulSoup(responsePage, "lxml")
	titles = pageSoup.select(".content > a")
	for title in titles:
		titleName = title.string
		requestContentURL = "http://www.eywedu.com/Xiyou/01/" + title["href"]
		responseContent = requests.get(url=requestContentURL, headers=requestHeaders).content.decode("gb2312", "ignore")
		contentSoup = BeautifulSoup(responseContent, "lxml")
		soupContent = contentSoup.select('td[background="Untitled-0104.jpg"] td[width="100%"]')[0]
		content = soupContent.text
		with open("./西游记.txt", "a", encoding="utf-8") as fp:
			fp.write(titleName + "\n" + content + "\n\n")
		print(titleName, "over！")
