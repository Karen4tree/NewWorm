# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std

from ScrollLoader import *



# 从Article url指向页面中抓取信息
class Article:
    url = None
    soup = None

    def __init__(self, url):
        if re.match(r'http://zhuanlan.zhihu.com/.+/\d{8}', url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a article url.")
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_article_id(self):
        return self.url[len(self.url) - 8:len(self.url)]

    def get_article_title(self):
        soup = self.soup
        # 傻逼知乎是动态加载整个页面的
