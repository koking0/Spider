# -*- coding: utf-8 -*-
import scrapy
from firstScrapy.items import FirstscrapyItem


class BaiduSpider(scrapy.Spider):
    # 爬虫应用名称
    name = 'baiDu'
    # 允许爬取的域名，如果不是该域名下的 url 则不会爬取
    allowed_domains = ['www.baidu.com']
    # 起始爬取 url
    start_urls = ['http://www.baidu.com/']

    # 将爬取起始 url 的结果作为 response 参数传入该函数，函数的返回值必须是可迭代对象或 null
    def parse(self, response):
        # xpath 为 response 的方法，可以直接写 xpath 表达式
        aList = response.xpath('//*[@id="u1"]/a')
        for data in aList:
            # 将解析到的数据封装到 items 对象中
            item = FirstscrapyItem()
            item["name"] = data.xpath('.//text()')[0].extract()
            item["url"] = data.xpath('./@href')[0].extract()
            yield item
