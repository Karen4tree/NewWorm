#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Question import Question
from OpinionMeasuring import OpinionMeasuring


class ExtendQuestion(Question):
    def __init__(self, url=None, question=None):
        if question is None:
            Question.__init__(self, url)
        elif url is None:
            Question.__init__(self, question.url)
        self.opinion = 0.0

    def caculateOpinion(self):
        # TODO:计算意见分
        pass
