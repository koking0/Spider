#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/7 17:31
# @File     : 4.第一个绑定回调.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import asyncio
import requests


async def request():
    url = "https://www.baidu.com"
    status = requests.get(url=url).status_code
    return status


def callback(tempTask):
    print("Status:", tempTask.result())


if __name__ == '__main__':
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    task.add_done_callback(callback)
    print("Task:", task)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print("Task:", task)
