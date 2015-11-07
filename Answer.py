# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'

from Requests import *


# 从Answer url指向页面中抓取信息
class Answer:
    url = None
    soup = None

    def __init__(self, url):
        if re.match(r"http://www.zhihu.com/question/\d{8}/answer/\d{8}", url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a answer url.")
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_answer_id(self):
        id = self.url[len(self.url) - 8:len(self.url)]
        return id

    def get_question_id(self):
        tmp = re.match(
            r'^(http://www.zhihu.com/question/)(\d{8})(/answer/\d{8})$', self.url)
        question_id = tmp.group(2)
        return question_id

    def get_author_id(self):
        soup = self.soup
        author_tag = soup.find("h3", class_="zm-item-answer-author-wrap")
        author_id = 'None'
        try:
            author_url = author_tag.find("a")["href"]
            tmp = re.match(r'^(/people/)(.+)$', author_url)
            author_id = tmp.group(2)
        except:
            pass
        finally:
            return author_id

    def get_detail(self):
        soup = self.soup
        detail = soup.find("div", class_="zm-editable-content clearfix")
        return detail

    def get_upvote_num(self):
        soup = self.soup
        upvote = soup.find("span", class_="count").string
        return upvote

    def get_visited_times(self):
        soup = self.soup
        visited_times = soup.find("div", class_="zm-side-section zh-answer-status")\
            .find("div", class_="zm-side-section-inner")\
            .find_all('p')[1].strong.string
        return visited_times

    def get_upvoters(self):  # 匿名用户先忽略了
        soup = self.soup
        data_aid = soup.find(
            "div", class_="zm-item-answer  zm-item-expanded")["data-aid"]
        request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2'
        r = requests.get(request_url, params={
                         "params": "{\"answer_id\":\"%d\"}" % int(data_aid)})
        soup = BeautifulSoup(r.content)
        voters_info = soup.find_all("span")[1:-1]
        if len(voters_info) == 0:
            return
        else:
            from User import User
            for voter_info in voters_info:
                if voter_info.find('a'):
                    voter_url = "http://www.zhihu.com" + \
                        str(voter_info.a["href"])
                    yield User(voter_url)

    # ToDo: def get_comments()
