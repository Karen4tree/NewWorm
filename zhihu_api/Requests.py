#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cookielib
import sys
import httplib as http_client
import requests

from Exceptions import *
from Login import Login

__author__ = 'ZombieGroup'
__package__ = 'zhihu_api'


class Requests:

    def __init__(self):
        http_client.HTTPConnection.debuglevel = 0

        try:
            Logging.info('geting cookies')
            self.requests = requests.Session()
            self.requests.cookies = cookielib.LWPCookieJar('./cookies')
            self.requests.cookies.load(ignore_discard=True)
            Login.islogin()
        except NotLogin:
            Login.login()
        except:
            Logging.error(u"找不到cookie")

        reload(sys)
        print sys.getdefaultencoding()
        self.proxies = {"http": "http://127.0.0.1:8080",
                        "https": "http://127.0.0.1:8080"}

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

requests = Requests()
