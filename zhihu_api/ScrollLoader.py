# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std

import json
from __init__ import requests


class ScrollLoader:
    offset = 0
    http_method = None
    url = None
    result = None
    _xsrf = None
    hash_id = None

    def __init__(self, http_method, url, add, _xsrf=None, hash_id=None, start=None):
        self.offset = 0
        self.http_method = http_method
        self.url = url
        self.add = add
        self._xsrf = _xsrf
        self.hash_id = hash_id
        self.start = start

    def run(self):
        while True:
            self.offset += self.add
            # http://zhuanlan.zhihu.com/api/columns/
            if self.http_method == 'get':
                r = requests.get(self.url + "&offset={0}".format(self.offset))
                if not json.loads(r.text):
                    break
                else:
                    for each_article in json.loads(r.text):
                        yield each_article['url']

            # http://www.zhihu.com/node/ProfileFollowersListV2
            if self.http_method == 'post' and self.start == None:
                params = """\"offset":{0},"order_by":"created","hash_id":"{1}\"""".format(
                    self.offset, self.hash_id)
                payload = {'method': 'next',
                           'params': "{" + params + "}", '_xsrf': self._xsrf}
                r = requests.post(self.url, data=payload)
                self.result = json.loads(r.text)['msg']
                if not self.result:
                    break
                else:
                    yield self.result

            # user_url/topics
            if self.http_method == 'post' and self.start != None:
                payload = {'start': self.start,
                           'offset': self.offset, '_xsrf': self._xsrf}
                r = requests.post(self.url, data=payload)
                self.result = json.loads(r.text)['msg']
                if self.result[0] == 0:
                    break
                else:
                    yield self.result[1:]
