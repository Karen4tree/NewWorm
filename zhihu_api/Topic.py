# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

from Requests import requests

__author__ = 'ZombieGroup'


# 从Topic url指向页面中抓取信息


class Topic:
    url = None
    soup = None

    def __init__(self, url, name=None):
        if not (re.match("http://www.zhihu.com/topic/.+", url) or re.match("https://www.zhihu.com/topic/.+", url)):
            raise ValueError("\"" + url + "\"" + " : it isn't a topic url.")
        else:
            self.url = url
        if name is not None:
            self.name = name
        if self.soup is None:
            self.parser()

    def parser(self):
        try:
            r = requests.get(self.url)
            self.soup = BeautifulSoup(r.content)
        except:
            self.parser()

    def get_topic_id(self):
        topic_id = self.url[len(self.url) - 8:len(self.url)]
        return topic_id

    def get_topic_name(self):
        soup = self.soup
        self.name = soup.find("h1", class_ = "zm-editable-content").string
        return self.name

    def get_question_num(self):
        r = requests.get(self.url + "/questions")
        soup1 = BeautifulSoup(r.content)
        try:
            pages = soup1.find("div", class_ = "zm-invite-pager").find_all("span")
            total_pages = pages[len(pages) - 2].find("a").string
            tmp = (int(total_pages) - 1) * 20  # 每页20个,除最后一页以外
            r = requests.get(self.url + "/questions?page=" + total_pages)
            soup2 = BeautifulSoup(r.content)
            question_on_last_page = soup2.find_all("div", class_ = "feed-item feed-item-hook question-item")
            question_num = tmp + len(question_on_last_page)
            return question_num
        except AttributeError:
            return 0

    def get_follower_num(self):
        soup = self.soup
        try:
            followers_num = soup.find("div", class_ = "zm-topic-side-followers-info").find("a").strong.string
            return int(followers_num)
        except AttributeError:
            return 0

    def get_questions(self):
        url = self.url + "/questions?page="
        url_head = "http://www.zhihu.com"
        r = requests.get(url + '1')
        soup = BeautifulSoup(r.content)
        pages = soup.find("div", class_ = "zm-invite-pager").find_all("span")
        total_pages = int(pages[len(pages) - 2].find("a").string)
        from Question import Question
        for i in range(1, total_pages + 1):
            r = requests.get(url + '%d' % i)
            soup = BeautifulSoup(r.content)
            question_on_this_page = soup.find_all("a", class_ = "question_link")
            for question_tag in question_on_this_page:
                question_url = url_head + question_tag["href"]
                yield Question(question_url)

    def get_father(self):
        url = self.url+ "/organize"
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        parrent_div = soup.find(id="zh-topic-organize-parent-editor")
        parrent_url = parrent_div.find_all("a")
        url_head = "http://www.zhihu.com/topic/"
        for item in parrent_url:
            yield Topic(url_head + item["data-token"])

    def get_child(self):
        url = self.url+ "/organize"
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        child_div = soup.find(id="zh-topic-organize-child-editor")
        child_url = child_div.find_all("a")
        url_head = "http://www.zhihu.com/topic/"
        for item in child_url:
            yield Topic(url_head + item["data-token"])

