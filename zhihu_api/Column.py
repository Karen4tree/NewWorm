# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std

from __init__ import *
from ScrollLoader import ScrollLoader



# 从Article url指向页面中抓取信息


class Column:
    url = None
    soup = None

    def __init__(self, url):
        if re.match(r'http://zhuanlan.zhihu.com/.+', url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a column url.")
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_column_name(self):
        m = re.search(r"http://zhuanlan.zhihu.com/(.*)", self.url)
        return m.group(1)

    def get_articles(self):
        column_name = self.get_column_name()
        scroll_loader = ScrollLoader("get", "http://zhuanlan.zhihu.com/api/columns/" + column_name + "/posts?limit=10",
                                     10)
        for response in scroll_loader.run():
            yield Article("http://zhuanlan.zhihu.com" + response)
    # TODO: get follower num
    # TODO: get author
