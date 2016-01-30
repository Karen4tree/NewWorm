# -*- coding: utf-8 -*-
import re
import html2text
from bs4 import BeautifulSoup

from Requests import requests

__author__ = 'ZombieGroup'
# 从Answer url指向页面中抓取信息


class Answer:

    def __init__(self, url):
        if re.match(r"http://www.zhihu.com/question/\d{8}/answer/\d{8}", url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a answer url.")
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
        text = None
        try:
            detail = str(
                soup.find("div", class_="zm-editable-content clearfix"))
            text = html2text.html2text(detail)
            # TODO: 改H5
            r = re.findall(
                r'&lt;img\ssrc=".*"\ndata-rawwidth=".+"\sdata-rawheight=".+"\sclass=".+"\nwidth=".+"&gt;!\[\]\(.+\)', text)
            for i in r:
                t = re.split(
                    r'(&lt;img\ssrc=")(.*)("\ndata-rawwidth=".+"\sdata-rawheight=".+"\sclass=".+"\nwidth=".+"&gt;)(!\[\])\((.+)\)', i)
                text = text.replace(i, t[4] + '(' + t[2] + ')')
        except:
            pass
        finally:
            return text

    def get_upvote_num(self):
        soup = self.soup
        upvote = 0
        try:
            upvote = soup.find("span", class_="count").string
        except:
            pass
        finally:
            return upvote

    def get_visited_times(self):
        soup = self.soup
        visited_times = 0
        try:
            visited_times = soup.find("div", class_="zm-side-section zh-answer-status").find(
                "div", class_="zm-side-section-inner").find_all('p')[1].strong.string
        except:
            pass
        finally:
            return visited_times

    def get_upvoters(self):  # 匿名用户先忽略了
        soup = self.soup
        data_aid = soup.find("div", class_="zm-item-answer  zm-item-expanded")["data-aid"]
        request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2'
        r = requests.get(request_url, params={"params": "{\"answer_id\":\"%d\"}" % int(data_aid)})
        soup = BeautifulSoup(r.content)
        voters_info = soup.find_all("span")[1:-1]
        if len(voters_info) == 0:
            return
        else:
            from User import User
            for voter_info in voters_info:
                if voter_info.find('a'):
                    voter_url = "http://www.zhihu.com" + str(voter_info.a["href"])
                    # Bloom
                    #if not userBloom.is_element_exist(voter_url):
                    #   userBloom.is_element_exist(voter_url)
                    yield User(voter_url)

                    # ToDo: def get_comments()
