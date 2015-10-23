# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std

import os, sys, time, platform, random
import re, json, cookielib
# requirements
import requests, termcolor, html2text

try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
# module
from auth import islogin
from auth import Logging

# 从auth.py中调用身份信息
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard = True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")

if not islogin():
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")

reload(sys)
sys.setdefaultencoding('utf8')


# 从Article url指向页面中抓取信息
class Article:
    url = None
    soup = None

    def __init__(self, url):
        if re.match(r'http://zhuanlan.zhihu.com/.+/\d{8}', url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a article url.")
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_article_id(self):
        return self.url[len(self.url) - 8:len(self.url)]

    def get_article_title(self):
        soup = self.soup
        # 傻逼知乎是动态加载整个页面的
