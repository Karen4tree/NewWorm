# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std


from ScrollLoader import ScrollLoader
import re
import json
import cookielib
import sys
import logging
import logging.config

import termcolor
import html2text
from bs4 import BeautifulSoup

from auth import islogin
from auth import Logging
from BloomFliter import BloomFilter


import httplib as http_client
from Requests import requests

# 从Comment url指向页面中抓取信息


class Comment:

    def __init__(self, url, question_id=None, answer_id=None, content=None, vote_num=0):
        self.question_id = question_id
        self.answer_id = answer_id
        self.content = content
        self.vote_num = vote_num
# TODO: 大坑要填
