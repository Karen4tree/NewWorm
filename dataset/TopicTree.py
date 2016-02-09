#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
from bs4 import BeautifulSoup
from zhihu_api import get_xsrf, get_hash_id
from zhihu_api.Topic import Topic
from zhihu_api.Requests import requests
<<<<<<< HEAD


=======
>>>>>>> a37b25c6f87050f9546d768078b983b97cd20850
# 现阶段使用知乎本身的层次结构,如果有必要,可以再上BRT


class TreeNode:
<<<<<<< HEAD
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
=======
    def __init__(self,content):
        self.parent = None
        self.content = content
        self.children = []
        self.depth = 0

    def setParent(self, parent):
        parent.insertChildren(self)
        self.parent = parent

    def setContent(self, content):
        self.content = content

    def insertChildren(self, child):
>>>>>>> a37b25c6f87050f9546d768078b983b97cd20850
        if self.children == []:
            self.depth = child.depth + 1
        elif child.depth > max(self.children):
            self.depth = child.depth + 1
        self.children.append(child)
        child.parent = self


class TopicTree:
    def __init__(self):
<<<<<<< HEAD
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

=======
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
            tmp = TreeNode({'url':url,'catagory_id':catagory_id})
            self.superRoot.insertChildren(tmp)

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
                node.insertChildren(TreeNode(Topic(url_head + url_tail)))

    def grow(self, node):
        if node == self.superRoot:
            self.get_roots()
            self.get_top_level()
            for item in self.superRoot.children:
                self.grow(item)

        for child in node.content.getchild():
            node.insertChildren(TreeNode(child))

        for subnode in node.children:
            self.grow(subnode)
>>>>>>> a37b25c6f87050f9546d768078b983b97cd20850

    def trans_into_BRT(self):
        pass
