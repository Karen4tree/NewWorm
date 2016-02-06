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
        #d['name'] = node.__class__.__name__
        #d['children'] = node.__module__
        d.update(node.__dict__)
        return d


writer = TreeWriter()
writer.tree.grow(writer.tree.superRoot)

print writer.default(writer.tree.superRoot)