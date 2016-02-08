# -*- coding: utf-8 -*-_

# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import itertools
import multiprocessing as mp
import time

from database_operation.DataBase import DataBase
from database_operation.IfExist import IfExist
from worm_status import Worm_status
from zhihu_api.Logging import Logging
from zhihu_api.Topic import Topic
from zhihu_api.User import User

__author__ = 'ZombieGroup'


def content_spider(question):
    if not IfExist.question_exist(question):
        DataBase.put_question_in_db(question)
        Logging.info("Topics of question id %s" % question.get_question_id())
        for topictag in question.get_topics():
            DataBase.put_topic_in_db(topictag)
            DataBase.put_question_topic_in_db(question, topictag)

        Logging.info("Answers of question id %s" % question.get_question_id())
        for answer in question.get_answers():
            DataBase.put_user_in_db(answer.get_author())
            DataBase.put_answer_in_db(answer)
            for user in answer.get_upvoters():
                if not IfExist.user_exist(user):
                    DataBase.put_user_in_db(user)
                DataBase.put_vote_in_db(answer, user)

        Logging.info("Follower of question id %s" % question.get_question_id())
        for follower in question.get_followers():
            DataBase.put_user_in_db(follower)
            DataBase.put_follow_question_in_db(question, follower)
    else:
        Logging.debug("Exist Question")


def user_spider(user):
    DataBase.put_user_in_db(user)
    for follower in user.get_followers():
        DataBase.put_user_in_db(follower)
        DataBase.put_follow_user_in_db(user,follower)


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(1000000)
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19736651")
    DataBase.put_topic_in_db(topic)
    go = topic.get_questions()
    N = 20
    while True:
        try:
            p.map(content_spider, itertools.islice(go, N))
        except TypeError:
            continue
        except AttributeError:
            continue
