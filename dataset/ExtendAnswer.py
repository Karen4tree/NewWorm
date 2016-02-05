#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Answer import Answer


class ExtendAnswer(Answer):
    def __init__(self, url=None, answer=None):
        if answer is None:
            Answer.__init__(self,url)
        elif url is None:
            Answer.__init__(self,answer.url)
        self.opinion = 0.0

    def caculateOpinion(self):
        # TODO:计算意见分
        pass
