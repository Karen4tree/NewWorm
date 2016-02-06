#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from TopicTree import TopicTree


class TreeWriter(json.JSONEncoder):
    def __init__(self):
        super(TreeWriter, self).__init__()
        self.tree = TopicTree()

    def default(self,node):
        #convert object to a dict
        d = {}
        d['name'] = node.name
        d['children'] = node.children
        #d.update(node.__dict__)
        return d