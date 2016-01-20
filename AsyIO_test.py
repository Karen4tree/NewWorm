# -*- coding: utf-8 -*-_

__author__ = 'ZombieGroup'

from zhihu_api.Topic import Topic
from zhihu_api.Question import Question
from database_operation.DataBase import DataBase
from zhihu_api import question_queue

from gevent.pool import Group
import gevent
from gevent.queue import Queue, Empty

topic = Topic("http://www.zhihu.com/topic/19554927")

mastergroup = Group()
slavegroup = Group()


def slave(name):
    while True:
        question = question_queue.get()
        print("slave %s get one question from queue" % name)
        DataBase.put_question_in_db(question)
        DataBase.put_question_topic_in_db(question)
        DataBase.put_follow_question_in_db(question)
        for answer in question.get_answers():
            DataBase.put_answer_in_db(answer)
            DataBase.put_vote_in_db(answer)
        gevent.sleep(0)


def master(name):
    print 'master %s' % name
    topic.get_questions()


mastergroup.map(master, xrange(3))
slavegroup.map(slave, xrange(100))
