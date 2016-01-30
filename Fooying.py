# -*- coding: utf-8 -*-_

# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import itertools
import multiprocessing as mp

from database_operation.DataBase import DataBase
from worm_status import Worm_status
from zhihu_api.Logging import Logging
from zhihu_api.Topic import Topic
from zhihu_api.User import User

__author__ = 'ZombieGroup'

userBloom = Worm_status.read_status("userBloom")
questionBloom = Worm_status.read_status("questionBloom")
answerBloom = Worm_status.read_status("answerBloom")
topicBloom = Worm_status.read_status("topicBloom")
articleBloom = Worm_status.read_status("articleBloom")
collumnBloom = Worm_status.read_status("collumnBloom")
commentBloom = Worm_status.read_status("commentBloom")

lock = mp.Lock()


def spider(question):
    lock.acquire()
    questionBloom.insert_element(question.get_question_id())
    Worm_status.record_status("questionBloom",questionBloom)
    lock.release()
    DataBase.put_question_in_db(question)

    Logging.info("Follower of question id %s" % question.get_question_id())
    for follower in question.get_followers():
        if not userBloom.is_element_exist(follower.get_user_id()):
            lock.acquire()
            userBloom.insert_element(follower.get_user_id())
            Worm_status.record_status("userBloom",userBloom)
            lock.release()
            DataBase.put_user_in_db(follower)
            for userfollower in follower.get_followers():
                if not userBloom.is_element_exist(userfollower.get_user_id()):
                    lock.acquire()
                    userBloom.insert_element(userfollower.get_user_id())
                    Worm_status.record_status("userBloom",userBloom)
                    lock.release()
                    DataBase.put_user_in_db(userfollower)
                DataBase.put_follow_user_in_db(follower, userfollower)
        DataBase.put_follow_question_in_db(question, follower)

    Logging.info("Topics of question id %s" % question.get_question_id())
    for topic in question.get_topics():
        if not topicBloom.is_element_exist(topic.get_topic_id()):
            lock.acquire()
            topicBloom.insert_element(topic.get_topic_id())
            Worm_status.record_status("topicBloom",topicBloom)
            lock.release()
        DataBase.put_question_topic_in_db(question, topic)

    Logging.info("Answers of question id %s" % question.get_question_id())
    for answer in question.get_answers():
        if not answerBloom.is_element_exist(answer.get_answer_id()):
            lock.acquire()
            answerBloom.insert_element(answer.get_answer_id())
            Worm_status.record_status("answerBloom",answerBloom)
            lock.release()
        if not userBloom.is_element_exist(answer.get_author_id()):
            DataBase.put_user_in_db(User("http://www.zhihu.com/people/%s" % answer.get_author_id()))
            lock.acquire()
            userBloom.insert_element(answer.get_author_id())
            Worm_status.record_status("userBloom",userBloom)
            lock.release()
        DataBase.put_answer_in_db(answer)
        for user in answer.get_upvoters():
            if not userBloom.is_element_exist(user.get_user_id()):
                lock.acquire()
                userBloom.insert_element(user.get_user_id())
                Worm_status.record_status("userBloom",userBloom)
                lock.release()
            DataBase.put_vote_in_db(answer, user)

            # time.sleep(0)


if __name__ == '__main__':
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19736651")
    DataBase.put_topic_in_db(topic)
    topicBloom.insert_element(topic.get_topic_id())
    Worm_status.record_status("topicBloom",topicBloom)
    go = topic.get_questions()
    N = 20
    while True:
        try:
            p.map(spider, itertools.islice(go, N), chunksize = 100)
        except TypeError:
            continue
