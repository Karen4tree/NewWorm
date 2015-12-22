# -*- coding: utf-8 -*-
import Login
from BloomFliter import BloomFilter
from Requests import Requests

__author__ = 'ZombieGroup'
__package__ = 'zhihu_api'

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

requests = Requests()

debug_info_flag = True
