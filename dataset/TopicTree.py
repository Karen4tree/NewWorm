#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
from bs4 import BeautifulSoup
from zhihu_api import get_xsrf, get_hash_id
from zhihu_api.Topic import Topic
from zhihu_api.Requests import requests


class TopicTree:
    def __init__(self):
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
            yield url,catagory_id

    def get_top_level(self):
        soup = self.soup
        self.depth += 1
        catagories = soup.find("ul", class_ = "zm-topic-cat-main clearfix").find_all("li")
        for hashtag in catagories:
            url = self.starturl + hashtag.find("a")["href"]
            catagory_id = int(hashtag["data-id"])
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            text = r.text

            # scroll_loading
            loadurl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
            offset = 0
            #tmp_str = soup.find("div", class_ = "zh-general-list clearfix")["data-init"]
            #init_payload = re.match(r'\{\"topic_id\"\:.+\"hash_id\"\:.*\"(.*)\"\}\,\"nodename\"\:.+\}', tmp_str)
            hashid ='f3a16398157b384ed0efe9843dd7798c'#init_payload.group(1)
            _xsrf =get_xsrf(soup)
            responses = []
            while True:
                offset += 20
                payload = {'method': 'next','params': '{"topic_id":%d,"offset":%d,"hash_id":"%s"}'%(catagory_id,offset,hashid),'_xsrf': _xsrf}
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
                tmp = re.match(r'<a target="_blank" href="(.+)">',item)
                url_tail = tmp.group(1)
                yield Topic(url_head + url_tail)

    def get_next_level(self, currentlevel):
        self.depth += 1
        for topic in currentlevel:
            topic.get_child()
