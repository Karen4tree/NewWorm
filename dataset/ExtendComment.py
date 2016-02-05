#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Comment import Comment


class ExtendComment(Comment):
    def __init__(self, url=None, comment=None):
        if comment is None:
            Comment.__init__(self, url)
        elif url is None:
            Comment.__init__(self, comment.url)
        self.opinion = 0.0

    def caculate_opinion(self):
        # TODO:计算意见分
        pass
