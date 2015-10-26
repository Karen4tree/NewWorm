# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std


from ScrollLoader import ScrollLoader
from Requests import *

from Answer import Answer
from User import User


# 从Question url指向页面中抓取信息
class Question:
    soup = None
    url = None

    def __init__(self, url, title=None, asker_id=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/question/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url
        if title is not None:
            self.title = title
        if self.soup is None:
            self.parser()
        if asker_id is not None:
            self.asker_id = asker_id

    def get_question_id(self):
        return self.url[len(self.url) - 8:len(self.url)]

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_follower_num(self):
        soup = self.soup
        followers_num = int(
            soup.find("div", class_="zg-gray-normal").a.strong.string)
        return followers_num

    def get_title(self):
        if hasattr(self, "title"):
            return self.title
        else:
            soup = self.soup
            title = soup.find(
                "h2", class_="zm-item-title").string.encode("utf-8").replace("\n", "")
            self.title = title
            return title

    def get_detail(self):
        soup = self.soup
        detail = soup.find(
            "div", id="zh-question-detail").div.get_text().encode("utf-8")
        return detail

    def get_answers_num(self):
        soup = self.soup
        answers_num = 0
        if soup.find("h3", id="zh-question-answer-num") is not None:
            answers_num = int(
                soup.find("h3", id="zh-question-answer-num")["data-num"])
        return answers_num

    def get_topics(self):
        soup = self.soup
        topic_tags = soup.find_all("a", class_="zm-item-tag")
        from Topic import Topic
        for topic_tag in topic_tags:
            topic_name = topic_tag.string
            topic_url = "http://www.zhihu.com" + topic_tag["href"]
            yield Topic(topic_url, topic_name)

    def get_answers(self):
        soup = self.soup
        answer_tags = soup.find_all("div", class_="zm-item-answer")
        for answer_tag in answer_tags:
            answer_url = self.url + "/answer/" + answer_tag["data-atoken"]
            yield Answer(answer_url)

    def get_followers(self):
        follower_page_url = self.url + '/followers'
        r = requests.get(follower_page_url)
        soup = BeautifulSoup(r.content)
        followers = []
        # 需要滚动加载,然而我并不会
        follower_tags = soup.find_all("a", class_="zm-item-link-avatar")
        for follower_tag in follower_tags:
            follower_url = "http://www.zhihu.com" + follower_tag["href"]
            follower = User(follower_url)
            followers.append(follower)
        return followers
