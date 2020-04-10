# -*- coding: utf-8 -*-
import time
import scrapy
from myBlog.items import MyblogItem


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    start_urls = ['https://alex007.blog.csdn.net/']

    pageNumber = 1
    pageUrl = 'https://alex007.blog.csdn.net/article/list/%d'

    def parse(self, response):
        print(f"正在爬取第{self.pageNumber}页，url={self.pageUrl % self.pageNumber}。")
        divList = response.xpath('//*[@id="mainBox"]/main/div[2]/div')
        for div in divList:
            item = MyblogItem()
            item["name"] = ("".join(div.xpath('.//h4/a/text()').extract())).strip("\n").strip()
            contentUrl = div.xpath('.//h4/a/@href').extract_first()
            print(f"正在爬取第文章{item['name']}，url={contentUrl}。")
            time.sleep(2)
            yield scrapy.Request(url=contentUrl, callback=self.parseContent, meta={'item': item})

        if self.pageNumber < 2:
            self.pageNumber += 1
            url = format(self.pageUrl % self.pageNumber)
            # 递归爬起数据，callback 参数为回调函数
            yield scrapy.Request(url=url, callback=self.parse)

    def parseContent(self, response):
        item = response.meta["item"]
        item["content"] = "".join(response.xpath('//*[@id="content_views"]//text()').extract())
        yield item
