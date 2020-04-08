#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/4/7 16:39
# @File     : 1.第一个协程.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
# 首先引入 asyncio 包，这样才能使用 async 和 await
import asyncio


# 使用 async 定义一个 execute 方法，接收一个参数并打印
async def execute(x):
	print("Number = ", x)

# 此时调用 execute 函数并不会执行，而是返回一个协程对象
coroutine = execute(1)
print("coroutine:", coroutine)
print("After calling execute.")

# 然后使用 get_event_loop 方法创建一个事件循环 loop
loop = asyncio.get_event_loop()
# 之后调用 loop 对象的 run_until_complete 方法将协程对象注册到事件循环 loop 中并启动，函数才能运行
loop.run_until_complete(coroutine)
print("After calling loop.")
