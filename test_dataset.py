#!/usr/bin/env python
# -*- coding:utf-8 -*-
from dataset.TopicTree import TopicTree

tree = TopicTree()
for item in tree.get_top_level():
    try:
        print item.get_topic_name()
    except AttributeError:
        print "lalala"