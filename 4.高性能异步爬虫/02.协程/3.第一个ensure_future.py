#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/7 17:26
# @File     : 3.第一个ensure_future.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import asyncio


async def execute(x):
    print("Number = ", x)


if __name__ == '__main__':
    coroutine = execute(1)
    print("Coroutine:", coroutine)
    print("After calling execute.")

    task = asyncio.ensure_future(coroutine)
    print("Task:", task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print("Task:", task)
    print("After calling loop.")
