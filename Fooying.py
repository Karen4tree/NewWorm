# -*- coding: utf-8 -*-_

from database_operation.DataBase import DataBase
from zhihu_api.Topic import Topic
from zhihu_api import *

__author__ = 'ZombieGroup'
# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import multiprocessing as mp
import itertools


def spider(question):
    print question.get_question_id()
    DataBase.put_question_in_db(question)
    for answer in question.get_answers():
        DataBase.put_answer_in_db(answer)
        DataBase.put_vote_in_db(answer)


if __name__ == '__main__':
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19554927")  # 网络安全
    DataBase.put_topic_in_db(topic)
    go = topic.get_questions()
    N = 20
    while True:
        g2 = p.map(f, itertools.islice(go, N))
        if not g2:
            break
