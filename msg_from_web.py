# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'

#################################################################
#################################################################
## 此文件中的各个类均为从web中获取信息
## 各类构造时url为必需
## url传入时已经保证确实存在,故本文件中各类均不考虑url指向页面404的问题
#################################################################
#################################################################

# Build-in / Std
import os, sys, time, platform, random
import re, json, cookielib
# requirements
import requests, termcolor, html2text
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
# module
from auth import islogin
from auth import Logging

##########################################################
##
##从auth.py中调用身份信息
##
##########################################################
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")


if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")


reload(sys)
sys.setdefaultencoding('utf8')
##########################################################
##
##从User个人主页抓取信息
##
##########################################################
class User:
    url=None
    soup=None
    def __init__(self, url):
        if url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError("\"" + url + "\"" + " : it isn't a user url.")
        else:
            self.url = url
        if self.soup==None:
            soup=self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_user_id(self):
        match = re.match(r"^(http://www.zhihu.com/peoole/)(.+)$",self.url)
        return match.group(2)

    def get_follower_num(self):
        soup = self.soup
        followers_num = int(soup.find("div", class_="zm-profile-side-following zg-clear").find_all("a")[1].strong.string)
        return followers_num

    def get_followee_num(self):
        soup = self.soup
        followee_num = int(soup.find("div", class_="zm-profile-side-following zg-clear").find_all("a")[0].strong.string)
        return followee_num

    def get_thanks_num(self):
        soup = self.soup
        thanks_num = int(soup.find("span", class_="zm-profile-header-user-thanks").strong.string)
        return thanks_num

    def get_vote_num(self):
        soup=self.soup
        agree_num = int(soup.find("span", class_="zm-profile-header-user-agree").strong.string)
        return agree_num

    def get_ask_num(self):
        soup = self.soup
        ask_num = int(soup.find_all("span", class_="num")[0].string)
        return ask_num

    def get_answer_num(self):
        soup = self.soup
        answer_num = int(soup.find_all("span", class_="num")[1].string)
        return answer_num

    def get_collection_num(self):
        soup = self.soup
        collection_num = int(soup.find("div", class_="profile-navbar clearfix").find_all("a")[3].span.string)
        return collection_num

    def get_followers(self):
        follower_page_url = self.url + '/followers'
        r = requests.get(follower_page_url)
        soup = BeautifulSoup(r.content)
        followers = []
        #需要滚动加载,然而我并不会
        follower_tags = soup.find_all("a", class_="zm-item-link-avatar")
        for follower_tag in follower_tags:
            follower_url = "http://www.zhihu.com"+follower_tag["href"]
            follower = User(follower_url)
            followers.append(follower)
        return followers

    def get_followees(self):
        followee_page_url = self.url + '/followees'
        r = requests.get(followee_page_url)
        soup = BeautifulSoup(r.content)
        followees = []
        #需要滚动加载,然而我并不会
        followee_tags = soup.find_all("a", class_="zm-item-link-avatar")
        for followee_tag in followee_tags:
            followee_url = "http://www.zhihu.com"+followee_tag["href"]
            followee = User(followee_url)
            followees.append(followee)
        return followees

    def get_asks(self):
        asks = []
        asks_num = self.get_ask_num()
        if asks_num == 0:
            return
        else:
            for i in xrange((asks_num - 1) / 20 + 1):
                ask_url = self.url + "/asks?page=" + str(i + 1)
                r = requests.get(ask_url)
                soup = BeautifulSoup(r.content)
                for question in soup.find_all("a", class_="question_link"):
                    url = "http://www.zhihu.com" + question["href"]
                    title = question.string.encode("utf-8")
                    asked = Questions(url, title)
                    asks.append(asked)
    def get_answers(self):
        answers = []
        answers_num = self.get_answer_num()
        if answers_num == 0:
            return
        else:
            for i in xrange((answers_num-1)/20+1):
                answer_url = self.url+"/answers?page="+str(i+1)
                r = requests.get(answer_url)
                soup = BeautifulSoup(r.content)
                for answer_tag in soup.find_all("a", class_="question_link"):
                    answer_url = 'http://www.zhihu.com'+ answer_tag["href"]
                    answer = Answers(answer_url)
                    answers.append(answer)
        return answers

    def get_articles(self):
        articles=[]
        post_url = self.url + '/posts'
        r = requests.get(post_url)
        soup = BeautifulSoup(r.content)
        for article_tag in soup.find_all("a",class_="post-link"):
            article_url = article_tag["href"]
            article = Article(article_url)
            articles.append(article)
        return articles

##########################################################
##
##从Question url指向页面中抓取信息
##
##########################################################
class Questions:
    soup = None
    url = None
    def __init__(self, url, title=None, asker_id=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/question/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url
        if title != None:
            self.title = title
        if self.soup == None:
            self.parser()
        if asker_id != None:
            self.asker_id = asker_id

    def get_question_id(self):
        return self.url[len(self.url)-7:len(self.url)]

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_follower_num(self):
        soup = self.soup
        followers_num = int(soup.find("div", class_="zg-gray-normal").a.strong.string)
        return followers_num

    def get_title(self):
        if hasattr(self, "title"):
            return self.title
        else:
            soup = self.soup
            title = soup.find("h2", class_="zm-item-title").string.encode("utf-8").replace("\n", "")
            self.title = title
            return title

    def get_detail(self):
        soup = self.soup
        detail = soup.find("div", id="zh-question-detail").div.get_text().encode("utf-8")
        return detail

    def get_answers_num(self):
        soup = self.soup
        answers_num = 0
        if soup.find("h3", id="zh-question-answer-num") != None:
            answers_num = int(soup.find("h3", id="zh-question-answer-num")["data-num"])
        return answers_num

    def get_topics(self):
        soup=self.soup
        topic_tags = soup.find_all("a",class_="zm_item_tag")
        topics=[]
        for topic_tag in topic_tags:
            topic_name = topic_tag.contents[0].encode("utf-8").replace("\n", "")
            topic_url = "http://www.zhihu.com/topic/"+topic_tag["href"]
            topic = Topics(topic_url,topic_name)
            topics.append(topic)
        return topics

    def get_answers(self):
        soup = self.soup
        answers = []
        answer_tags=soup.find_all("div", class_="zg-anchor-hidden")["name"]
        for answer_tag in answer_tags:
            answer_url = answer_tag[len(answer_tag)-7:len(answer_tag)]
            answer = Answers(answer_url)
            answers.append(answer)
        return answers

    def get_followers(self):
        follower_page_url = self.url + '/followers'
        r = requests.get(follower_page_url)
        soup = BeautifulSoup(r.content)
        followers = []
        #需要滚动加载,然而我并不会
        follower_tags = soup.find_all("a", class_="zm-item-link-avatar")
        for follower_tag in follower_tags:
            follower_url = "http://www.zhihu.com"+follower_tag["href"]
            follower = User(follower_url)
            followers.append(follower)
        return followers

##########################################################
##
##从Answer url指向页面中抓取信息
##
##########################################################
class Answers:
    url=None
    soup=None
    def __init__(self, url):
        if url[0:len(url) - 8] != "http://www.zhihu.com/question/"+r"\d{8}"+"/answer/":
            raise ValueError("\"" + url + "\"" + " : it isn't a answer url.")
        else:
            self.url=url


class Topics:
    url = None
    soup = None
    def __init__(self, url, name=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/topic/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url
        if name != None:
            self.name=name
    #def get_question_num:
   # def get_follower_num:

#class Collections:
#class Article: