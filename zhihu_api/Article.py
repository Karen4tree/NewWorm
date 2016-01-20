# -*- coding: utf-8 -*-
import re
import json

from Requests import requests

__author__ = 'ZombieGroup'
# 从Article url指向页面中抓取信息


class Article:

    def __init__(self, url):
        if re.match(r'http://zhuanlan.zhihu.com/.+/\d{8}', url):
            self.url = url
            self.get_api_url()
            self.parser()
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a article url.")

    def get_api_url(self):
        match = re.match(r"http://zhuanlan.zhihu.com/(\w*)/(\d*)", self.url)
        self.api_url = "http://zhuanlan.zhihu.com/api/columns/" + \
            match.group(1) + "/posts/" + match.group(2)

    def parser(self):
        r = requests.get(self.api_url)
        response = json.loads(r.text)
        self.rating = response['rating']
        self.title = response['title']
        self.titleImage = response['titleImage']
        self.topics = response['topics']
        self.author_url = response['author']['profileUrl']
        self.content = response['content']
        self.snapshotUrl = response['snapshotUrl']
        self.publishedTime = response['publishedTime']
        self.column = response['column']['slug']
        self.summary = response['summary']
        self.commentsCount = response['commentsCount']
        self.likesCount = response['likesCount']
        self.comment_url = response['links']['comments']

    def get_comments(self):
        r = requests.get(self.comment_url)
        # TODO: 滚动加载

# TODO: get_article_id()
# TODO: get_author()
