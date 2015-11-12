# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'


from Requests import *

# 从Topic url指向页面中抓取信息


class Topic:
    url = None
    soup = None

    def __init__(self, url, name=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/topic/":
            raise ValueError("\"" + url + "\"" + " : it isn't a topic url.")
        else:
            self.url = url
        if name is not None:
            self.name = name
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_topic_id(self):
        topic_id = self.url[len(self.url) - 8:len(self.url)]
        return topic_id

    def get_topic_name(self):
        soup = self.soup
        topic_name = soup.find("h1", class_="zm-editable-content").string
        return topic_name

    def get_question_num(self):
        r = requests.get(self.url + "/questions")
        soup1 = BeautifulSoup(r.content)
        pages = soup1.find("div", class_="zm-invite-pager").find_all("span")
        total_pages = pages[len(pages) - 2].find("a").string
        tmp = (int(total_pages) - 1) * 20  # 每页20个,除最后一页以外
        r = requests.get(self.url + "/questions?page=" + total_pages)
        soup2 = BeautifulSoup(r.content)
        question_on_last_page = soup2.find_all(
            "div", class_="feed-item feed-item-hook question-item")
        question_num = tmp + len(question_on_last_page)
        return question_num

    def get_follower_num(self):
        soup = self.soup
        followers_num = soup.find(
            "div", class_="zm-topic-side-followers-info").find("a").strong.string
        return followers_num

    def get_questions(self):
        url = self.url + "/questions?page="
        url_head = "http://www.zhihu.com"
        r = requests.get(url + '1')
        soup = BeautifulSoup(r.content)
        pages = soup.find("div", class_="zm-invite-pager").find_all("span")
        total_pages = int(pages[len(pages) - 2].find("a").string)
        from Question import Question
        for i in range(1, total_pages):
            r = requests.get(url + '%d' % i)
            soup = BeautifulSoup(r.content)
            question_on_this_page = soup.find_all("a", class_="question_link")
            for question_tag in question_on_this_page:
                question_url = url_head + question_tag["href"]
                yield Question(question_url)