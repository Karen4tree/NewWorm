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
            question = question_queue.get()
            print 'question slave %s get one question from the queue' % name
            database.put_question_in_db(question)
            question.get_followers()
            question.get_answers()
    except Empty:
        print 'question slave %s is dead' % name
        gevent.sleep(0)


def answer_slave(name):
    try:
        while True:
            answer = answer_queue.get()
            print 'answer slave %s get one answer from the queue' % name
            database.put_answer_in_db(answer)
            answer.get_upvoters()
    except Empty:
        print 'answer slave %s is dead' % name
        gevent.sleep(0)


def user_slave(name):
    try:
        while True:
            user = user_queue.get()
            print 'user slave %s get one user from the queue' % name
            database.put_user_in_db(user)
            user.get_followers()
            user.get_answers()
            user.get_asks()
    except Empty:
        print 'user slave %s is dead' % name
        gevent.sleep(0)


def master(name):
    print 'master %s' % name
    topic.get_questions()

masters = [gevent.spawn(master, i) for i in xrange(10)]
users = [gevent.spawn(user_slave, i) for i in xrange(100)]
questions = [gevent.spawn(question_slave, i) for i in xrange(100)]
answers = [gevent.spawn(answer_slave, i) for i in xrange(100)]
gevent.joinall(masters + users + questions + answers)
