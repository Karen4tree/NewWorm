# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from Requests import *
from Topic import Topic
from Question import Question
from DataBase import DataBase
from ReadData import ReadData


user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
database = DataBase(user, host, password, dbname)
readdata = ReadData(user, host, password, dbname)
#result = Queue()
topic = Topic("http://www.zhihu.com/topic/19554927")

def slave(name):
    while not question_queue.empty():
        question = question_queue.get()
        print 'slave %s get one question from the queue'%name
        database.put_question_in_db(question)
        gevent.sleep(0)

def master():
    topic.get_questions()


gevent.joinall([
    gevent.spawn(master),
    gevent.spawn(slave,'Fooying'),
    gevent.spawn(slave,'ZhuFengDa'),
    gevent.spawn(slave,'WangZhaoYi'),
])