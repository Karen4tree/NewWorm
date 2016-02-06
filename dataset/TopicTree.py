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
    def __init__(self, content):
        self.parent = None
        self.content = content
        self.children = []
        self.depth = 0

    def set_parent(self, parent):
        parent.insert_children(self)
        self.parent = parent

    def set_content(self, content):
        self.content = content

    def insert_children(self, child):
        if self.children == []:
            self.depth = child.depth + 1
        elif child.depth > max(self.children):
            self.depth = child.depth + 1
        self.children.append(child)
        child.parent = self


class TopicTree:
    def __init__(self):
        self.superRoot = TreeNode('SuperRoot')
        self.depth = 0
        self.starturl = 'https://www.zhihu.com/topics'
        self.parser()

    def parser(self):
        try:
            r = requests.get(self.starturl)
            self.soup = BeautifulSoup(r.content)
        except:
            self.parser()

    def get_roots(self):
        soup = self.soup
        catagories = soup.find("ul", class_ = "zm-topic-cat-main clearfix").find_all("li")
        for hashtag in catagories:
            url = self.starturl + hashtag.find("a")["href"]
            catagory_id = int(hashtag["data-id"])
            tmp = TreeNode({'url': url, 'catagory_id': catagory_id})
            self.superRoot.insert_children(tmp)

    def get_top_level(self):
        for node in self.superRoot.children:
            url = node.content['url']
            catagory_id = node.content['catagory_id']
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            text = r.text

            # scroll_loading
            loadurl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
            offset = 0
            hashid = 'f3a16398157b384ed0efe9843dd7798c'
            _xsrf = get_xsrf(soup)
            responses = []
            while True:
                offset += 20
                payload = {'method': 'next',
                           'params': '{"topic_id":%d,"offset":%d,"hash_id":"%s"}' % (catagory_id, offset, hashid),
                           '_xsrf': _xsrf}
                r = requests.post(loadurl, data = payload)
                result = json.loads(r.text)['msg']
                if not result:
                    break
                else:
                    responses.append(result)
            # end of scroll loading
            for response in responses:
                for item in response:
                    text += item

            topic_url = re.findall(r'<a target="_blank" href=".+">', text)
            url_head = 'http://www.zhihu.com'
            for item in topic_url:
                tmp = re.match(r'<a target="_blank" href="(.+)">', item)
                url_tail = tmp.group(1)
                node.insert_children(TreeNode(Topic(url_head + url_tail)))

    def grow(self, node):
        if node == self.superRoot:
            self.get_roots()
            self.get_top_level()
            for item in self.superRoot.children:
                self.grow(item)
        else:
            for child in node.content.getchild():
                node.insert_children(TreeNode(child))

            for subnode in node.children:
                self.grow(subnode)

    def trans_into_BRT(self):
        pass
