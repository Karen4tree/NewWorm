# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Stdimport os, sys, time, platform, random

import re, json, cookielib,sys
# requirements
import requests, termcolor, html2text

try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
# module
from auth import islogin
from auth import Logging
from Questions import Questions
from Answers import Answers
from Article import Article

print 'get cookies'
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

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}