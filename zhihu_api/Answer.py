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

    def get_author(self):
        soup = self.soup
        from User import User
        try:
            author_tag = soup.find("a", class_="author-link")
            author_url = author_tag['href']
            author = User("http://www.zhihu.com"+author_url)
            return author
        except:
            return None

    def get_author_id(self):
        author = self.get_author()
        if author is None:
            return None
        else:
            return author.get_user_id()

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

    def get_post_time(self):
        soup = self.soup
        timestr = soup.find("a", class_ = "answer-date-link last_updated meta-item")["data-tip"]
        timestr = str(timestr)
        tmp = re.split(r'\s', timestr)
        timestr = tmp[-1]
        if re.match(r'\d{4}-\d{2}-\d{2}',timestr):
            timestr += " 00:00:00"
        elif re.match(r'\d{2}\:\d{2}',timestr):
            if tmp[1] == '昨天':
                import datetime
                threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 1))
                string = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
                datestring = re.split(r'\s', string)
                datestring = datestring[0]
                timestr = datestring + " " +timestr
            else:
                import time
                string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                datestring = re.split(r'\s', string)
                datestring = datestring[0]
                timestr = datestring + " " +timestr
        return timestr

    def get_last_edit_time(self):
        soup = self.soup
        timestr = soup.find("a", class_ = "answer-date-link last_updated meta-item").string
        tmp = re.split(r'\s',timestr)
        timestr = tmp[-1]
        if re.match(r'\d{4}-\d{2}-\d{2}',timestr):
            timestr += " 00:00:00"
        elif re.match(r'\d{2}\:\d{2}',timestr):
            if tmp[1] == '昨天':
                import datetime
                threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 1))
                string = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
                datestring = re.split(r'\s', string)
                datestring = datestring[0]
                timestr = datestring + " " +timestr
            else:
                import time
                string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                datestring = re.split(r'\s', string)
                datestring = datestring[0]
                timestr = datestring + " " +timestr
        return timestr

    def get_upvoters(self):  # 匿名用户先忽略了
        soup = self.soup
        data_aid = soup.find("div", class_="zm-item-answer  zm-item-expanded")["data-aid"]
        request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2'
        r = requests.get(request_url, params={"params": "{\"answer_id\":\"%d\"}" % int(data_aid)})
        soup = BeautifulSoup(r.content)
        voters_info = soup.find_all("span")[1:-1]
        if len(voters_info) != 0:
            from User import User
            for voter_info in voters_info:
                if voter_info.find('a'):
                    voter_url = "http://www.zhihu.com" + str(voter_info.a["href"])
                    # Bloom
                    #if not userBloom.is_element_exist(voter_url):
                    #   userBloom.is_element_exist(voter_url)
                    yield User(voter_url)
                    # ToDo: def get_comments()
