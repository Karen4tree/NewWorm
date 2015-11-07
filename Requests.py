# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Stdimport os, sys, time, platform, random

import re
import json
import cookielib
import sys
import logging
# requirements
import requests
import termcolor
import html2text

from bs4 import BeautifulSoup

# module
from auth import islogin
from auth import Logging


# debug requests
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.


class Requests:

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        # TODO: 打印到文本

        print 'get cookies'
        self.requests = requests.Session()
        self.requests.cookies = cookielib.LWPCookieJar('cookies')
        try:
            self.requests.cookies.load(ignore_discard=True)
        except:
            Logging.error(u"你还没有登录知乎哦 ...")
            Logging.info(u"执行 `python auth.py` 即可以完成登录。")
            raise Exception("无权限(403)")

        if not islogin():
            Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
            raise Exception("无权限(403)")

        reload(sys)
        sys.setdefaultencoding('utf8')
        print sys.getdefaultencoding()
        self.proxies = {"http": "http://127.0.0.1:8080",
                        "https": "http://127.0.0.1:8080", }

    def get(self, url):
        try:
            return self.requests.get(url)
        except:
            self.get(url)

    def post(self, url, data):
        try:
            return self.requests.post(url, data)
        except:
            self.post(url, data)


def get_hash_id(soup):
    return soup.find("button", class_="zg-btn zg-btn-follow zm-rich-follow-btn")['data-id']


def get_xsrf(soup):
    return soup.find("input", {"name": "_xsrf"})['value']


requests = Requests()
