#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/8 8:19
# @File     : info.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import json
import random
import pymysql
import requests
from fake_useragent import UserAgent


class Spider:
	def __init__(self, email=None, password=None, indexUrl=None, loginUrl=None):
		self.session = requests.session()
		# 代理 IP 列表
		self.proxyList = [
			{"https": "60.168.80.79:18118"},
			{"https": "117.88.176.110:3000"},
			{"https": "121.31.102.146:8123"},
			{"https": "223.241.119.147:8010"},
		]
		# 登录账号基本信息
		self.data = {
			'ck': '',
			'name': email,
			'password': password,
			'remember': 'false',
			'ticket': ''
		}
		# 主页 URL
		self.indexUrl = indexUrl
		# 登录 URL
		self.loginUrl = loginUrl
		self.spiderUrl = {}

	@staticmethod
	def getHeaders():
		userAgent = {
			"User-Agent": UserAgent().random
		}
		return userAgent

	def getProxy(self):
		return random.choice(self.proxyList)

	def login(self):
		"""模拟用户登录"""
		header = self.getHeaders()
		self.session.post(url=self.loginUrl, headers=header, proxies=self.getProxy(), timeout=10, data=self.data)
		response = self.session.get(url=self.indexUrl, proxies=self.getProxy(), timeout=10, headers=header)
		self.getMiddleData(response.text)
		print("登录成功!")

	def getMiddleData(self, text):
		"""用于获取中间 URL，子代可重写"""
		pass

	def getData(self):
		"""获取目标数据，子代可重写"""
		pass

	@staticmethod
	def saveJson(fileName, obj):
		with open(f"{fileName}.json", "w", encoding="utf-8") as fp:
			json.dump(obj, fp, ensure_ascii=False)

	def saveDataBase(self, fileName, obj):
		db = pymysql.connect("localhost", "root", "20001001", "movies")
		self.createDataBaseTable(dataBase=db, tableName=fileName)
		cursor = db.cursor()
		for item in obj:
			sql = f"""INSERT INTO "{fileName}" ("排名", "电影名", "海报Url", "详情Url", "导演", "片长", "类型", "制片国家", "上映日期", "演员数量", "评分", "演员") 
value({item["排名"]},{item["电影名"]},{item["海报Url"]},{item["详情Url"]},{item["导演"]},{item["片长"]},{item["类型"]},{item["制片国家"]},{item["上映日期"]},{item["演员数量"]},{item["评分"]},{item["演员"]})"""
			try:
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print(e)
				db.rollback()
		db.close()

	@staticmethod
	def createDataBaseTable(dataBase, tableName):
		# 1.创建游标
		cursor = dataBase.cursor()
		# 2.如果数据库存在 TableName 表，则删除
		cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
		# 3.创建 TableName 表
		sql = f"""CREATE TABLE {tableName} (id INT NOT NULL AUTO_INCREMENT, 排名 INT, 电影名 VARCHAR(255), 海报Url VARCHAR(255), 详情Url VARCHAR(255), 导演 VARCHAR(255), 片长 VARCHAR(255), 类型 VARCHAR(255), 制片国家 VARCHAR(255), 上映日期 VARCHAR(255), 演员数量 INT, 评分 FLOAT, 演员 VARCHAR(255), PRIMARY KEY(id))"""
		cursor.execute(sql)
		cursor.close()
		print(f"{tableName} table 创建完毕！")
