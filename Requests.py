# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Stdimport os, sys, time, platform, random
import re
import json
import cookielib
import sys
import logging
import logging.config
# requirements
import requests
import termcolor
import html2text
import gevent
from gevent import monkey
from gevent.queue import Queue, Empty
from bs4 import BeautifulSoup
# module
from auth import islogin
from auth import Logging
from BloomFliter import BloomFilter

# debug requests
try:
    import http.client
except ImportError:
    # Python 2
    import httplib as http_client

# Global Var
ERROR_RATE = 0.005
ELEMENT_NUM = 99999999
QUEUE_SIZE = 20

question_queue = Queue(maxsize=QUEUE_SIZE)
user_queue = Queue(maxsize=QUEUE_SIZE)
topic_queue = Queue(maxsize=QUEUE_SIZE)
article_queue = Queue(maxsize=QUEUE_SIZE)
answer_queue = Queue(maxsize=QUEUE_SIZE)
column_queue = Queue(maxsize=QUEUE_SIZE)

question_bloom = BloomFilter(ERROR_RATE, ELEMENT_NUM)
user_bloom = BloomFilter(ERROR_RATE, ELEMENT_NUM)
topic_bloom = BloomFilter(ERROR_RATE, ELEMENT_NUM)
article_bloom = BloomFilter(ERROR_RATE, ELEMENT_NUM)
answer_bloom = BloomFilter(ERROR_RATE, ELEMENT_NUM)
column_bloom = BloomFilter(ERROR_RATE, ELEMENT_NUM)


class Requests:

    def __init__(self):
        http_client.HTTPConnection.debuglevel = 0

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


def get_hash_id(soup):
    return soup.find("button", class_="zg-btn zg-btn-follow zm-rich-follow-btn")['data-id']


def get_xsrf(soup):
    return soup.find("input", {"name": "_xsrf"})['value']


requests = Requests()
