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


def question_slave(name):
    try:
        while True:
            question = question_queue.get(timeout=1)
            print 'slave %s get one question from the queue' % name
            database.put_question_in_db(question)
            question.get_answers()
            gevent.sleep(0)
    except Empty:
        print 'slave %s is dead' % name


def answer_slave(name):
    try:
        while True:
            answer = answer_queue.get(timeout=1)
            print 'slave %s get one answer from the queue' % name
            database.put_answer_in_db(answer)
            answer.get_upvoters()
            gevent.sleep(0)
    except Empty:
        print 'slave %s is dead' % name


def user_slave(name):
    try:
        while True:
            user = user_queue.get(timeout=1)
            print 'slave %s get one user from the queue' % name
            database.put_user_in_db(user)
            gevent.sleep(0)
    except Empty:
        print 'slave %s is dead' % name


def master():
    topic.get_questions()


gevent.spawn(master).join()
question_group = Group()
answer_group = Group()
user_group = Group()
question_group.map(question_slave, xrange(100))
answer_group.map(answer_slave, xrange(100))
user_group.map(user_slave, xrange(100))
