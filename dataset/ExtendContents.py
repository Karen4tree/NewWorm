#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from zhihu_api.Answer import Answer
from zhihu_api.Comment import Comment
from zhihu_api.Question import Question
from qcloudapi.QcloudApi.qcloudapi import QcloudApi

module = 'wenzhi'
action = 'TextSentiment'
config = {
    'Region': 'gz',
    'secretId': 'AKIDS6fypYffcsCMxFmAsac9FOjEdncAlHMM',
    'secretKey': 'eu7cqU9zL90nMKodFwxGihRO62PNqTEB',
    'method': 'get'
}


class ExtendQuestion(Question):
    def __init__(self, url=None, question=None):
        if question is None:
            Question.__init__(self, url)
        elif url is None:
            Question.__init__(self, question.url)

        params = {
            'content': self.get_detail()
        }
        service = QcloudApi(module, config)
        tmp = re.match(r'\"positive\":(.*),\"negative\"', service.call(action, params))
        self.opinion = float(tmp.group(1))


class ExtendAnswer(Answer):
    def __init__(self, url=None, answer=None):
        if answer is None:
            Answer.__init__(self, url)
        elif url is None:
            Answer.__init__(self, answer.url)
        params = {
            'content': self.get_detail()
        }
        service = QcloudApi(module, config)
        tmp = re.match(r'\"positive\":(.*),\"negative\"', service.call(action, params))
        self.opinion = float(tmp.group(1))


class ExtendComment(Comment):
    def __init__(self, url=None, comment=None):
        if comment is None:
            Comment.__init__(self, url)
        elif url is None:
            Comment.__init__(self, comment.url)
        params = {
            'content': self.get_detail()
        }
        service = QcloudApi(module, config)
        tmp = re.match(r'\"positive\":(.*),\"negative\"', service.call(action, params))
        self.opinion = float(tmp.group(1))

