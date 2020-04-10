# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()   # 存储菜单名
    url = scrapy.Field()    # 存储菜单 url
    pass
