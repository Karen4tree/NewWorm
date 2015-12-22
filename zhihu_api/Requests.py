#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'ZombieGroup'
__package__='zhihu_api'

import cookielib
import sys
from auth import islogin
from Logging import Logging
import httplib as http_client
import requests
from Exceptions import *


class Requests:
    def __init__(self):
        http_client.HTTPConnection.debuglevel = 0

        print 'get cookies'
        self.requests = requests.Session()
        self.requests.cookies = cookielib.LWPCookieJar('./cookies')
        try:
            self.requests.cookies.load(ignore_discard = True)
            islogin()
        except NotLogin:
            Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
        except:
            Logging.error(u"找不到cookie")

        reload(sys)
        print sys.getdefaultencoding()
        self.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

    def get(self, url, **kwargs):
        try:
            return self.requests.get(url, **kwargs)
        except:
            self.get(url, **kwargs)

    def post(self, url, data):
        try:
            return self.requests.post(url, data)
        except:
            self.post(url, data)
