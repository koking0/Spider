# 一、需求
1. 使用任意代理 IP 进行如下操作
2. 使用requests模块进行豆瓣电影的个人用户登录操作
3. 使用requests模块访问个人用户的电影排行榜->分类排行榜->任意分类对应的子页面
4. 爬取需求3对应页面的电影详情数据
5. 爬取需求3对应页面中滚动条向下拉动2000像素后加载出所有电影详情数据，存储到本地json文件中或者相应数据库中
【备注】电影详情数据包括：海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分

# 二、分析
1. 使用任意代理 IP 进行如下操作
编写一个基本信息类，其中存储代理 IP、User-Agent 和帐密等信息：

```python
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
```

2. 使用 requests 模块进行豆瓣电影的个人用户登录操作

登录页面 URL：https://accounts.douban.com/j/mobile/login/basic

为了验证是否登录成功，可以将主页下载下来看看效果，电影主页 URL：https://movie.douban.com/chart

```python
def login(self):
	"""模拟用户登录"""
	header = self.getHeaders()
	self.session.post(url=self.loginUrl, headers=header, proxies=self.getProxy(), timeout=10, data=self.data)
	response = self.session.get(url=self.indexUrl, proxies=self.getProxy(), timeout=10, headers=header)
	self.getMiddleData(response.text)
	print("登录成功!")
```

3. 使用requests模块访问个人用户的电影排行榜->分类排行榜->任意分类对应的子页面

需求只是对任意一个分类爬取即可，我们可以通过对页面 Elements 的分析得到所有分类的 URL：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200408205230974.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

```python
def getMiddleData(self, text):
	"""用于获取中间 URL，子代可重写"""
	tree = etree.HTML(text)
	spanList = tree.xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
	for item in spanList:
		typeName, typeNumber, interval_id = re.search('type_name=(.*?)&type=(\d+)&interval_id=(.*?)&action=',
		                                              item.xpath('./a/@href')[0]).groups()
		self.spiderUrl[typeName] = f"https://movie.douban.com/j/chart/top_list?type={typeNumber}&interval_id={interval_id}&action=&start=0&limit=40"

```

4. 爬取需求3对应页面的电影详情数据

5. 爬取需求3对应页面中滚动条向下拉动2000像素后加载出所有电影详情数据，存储到本地json文件中或者相应数据库中

通过对 Network 的分析，可以发现电影数据是通过 json 传输的，并且每一次默认是获取20条数据。

滚动条向下拉动2000像素后会加载21~40条数据，可以使用 selenium 这个神奇的工具，我用了一种取巧的方法，通过设置 limit 来一次性获取40条数据。

所以我们在拼接 URL 的时候使用的是：https://movie.douban.com/j/chart/top_list?type={typeNumber}&interval_id={interval_id}&action=&start=0&limit=40

在这里要注意一个问题：==豆瓣封IP，白天一分钟可以访问40次，晚上一分钟可以访问60次，超过限制次数就会封IP。==

参考文章：[爬取豆瓣遇到的问题](https://blog.csdn.net/eye_water/article/details/78585394)

# 三、Code

## main.py

```python
from spider import Spider


class DouBanSpider(Spider):
    pass


if __name__ == '__main__':
    spider = DouBanSpider(
        email="**************",
        password="**************",
        indexUrl="https://movie.douban.com/chart",
        loginUrl="https://accounts.douban.com/j/mobile/login/basic",
    )
    session = spider.login()
    spider.getData()

```
## spider.py

```python
import json
import random
import re
import time
import pymysql
import requests
from lxml import etree
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
		tree = etree.HTML(text)
		spanList = tree.xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
		for item in spanList:
			typeName, typeNumber, interval_id = re.search('type_name=(.*?)&type=(\d+)&interval_id=(.*?)&action=',
			                                              item.xpath('./a/@href')[0]).groups()
			self.spiderUrl[typeName] = f"https://movie.douban.com/j/chart/top_list?type={typeNumber}&interval_id={interval_id}&action=&start=0&limit=40"

	def getData(self):
		"""获取目标数据"""
		for name, url in self.spiderUrl.items():
			header = self.getHeaders()
			response = self.session.get(url=url, headers=header, proxies=self.getProxy(), timeout=10).json()
			for item in response:
				try:
					item.pop("rating")
					item.pop("is_playable")
					item.pop("id")
					item.pop("vote_count")
					item.pop("is_watched")
					item["排名"], item["电影名"], item["海报Url"] = item.pop("rank"), item.pop("title"), item.pop("cover_url")
					detailUrl = item.pop("url")
					item["详情Url"] = detailUrl
					detailPage = self.session.get(url=detailUrl, headers=header, proxies=self.getProxy(), timeout=10).text
					tree = etree.HTML(detailPage)
					item["导演"] = ",".join(tree.xpath('//*[@id="info"]/span[1]/span[2]/a/text()'))
					item["片长"] = tree.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')[0]
					item["类型"], item["制片国家"], item["上映日期"] = ",".join(item.pop("types")), ",".join(
						item.pop("regions")), item.pop(
						"release_date")
					item["演员数量"], item["评分"], item["演员"] = item.pop("actor_count"), item.pop("score"), ",".join(
						item.pop("actors"))
					item["语言"] = ",".join(re.search('<span class="pl">语言:</span> (.*?)<br/>', detailPage).groups())
					print("\t", item["电影名"], "爬取完毕。")
					time.sleep(1.5)
				except Exception as e:
					print("\t", item["电影名"], "爬取出错：", e)
					item["error"] = str(e)
					break
			self.saveJson(fileName=name, obj=response)
			# self.saveDataBase(fileName=name, obj=response)
			print(f"{name}系列爬取完毕！")
			break

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

```
效果展示：

```
{
    "排名": 1,
    "电影名": "肖申克的救赎",
    "海报Url": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg",
    "详情Url": "https://movie.douban.com/subject/1292052/",
    "导演": "弗兰克·德拉邦特",
    "片长": "142分钟",
    "类型": "犯罪,剧情",
    "制片国家": "美国",
    "上映日期": "1994-09-10",
    "演员数量": 25,
    "评分": "9.7",
    "演员": "蒂姆·罗宾斯,摩根·弗里曼,鲍勃·冈顿,威廉姆·赛德勒,克兰西·布朗,吉尔·贝罗斯,马克·罗斯顿,詹姆斯·惠特摩,杰弗里·德曼,拉里·布兰登伯格,尼尔·吉恩托利,布赖恩·利比,大卫·普罗瓦尔,约瑟夫·劳格诺,祖德·塞克利拉,保罗·麦克兰尼,芮妮·布莱恩,阿方索·弗里曼,V·J·福斯特,弗兰克·梅德拉诺,马克·迈尔斯,尼尔·萨默斯,耐德·巴拉米,布赖恩·戴拉特,唐·麦克马纳斯",
    "语言": "英语"
  },
  {
    "排名": 2,
    "电影名": "霸王别姬",
    "海报Url": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2561716440.jpg",
    "详情Url": "https://movie.douban.com/subject/1291546/",
    "导演": "陈凯歌",
    "片长": "171 分钟",
    "类型": "剧情,爱情,同性",
    "制片国家": "中国大陆,中国香港",
    "上映日期": "1993-07-26",
    "演员数量": 26,
    "评分": "9.6",
    "演员": "张国荣,张丰毅,巩俐,葛优,英达,蒋雯丽,吴大维,吕齐,雷汉,尹治,马明威,费振翔,智一桐,李春,赵海龙,李丹,童弟,沈慧芬,黄斐,徐杰,黄磊,冯远征,杨立新,方征,周璞,隋永清",
    "语言": "汉语普通话"
  },
  ```
