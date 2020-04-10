# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class BeautyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """用于请求方法"""
        print(f'开始下载{item["image_urls"]}')
        yield scrapy.Request(url=item["image_urls"])

    def file_path(self, request, response=None, info=None):
        """指定文件存储路径"""
        return request.url.split('/')[-1]

    def item_completed(self, results, item, info):
        return item
