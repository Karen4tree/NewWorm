#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
from bs4 import BeautifulSoup
from zhihu_api import get_xsrf, get_hash_id
from zhihu_api.Topic import Topic
from zhihu_api.Requests import requests

# 现阶段使用知乎本身的层次结构,如果有必要,可以再上BRT


class TreeNode:
    def __init__(self, topic):
        self.parent = None
        self.topic = topic
        self.name = topic.get_topic_name()
        self.children = []
        self.depth = 0

    def set_parent(self, parent):
        parent.insert_children(self)
        self.parent = parent

    def set_content(self, content):
        self.topic = content

    def insert_children(self, child):
        if self.children == []:
            self.depth = child.depth + 1
        elif child.depth > max(self.children):
            self.depth = child.depth + 1
        self.children.append(child)
        child.parent = self


class TopicTree:
    def __init__(self):
        self.depth = 0
        self.rootTopic = Topic("https://www.zhihu.com/topic/19776749")
        self.root = TreeNode(self.rootTopic)

    def grow(self, treenode):
        for topic in treenode.topic.get_child():
            print topic.get_topic_name()
            child = TreeNode(topic)
            treenode.insert_children(child)
        for node in treenode.children:
            self.grow(node)

    def trans_into_BRT(self):
        pass
