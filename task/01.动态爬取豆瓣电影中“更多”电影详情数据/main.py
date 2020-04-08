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
from spider import Spider


class DouBanSpider(Spider):
    pass


if __name__ == '__main__':
    spider = DouBanSpider(
        email="2426671397@qq.com",
        password="Alex123",
        indexUrl="https://movie.douban.com/chart",
        loginUrl="https://accounts.douban.com/j/mobile/login/basic",
    )
    session = spider.login()
    spider.getData()
