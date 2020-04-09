#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/7 23:15
# @File     : main.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import re
import time
from lxml import etree
from spider import Spider


class DouBanSpider(Spider):
    def getMiddleData(self, text):
        """用于获取中间 URL，子代可重写"""
        tree = etree.HTML(text)
        spanList = tree.xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
        for item in spanList:
            typeName, typeNumber, interval_id = re.search('type_name=(.*?)&type=(\d+)&interval_id=(.*?)&action=',
                                                          item.xpath('./a/@href')[0]).groups()
            self.spiderUrl[
                typeName] = f"https://movie.douban.com/j/chart/top_list?type={typeNumber}&interval_id={interval_id}&action=&start=0&limit=40"


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


if __name__ == '__main__':
    spider = DouBanSpider(
        email="2426671397@qq.com",
        password="Alex123",
        indexUrl="https://movie.douban.com/chart",
        loginUrl="https://accounts.douban.com/j/mobile/login/basic",
    )
    session = spider.login()
    spider.getData()
