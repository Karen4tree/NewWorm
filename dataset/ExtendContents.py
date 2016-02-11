#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Answer import Answer
from zhihu_api.Comment import Comment
from zhihu_api.Question import Question


class ExtendQuestion(Question):
    def __init__(self, url=None, question=None):
        if question is None:
            Question.__init__(self, url)
        elif url is None:
            Question.__init__(self, question.url)
        self.opinion = 0.0


class ExtendAnswer(Answer):
    def __init__(self, url=None, answer=None):
        if answer is None:
            Answer.__init__(self, url)
        elif url is None:
            Answer.__init__(self, answer.url)
        self.opinion = 0.0


class ExtendComment(Comment):
    def __init__(self, url=None, comment=None):
        if comment is None:
            Comment.__init__(self, url)
        elif url is None:
            Comment.__init__(self, comment.url)
        self.opinion = 0.0

