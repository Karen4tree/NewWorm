# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from Requests import *
from Topic import Topic
from Question import Question
from DataBase import DataBase
from ReadData import ReadData
from gevent.pool import Group

user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
database = DataBase(user, host, password, dbname)
readdata = ReadData(user, host, password, dbname)
#result = Queue()
topic = Topic("http://www.zhihu.com/topic/19554927")

def slave(name):
    try:
        while True:
            question = question_queue.get(timeout=1)
            print 'slave %s get one question from the queue'%name
            database.put_question_in_db(question)
            gevent.sleep(0)
    except Empty:
        print 'slave %s is dead'%name

def master():
    topic.get_questions()

group = Group()
gevent.spawn(master)
group.map(slave,xrange(100))

group.join()
