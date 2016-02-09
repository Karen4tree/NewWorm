# -*- coding: utf-8 -*-

from BloomFliter import BloomFilter
from gevent.queue import Queue

__author__ = 'ZombieGroup'


def get_hash_id(soup):
    return soup.find("button", class_ = "zg-btn zg-btn-follow zm-rich-follow-btn")['data-id']


def get_xsrf(soup):
    return soup.find("input", {"name": "_xsrf"})['value']


debug_info_flag = True

question_queue = Queue(maxsize = 10)
