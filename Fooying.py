# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from DataBase import DataBase
from Topic import Topic

# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import multiprocessing as mp
import itertools

user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
db = DataBase(user, host, password, dbname)

def spider(question):
    print question.get_question_id()
    db.put_question_in_db(question)
    for answer in question.get_answers():
        db.put_answer_in_db(answer)
        db.put_vote_in_db(answer)


if __name__ == '__main__':
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19554927")# 网络安全
    db.put_topic_in_db(topic)
    go = topic.get_questions()
    N = 20
    while True:
        g2 = p.map(f, itertools.islice(go, N))
        if not g2:
            break