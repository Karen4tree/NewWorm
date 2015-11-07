# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std


from ScrollLoader import ScrollLoader
from Requests import *

from Answer import Answer
from User import User

# 从Comment url指向页面中抓取信息
class Comment:
    def __init__(self, url, question_id=None, answer_id=None, content=None,vote_num=0):
        self.question_id=question_id
        self.answer_id=answer_id
        self.content=content
        self.vote_num=vote_num
