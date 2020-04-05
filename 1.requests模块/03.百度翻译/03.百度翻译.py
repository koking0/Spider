#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 18:43
# @File     : 03.百度翻译.py
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> QQ        : 2426671397
# >>> Mail      : alex18812649207@gmail.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://blog.csdn.net/weixin_43336281
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import json

import requests

if __name__ == '__main__':
    requestUrl = "https://fanyi.baidu.com/sug"
    requestHeader = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    keyword = input("Please input content: ")
    formData = {
        "kw": keyword,
    }
    requestResponse = requests.post(url=requestUrl, headers=requestHeader, data=formData)
    result = requestResponse.json()
    with open("%s翻译结果.json" % keyword, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False)
