# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class FirstscrapyPipeline(object):
    def __init__(self):
        self.fp = None

    def open_spider(self, spider):
        """开启爬虫时执行一次"""
        self.fp = open("data.txt", "w")

    def process_item(self, item, spider):
        self.fp.write(f'{item["name"]}:{item["url"]}\n')
        return item

    def close_spider(self, spider):
        """结束爬虫时执行一次"""
        self.fp.close()


class DataBasePipeline(object):
    def __init__(self):
        self.connect, self.cursor = None, None

    def open_spider(self, spider):
        self.connect = pymysql.Connect(host="127.0.0.1", port=3306, user="root", password="20001001", db="test", charset="utf8")

    def process_item(self, item, spider):
        self.cursor = self.connect.cursor()
        try:
            sql = 'INSERT INTO scrapy1 VALUES ("%s", "%s");' % (item["name"], item["url"])
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()
        return item

    def close_spider(self, spider):
        self.connect.close()
        self.cursor.close()
