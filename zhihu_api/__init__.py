# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Stdimport os, sys, time, platform, random

import re
import json
import cookielib
import sys
import logging
import logging.config

import requests
import termcolor
import html2text
from bs4 import BeautifulSoup

from auth import islogin
from auth import Logging

from BloomFliter import BloomFilter
from Requests import Requests
from User import User
from Answer import Answer
from Article import Article
from BloomFliter import BloomFilter
from Collection import Collection
from Column import Column
from Comment import Comment
from Question import Question
from Requests import Requests
from Topic import Topic
# debug requests
# You must initialize logging, otherwise you'll not see debug output.
try:
    import http.client
except ImportError:
    # Python 2
    import httplib as http_client


requests = Requests()

# Bloom Fliters
ERROR_RATE = 0.05
ITEM_NUM = 10000

userBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
questionBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
answerBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
topicBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
articleBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
collumnBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
commentBloom = BloomFilter(ERROR_RATE, ITEM_NUM)


def get_hash_id(soup):
    return soup.find("button", class_="zg-btn zg-btn-follow zm-rich-follow-btn")['data-id']


def get_xsrf(soup):
    return soup.find("input", {"name": "_xsrf"})['value']
