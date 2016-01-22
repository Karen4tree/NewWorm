# -*- coding: utf-8 -*-

from BloomFliter import BloomFilter
from Queue import Queue

__author__ = 'ZombieGroup'

# Bloom Filters, only store the ids in the bloom filters
ERROR_RATE = 0.05
ITEM_NUM = 10000

userBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
questionBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
answerBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
topicBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
articleBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
collumnBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
commentBloom = BloomFilter(ERROR_RATE, ITEM_NUM)

MAXSIZE = 100
userQueue = Queue(maxsize = MAXSIZE)
questionQueue = Queue(maxsize = MAXSIZE)
answerQueue = Queue(maxsize = MAXSIZE)
topicQueue = Queue(maxsize = MAXSIZE)
articleQueue = Queue(maxsize = MAXSIZE)
collumnQueue = Queue(maxsize = MAXSIZE)
commentQueue = Queue(maxsize = MAXSIZE)


def get_hash_id(soup):
    return soup.find("button", class_ = "zg-btn zg-btn-follow zm-rich-follow-btn")['data-id']


def get_xsrf(soup):
    return soup.find("input", {"name": "_xsrf"})['value']


debug_info_flag = True
