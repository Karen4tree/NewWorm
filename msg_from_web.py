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
    requests.cookies.load(ignore_discard = True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")

if not islogin():
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
    url = None
    soup = None

    def __init__(self, url):
        if url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError("\"" + url + "\"" + " : it isn't a user url.")
        else:
            self.url = url
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_user_id(self):
        tmp = re.match(r'^(http://www.zhihu.com/people/)(.+)$', self.url)
        user_id = tmp.group(2)
        return user_id

    def get_follower_num(self):
        soup = self.soup
        followers_num = int(
            soup.find("div", class_ = "zm-profile-side-following zg-clear").find_all("a")[1].strong.string)
        return followers_num

    def get_followee_num(self):
        soup = self.soup
        followee_num = int(
            soup.find("div", class_ = "zm-profile-side-following zg-clear").find_all("a")[0].strong.string)
        return followee_num

    def get_thanks_num(self):
        soup = self.soup
        thanks_num = int(soup.find("span", class_ = "zm-profile-header-user-thanks").strong.string)
        return thanks_num

    def get_vote_num(self):
        soup = self.soup
        agree_num = int(soup.find("span", class_ = "zm-profile-header-user-agree").strong.string)
        return agree_num

    def get_ask_num(self):
        soup = self.soup
        ask_num = int(soup.find_all("span", class_ = "num")[0].string)
        return ask_num

    def get_answer_num(self):
        soup = self.soup
        answer_num = int(soup.find_all("span", class_ = "num")[1].string)
        return answer_num

    def get_articles_num(self):
        soup = self.soup
        articles_num = int(soup.find_all("span", class_ = "num")[2].string)
        return articles_num

    def get_collection_num(self):
        soup = self.soup
        collection_num = int(soup.find("div", class_ = "profile-navbar clearfix").find_all("a")[3].span.string)
        return collection_num

    def get_following_topics_num(self):
        soup = self.soup
        tag_strings = soup.find_all("div", class_ = "zm-profile-side-section-title")
        tag_string = tag_strings[len(tag_strings) - 1].find("a").strong.string
        substr = re.split("\s+", tag_string)
        num = int(substr[0])
        return num

    def get_following_columns_num(self):
        soup = self.soup
        tag_strings = soup.find_all("div", class_ = "zm-profile-side-section-title")
        tag_string = tag_strings[len(tag_strings) - 2].find("a").strong.string
        substr = re.split("\s+", tag_string)
        num = int(substr[0])
        return num

    def get_location(self):  # 所在地
        soup = self.soup
        location = None
        if soup.find("span", class_ = "location item") is not None:
            location = soup.find("span", class_ = "location item").string
        return location

    def get_business(self):  # 行业
        soup = self.soup
        business_item = None
        if soup.find("span", class_ = "business item") is not None:
            business_item = soup.find("span", class_ = "business item").string
        return business_item

    def get_employment(self):  # 公司
        soup = self.soup
        employment = None
        if soup.find("span", class_ = "employment item") is not None:
            employment = soup.find("span", class_ = "employment item").string
        return employment

    def get_position(self):  # 职位
        soup = self.soup
        position = None
        if soup.find("span", class_ = "position item") is not None:
            position = soup.find("span", class_ = "position item").string
        return position

    def get_education(self):
        soup = self.soup
        education = None
        if soup.find("span", class_ = "education item") is not None:
            education = soup.find("span", class_ = "education item").string
        return education

    def get_education_extra(self):
        soup = self.soup
        education_extra = None
        if soup.find("span", class_ = "education-extra item") is not None:
            education_extra = soup.find("span", class_ = "education-extra item").string
        return education_extra

    def get_followers(self):
        follower_page_url = self.url + '/followers'
        r = requests.get(follower_page_url)
        soup = BeautifulSoup(r.content)
        followers = []
        # 需要滚动加载,然而我并不会
        follower_tags = soup.find_all("a", class_ = "zm-item-link-avatar")
        for follower_tag in follower_tags:
            follower_url = "http://www.zhihu.com" + follower_tag["href"]
            follower = User(follower_url)
            followers.append(follower)
        return followers

    def get_followees(self):
        followee_page_url = self.url + '/followees'
        r = requests.get(followee_page_url)
        soup = BeautifulSoup(r.content)
        followees = []
        # 需要滚动加载,然而我并不会
        followee_tags = soup.find_all("a", class_ = "zm-item-link-avatar")
        for followee_tag in followee_tags:
            followee_url = "http://www.zhihu.com" + followee_tag["href"]
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
                for question in soup.find_all("a", class_ = "question_link"):
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
            for i in xrange((answers_num - 1) / 20 + 1):
                answer_url = self.url + "/answers?page=" + str(i + 1)
                r = requests.get(answer_url)
                soup = BeautifulSoup(r.content)
                for answer_tag in soup.find_all("a", class_ = "question_link"):
                    answer_url = 'http://www.zhihu.com' + answer_tag["href"]
                    answer = Answers(answer_url)
                    answers.append(answer)
        return answers

    def get_articles(self):
        articles = []
        post_url = self.url + '/posts'
        r = requests.get(post_url)
        soup = BeautifulSoup(r.content)
        for article_tag in soup.find_all("a", class_ = "post-link"):
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
        if title is not None:
            self.title = title
        if self.soup is None:
            self.parser()
        if asker_id is not None:
            self.asker_id = asker_id

    def get_question_id(self):
        return self.url[len(self.url) - 7:len(self.url)]

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

    def get_follower_num(self):
        soup = self.soup
        followers_num = int(soup.find("div", class_ = "zg-gray-normal").a.strong.string)
        return followers_num

    def get_title(self):
        if hasattr(self, "title"):
            return self.title
        else:
            soup = self.soup
            title = soup.find("h2", class_ = "zm-item-title").string.encode("utf-8").replace("\n", "")
            self.title = title
            return title

    def get_detail(self):
        soup = self.soup
        detail = soup.find("div", id = "zh-question-detail").div.get_text().encode("utf-8")
        return detail

    def get_answers_num(self):
        soup = self.soup
        answers_num = 0
        if soup.find("h3", id = "zh-question-answer-num") is not None:
            answers_num = int(soup.find("h3", id = "zh-question-answer-num")["data-num"])
        return answers_num

    def get_topics(self):
        soup = self.soup
        topic_tags = soup.find_all("a", class_ = "zm_item_tag")
        topics = []
        for topic_tag in topic_tags:
            topic_name = topic_tag.contents[0].encode("utf-8").replace("\n", "")
            topic_url = "http://www.zhihu.com/topic/" + topic_tag["href"]
            topic = Topics(topic_url, topic_name)
            topics.append(topic)
        return topics

    def get_answers(self):
        soup = self.soup
        answers = []
        answer_tags = soup.find_all("div", class_ = "zg-anchor-hidden")["name"]
        for answer_tag in answer_tags:
            answer_url = answer_tag[len(answer_tag) - 7:len(answer_tag)]
            answer = Answers(answer_url)
            answers.append(answer)
        return answers

    def get_followers(self):
        follower_page_url = self.url + '/followers'
        r = requests.get(follower_page_url)
        soup = BeautifulSoup(r.content)
        followers = []
        # 需要滚动加载,然而我并不会
        follower_tags = soup.find_all("a", class_ = "zm-item-link-avatar")
        for follower_tag in follower_tags:
            follower_url = "http://www.zhihu.com" + follower_tag["href"]
            follower = User(follower_url)
            followers.append(follower)
        return followers


##########################################################
##
##从Answer url指向页面中抓取信息
##
##########################################################
class Answers:
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
        tmp = re.match(r'^(http://www.zhihu.com/question/)(\d{8})(/answer/\d{8})$', self.url)
        question_id = tmp.group(2)
        return question_id

    def get_author_id(self):
        soup = self.soup
        author_tag = soup.find("h3", class_ = "zm-item-answer-author-wrap")
        author_url = author_tag.find("a")["href"]
        tmp = re.match(r'^(/people/)(.+)$', author_url)
        author_id = tmp.group(2)
        return author_id

    def get_detail(self):
        soup = self.soup
        detail = soup.find("div", class_ = "zm-editable-content clearfix").string
        return detail

    def get_upvote_num(self):
        soup = self.soup
        upvote = soup.find("span", class_ = "count").string
        return upvote

    def get_visited_times(self):
        soup = self.soup
        visited_times = soup.find("div", class_ = "zm-side-section zh-answer-status")\
            .find("div", class_ = "zm-side-section-inner")\
            .find_all('p')[1].strong.string
        return visited_times

    def get_upvoters(self):
        soup = self.soup
        data_aid = soup.find("div", class_= "zm-item-answer ")["data-aid"]
        request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2'
        r = requests.get(request_url, params = {"params": "{\"answer_id\":\"%d\"}" % int(data_aid)})
        soup = BeautifulSoup(r.content)
        voters_info = soup.find_all("span")[1:-1]
        if len(voters_info) == 0:
            return
            yield
        else:
            for voter_info in voters_info:
                if voter_info.string == (u"匿名用户、" or u"匿名用户"):
                    voter_url = None
                    yield User(voter_url)
                else:
                    voter_url = "http://www.zhihu.com" + str(voter_info.a["href"])
                    yield User(voter_url)


##########################################################
##
##从Topic url指向页面中抓取信息
##
##########################################################
class Topics:
    url = None
    soup = None

    def __init__(self, url, name=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/topic/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
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
        topic_name = soup.find("h1", class_ = "zm-editable-content").string
        return topic_name

    def get_questions_num(self):
        r = requests.get(self.url + "/questions")
        soup1 = BeautifulSoup(r.content)
        pages = soup1.find("div", class_ = "zm-invite-pager").find_all("span")
        total_pages = pages[len(pages) - 2].find("a").string
        tmp = (int(total_pages) - 1) * 20  # 每页20个,除最后一页以外
        r = requests.get(self.url + "/questions?page=" + total_pages)
        soup2 = BeautifulSoup(r.content)
        question_on_last_page = soup2.find_all("div", class_ = "feed-item feed-item-hook question-item")
        question_num = tmp + len(question_on_last_page)
        return question_num

    def get_followers_num(self):
        soup = self.soup
        followers_num = soup.find("div", class_="zm-topic-side-followers-info").find("a").strong.string
        return followers_num

    def get_followers(self):
        soup = self.soup
        #需要滚动加载

    def get_questions(self):
        url = self.url+"/questions?page="
        url_head = "http://www.zhihu.com"
        r = requests.get(url + '1')
        soup = BeautifulSoup(r.content)
        question_tags = []
        pages = soup.find("div", class_ = "zm-invite-pager").find_all("span")
        total_pages = int(pages[len(pages) - 2].find("a").string)
        for i in range(1,total_pages):
            r = requests.get(url+'%d'%i)
            soup = BeautifulSoup(r.content)
            question_on_this_page =soup.find_all("a", class_ = "question_link")
            for question_tag in question_on_this_page:
                question_url = url_head + question_tag["href"]
                yield Questions(question_url)



class Collections:
    url = None
    soup = None

    def __init__(self, url, name=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/collection/":
            raise ValueError("\"" + url + "\"" + " : it isn't a collection url.")
        else:
            self.url = url
        if name is not None:
            self.name = name
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)


class Article:
    url = None
    soup = None

    def __init__(self, url):
        self.url = url
        if self.soup is None:
            self.parser()

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content)

