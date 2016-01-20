# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from User import User
from Requests import requests

__author__ = 'ZombieGroup'
# 从Collection url指向页面中抓取信息


class Collection:
    url = None
    soup = None

    def __init__(self, url, name=None):
        if re.match(r"http://www.zhihu.com/collection/\d{8}", url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" +
                             " : it isn't a collection url.")
        if name is not None:
            self.name = name
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_collection_id(self):
        return self.url[len(self.url) - 8:len(self.url)]

    def get_collection_name(self):
        soup = self.soup
        name = soup.find("h2", id="zh-fav-head-title").string
        return name

    def get_creator(self):
        soup = self.soup
        creator_tag = soup.find(
            "div", class_="zg-section-title").find("div").find_all("a")[1]["href"]
        creator_url = "http://www.zhihu.com" + \
            creator_tag[0:len(creator_tag) - 12]
        creator = User(creator_url)
        return creator

    def get_answers(self):
        soup = self.soup
        if soup.find("div", class_="zm-invite-pager") is not None:
            total_pages = soup.find(
                "div", class_="zm-invite-pager").find_all("span")
            total_pages = int(total_pages[len(total_pages) - 2].string)
            for i in range(1, total_pages):
                url = self.url + "?page=%d" % i
                r = requests.get(url)
                soup = BeautifulSoup(r.content)
                tags = soup.find(
                    "div", id="zh-list-answer-wrap").find_all("div", class_="zm-item")
                for tag in tags:
                    question_part = tag.find("h2").find("a")["href"]
                    answer_part = tag.find(
                        "div", class_="zm-item-answer ")["data-atoken"]
                    answer_url = "http://www.zhihu.com" + question_part + "/answer/" + answer_part
                    from Answer import Answer
                    yield Answer(answer_url)
        else:
            tags = soup.find(
                "div", id="zh-list-answer-wrap").find_all("div", class_="zm-item")
            for tag in tags:
                question_part = tag.find("h2").find("a")["href"]
                answer_part = tag.find(
                    "div", class_="zm-item-answer ")["data-atoken"]
                answer_url = "http://www.zhihu.com" + question_part + "/answer/" + answer_part
                from Answer import Answer
                yield Answer(answer_url)
