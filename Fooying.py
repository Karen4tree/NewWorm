# -*- coding: utf-8 -*-_

# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import itertools
import multiprocessing as mp

from spider import read_status,record_status
from database_operation.DataBase import DataBase
from zhihu_api.Logging import Logging
from zhihu_api.Topic import Topic

__author__ = 'ZombieGroup'

userBloom = read_status("userBloom")
questionBloom = read_status("questionBloom")
answerBloom = read_status("answerBloom")
topicBloom = read_status("topicBloom")
articleBloom = read_status("articleBloom")
collumnBloom = read_status("collumnBloom")
commentBloom = read_status("commentBloom")

userlock = mp.Lock()
questionlock = mp.Lock()
answerlock = mp.Lock()
topiclock = mp.Lock()
articlelock = mp.Lock()
collumnlock = mp.Lock()
commentlock = mp.Lock()


def spider(question):
    if not questionBloom.is_element_exist(question.get_question_id()):
        questionlock.acquire()
        questionBloom.insert_element(question.get_question_id())
        record_status("questionBloom", questionBloom)
        questionlock.release()
        DataBase.put_question_in_db(question)
        Logging.info("Topics of question id %s" % question.get_question_id())
        for topictag in question.get_topics():
            if not topicBloom.is_element_exist(topictag.get_topic_id()):
                DataBase.put_topic_in_db(topictag)
                topiclock.acquire()
                topicBloom.insert_element(topictag.get_topic_id())
                record_status("topicBloom", topicBloom)
                topiclock.release()
            DataBase.put_question_topic_in_db(question, topictag)

        Logging.info("Answers of question id %s" % question.get_question_id())
        for answer in question.get_answers():
            if not answerBloom.is_element_exist(answer.get_answer_id()):
                answerlock.acquire()
                answerBloom.insert_element(answer.get_answer_id())
                record_status("answerBloom", answerBloom)
                answerlock.release()
            if not userBloom.is_element_exist(answer.get_author_id()):
                DataBase.put_user_in_db(answer.get_author())
                userlock.acquire()
                userBloom.insert_element(answer.get_author_id())
                record_status("userBloom", userBloom)
                userlock.release()
            DataBase.put_answer_in_db(answer)
            for user in answer.get_upvoters():
                if not userBloom.is_element_exist(user.get_user_id()):
                    DataBase.put_user_in_db(user)
                    userlock.acquire()
                    userBloom.insert_element(user.get_user_id())
                    record_status("userBloom", userBloom)
                    userlock.release()
                DataBase.put_vote_in_db(answer, user)

        Logging.info("Follower of question id %s" % question.get_question_id())
        for follower in question.get_followers():
            if not userBloom.is_element_exist(follower.get_user_id()):
                DataBase.put_user_in_db(follower)
                userlock.acquire()
                userBloom.insert_element(follower.get_user_id())
                record_status("userBloom", userBloom)
                userlock.release()
            DataBase.put_follow_question_in_db(question, follower)
    else:
        Logging.debug("Exist Question")
        #time.sleep(0.1)


def user_spider(user):
    for follower in user.get_followers():
        DataBase.put_user_in_db(follower)
        DataBase.put_follow_user_in_db(user,follower)


if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(1000000)
    """THREADS = 10
    p = mp.Pool(processes = THREADS)
    topic = Topic("http://www.zhihu.com/topic/19554927")
    if not topicBloom.is_element_exist(topic.get_topic_id()):
        topicBloom.insert_element(topic.get_topic_id())
        record_status("topicBloom", topicBloom)
    DataBase.put_topic_in_db(topic)
    go = topic.get_questions()
    num = topic.get_question_num()
    while num >= 0:
        try:
            p.map(spider,itertools.islice(go,20))
        except AttributeError:
            pass
        finally:
            num -= 20"""
    from database_operation.ReadData import ReadData
    from database_operation.IfExist import IfExist
    from zhihu_api.User import User
    for i in range(10000):
        users = ReadData.read_all_user()
        for user in users:
            user_id = str(user[0])
            if not IfExist.user_exist_in_follow_user(user_id):
                user_spider(User('http://www.zhihu.com/people/'+user_id))

