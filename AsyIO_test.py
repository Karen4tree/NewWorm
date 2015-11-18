# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from Requests import *
from gevent import monkey
import gevent
from Topic import Topic
from Question import Question
from gevent.queue import Queue
from DataBase import DataBase
from ReadData import ReadData

result = Queue(maxsize = 20)

user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
database = DataBase(user, host, password, dbname)
readdata = ReadData(user, host, password, dbname)


def slave(name):
    while not result.empty():
        question = result.get_nowait()
        print 'slave %s get one question from the queue'%name
        database.put_question_in_db(question)
        gevent.sleep(0)


def master():
    url = "http://www.zhihu.com/topic/19554927/questions?page="
    url_head = "http://www.zhihu.com"
    r = requests.get(url + '1')
    soup = BeautifulSoup(r.content)
    pages = soup.find("div", class_="zm-invite-pager").find_all("span")
    total_pages = int(pages[len(pages) - 2].find("a").string)
    for i in range(1, total_pages+1):
        r = requests.get(url + '%d' % i)
        soup = BeautifulSoup(r.content)
        question_on_this_page = soup.find_all("a", class_="question_link")
        for question_tag in question_on_this_page:
            question_url = url_head + question_tag["href"]
            print 'put one question in the queue'
            result.put(Question(question_url))

gevent.joinall([
    gevent.spawn(master),
    gevent.spawn(slave,'Fooying'),
    gevent.spawn(slave,'ZhuFengDa'),
    gevent.spawn(slave,'WangZhaoYi'),
])