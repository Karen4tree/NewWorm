# -*- coding: utf-8 -*-_

from database_operation.DataBase import DataBase
from zhihu_api.Topic import Topic
from zhihu_api import questionBloom, userBloom, userQueue, answerBloom, topicBloom, topicQueue
# http://stackoverflow.com/questions/5318936/python-multiprocessing-pool-lazy-iteration
import multiprocessing as mp
import itertools

__author__ = 'ZombieGroup'

topic = Topic("https://www.zhihu.com/topic/19554927")


def spider(questions):
    for question in questions:
        questionBloom.insert_element(question.get_question_id())
        DataBase.put_question_in_db(question)

        for follower in question.get_followers():
            if not userBloom.is_element_exist(follower.get_user_id()):
                userBloom.insert_element(follower.get_user_id())
                userQueue.put(follower)
                DataBase.put_user_in_db(follower)
            DataBase.put_follow_question_in_db(question, follower)

        for topic in question.get_topics():
            if not topicBloom.is_element_exist(topic.get_topic_id()):
                topicBloom.insert_element(topic.get_topic_id())
            DataBase.put_question_topic_in_db(question, topic)

        for answer in question.get_answers():
            if not answerBloom.is_element_exist(answer.get_answer_id()):
                answerBloom.insert_element(answer.get_answer_id())
            DataBase.put_answer_in_db(answer)
            for user in answer.get_upvoters():
                if not userBloom.is_element_exist(user.get_user_id()):
                    userBloom.insert_element(user.get_user_id())
                DataBase.put_vote_in_db(answer, user)


if __name__ == '__main__':
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19736651")
    DataBase.put_topic_in_db(topic)
    topicBloom.insert_element(topic.get_topic_id())
    go = topic.get_questions()
    N = 20
    while True:
        g2 = p.map(spider(itertools.islice(go, N)))
        if not g2:
            break
