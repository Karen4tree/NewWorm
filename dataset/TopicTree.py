#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from zhihu_api.Requests import requests
from Queue import Queue

class TopicTree:
    def __init__(self):
        self.depth = 0
        self.starturl = ''
        self.soup = None

    def parser(self):
        try:
            r = requests.get(self.starturl)
            self.soup = BeautifulSoup(r.content)
        except:
            self.parser()

    def get_top_level(self):
        self.depth += 1
        return

    def get_next_level(self):
        
    def draw(self):

