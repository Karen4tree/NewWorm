# -*- coding: utf-8 -*-_

from database_operation.DataBase import DataBase
from zhihu_api.Topic import Topic
from zhihu_api.User import User
from zhihu_api.Logging import Logging
from zhihu_api.BloomFliter import BloomFilter
# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import multiprocessing as mp
import itertools
import time

__author__ = 'ZombieGroup'

ERROR_RATE = 0.05
ITEM_NUM = 10000

userBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
questionBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
answerBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
topicBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
articleBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
collumnBloom = BloomFilter(ERROR_RATE, ITEM_NUM)
commentBloom = BloomFilter(ERROR_RATE, ITEM_NUM)

#lock = mp.Lock()

def spider(question):
    #lock.acquire()
    questionBloom.insert_element(question.get_question_id())
    #lock.release()
    DataBase.put_question_in_db(question)

    Logging.info("Follower of question id %s" % question.get_question_id())
    for follower in question.get_followers():
        if not userBloom.is_element_exist(follower.get_user_id()):
            #lock.acquire()
            userBloom.insert_element(follower.get_user_id())
            #lock.release()
            DataBase.put_user_in_db(follower)
            for userfollower in follower.get_followers():
                if not userBloom.is_element_exist(userfollower.get_user_id()):
                    #lock.acquire()
                    userBloom.insert_element(userfollower.get_user_id())
                    #lock.release()
                    DataBase.put_user_in_db(userfollower)
                DataBase.put_follow_user_in_db(follower,userfollower)
        DataBase.put_follow_question_in_db(question, follower)

    Logging.info("Topics of question id %s" % question.get_question_id())
    for topic in question.get_topics():
        if not topicBloom.is_element_exist(topic.get_topic_id()):
            #lock.acquire()
            topicBloom.insert_element(topic.get_topic_id())
            #lock.release()
        DataBase.put_question_topic_in_db(question, topic)

    Logging.info("Answers of question id %s"%question.get_question_id())
    for answer in question.get_answers():
        if not answerBloom.is_element_exist(answer.get_answer_id()):
            #lock.acquire()
            answerBloom.insert_element(answer.get_answer_id())
            #lock.release()
        if not userBloom.is_element_exist(answer.get_author_id()):
            DataBase.put_user_in_db(User("http://www.zhihu.com/people/%s" % answer.get_author_id()))
            #lock.acquire()
            userBloom.insert_element(answer.get_author_id())
            #lock.release()
        DataBase.put_answer_in_db(answer)
        for user in answer.get_upvoters():
            if not userBloom.is_element_exist(user.get_user_id()):
                #lock.acquire()
                userBloom.insert_element(user.get_user_id())
                #lock.release()
            DataBase.put_vote_in_db(answer, user)

    #time.sleep(0)


if __name__ == '__main__':
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19736651")
    DataBase.put_topic_in_db(topic)
    topicBloom.insert_element(topic.get_topic_id())
    go = topic.get_questions()
    N = 20
    while True:
        try:
            p.map(spider, itertools.islice(go, N),chunksize = 100)
        except TypeError:
            continue
