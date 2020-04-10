# -*- coding: utf-8 -*-
import scrapy
from beauty.items import BeautyItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    start_urls = ['http://wuming3175.lofter.com//']

    pageNumber = 1
    pageUrl = "http://wuming3175.lofter.com/?page=%d"

    def parse(self, response):
        divList = response.xpath('/html/body/div[3]/div')
        for div in divList:
            item = BeautyItem()
            imageSrc = div.xpath('.//div[2]/div[1]/div[1]/a/img/@src').extract_first()
            if imageSrc:
                item["image_urls"] = imageSrc.split("?")[0]
                yield item

        if self.pageNumber < 22:
            self.pageNumber += 1
            url = format(self.pageUrl % self.pageNumber)
            yield scrapy.Request(url=url, callback=self.parse)
