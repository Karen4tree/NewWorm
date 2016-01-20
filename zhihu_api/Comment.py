# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from Requests import requests
from ScrollLoader import ScrollLoader

__author__ = 'ZombieGroup'
# 从Comment url指向页面中抓取信息


class Comment:
    def __init__(self, url, comment_id=None, question_id=None, answer_id=None, author_id=None, content=None, time=None,
                 vote_num=0):
        self.comment_id = comment_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.author_id = author_id
        self.content = content
        self.time = time
        self.vote_num = vote_num
        if re.match(r"http:/www.zhihu.com/question/\d{8}/answer/\d{8}comment/\d{8}", url):
            self.url = url
        else:
            raise ValueError("\"" + url + "\"" + " : it isn't a comment url.")
        self.parser()

    def parser(self):
        try:
            r = requests.get(self.url)
            self.soup = BeautifulSoup(r.content)
        except:
            self.parser()

    def get_question_id(self):
        tmp = re.match(r'^(http://www.zhihu.com/question/)(\d{8})(/answer/\d{8})$', self.url)
        question_id = tmp.group(2)
        return question_id

    # Todo:获取answer_id
    # 在Answer.py里面answer_id = self.url[len(self.url) - 8:len(self.url)],但是不能理解后面的这个表达式是什么意思，我能不能继续使用
    def get_answer_id(self):
        id = self.url[len(self.url) - 8:len(self.url)]
        return id

    def get_comment_id(self):
        # 直接寻找与内容匹配的data-reactid,问题是，一个页面有那么多data-reactid，不知道能不能这样找
        # 如果不能，根据问题ID+回答ID+作者ID+内容+时间利用hash自己建一个ID
        # 所有函数都有一个问题，匹配结果有多个的时候也可以直接找吗，如answer.py里面的get_detail匹配zm-editable-content clearfix。下面的问题与这儿的问题是一致的
        soup = self.soup
        comment_id = \
            soup.find("div", class_ = "_CommentItem_root_PQNS").find("div", class_ = "_CommentItem_body_3qwB").find(
                "div", class_ = "_CommentItem_content_CYqW")["data-reactid"].string
        return comment_id

    def get_author_id(self):
        # 找到author_id的外层标签是div class="_CommentItem_header_2JGh"。
        soup = self.soup
        author_tag = soup.find("div", class_ = "_CommentItem_header_2JGh")
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
        detail = str(soup.find("div", class_ = "_CommentItem_content_CYqW"))
        # detail = html2text.html2text(detail)
        return detail

    def get_time(self):
        # 一层层地匹配div有必要吗
        soup = self.soup
        time = str(
                soup.find("div", class_ = "_CommentItem_root_PQNS").find("div", class_ = "_CommentItem_body_3qwB").find(
                        "div", class_ = "_CommentItem_footer_46v8 clearfix").find("time")["title"])
        return time

    def get_vote_num(self):
        # 有两个span，不知道怎么搜索
        soup = self.soup
        vote = 0
        try:
            vote = str(
                soup.find("div", class_ = "_CommentItem_root_PQNS").find("div", class_ = "_CommentItem_body_3qwB").find(
                        "div", class_ = "_CommentItem_footer_46v8 clearfix").find("span",class_ = "_CommentItem_likes_2hey").span)
        except:
            pass
        finally:
            return vote
