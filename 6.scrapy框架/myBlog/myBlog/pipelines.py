# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MyblogPipeline(object):
    def __init__(self):
        self.fp = None

    def open_spider(self, spider):
        self.fp = open("blog.txt", "w", encoding="utf-8")

    def process_item(self, item, spider):
        self.fp.write(f'{item["name"]}\n\t{item["content"]}\n\n')
        return item

    def close_spider(self, spider):
        self.fp.close()
