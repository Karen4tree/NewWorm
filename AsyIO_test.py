# -*- coding: utf-8 -*-_
from database_operation.DataBase import DataBase
from worm_status import Worm_status
from zhihu_api.Logging import Logging
from zhihu_api.Topic import Topic

import itertools
from gevent.pool import Pool

userBloom = Worm_status.read_status("userBloom")
questionBloom = Worm_status.read_status("questionBloom")
answerBloom = Worm_status.read_status("answerBloom")
topicBloom = Worm_status.read_status("topicBloom")
articleBloom = Worm_status.read_status("articleBloom")
collumnBloom = Worm_status.read_status("collumnBloom")
commentBloom = Worm_status.read_status("commentBloom")

__author__ = 'ZombieGroup'


def spider(question):
    if not questionBloom.is_element_exist(question.get_question_id()):
        questionBloom.insert_element(question.get_question_id())
        Worm_status.record_status("questionBloom", questionBloom)
        DataBase.put_question_in_db(question)
        Logging.info("Topics of question id %s" % question.get_question_id())
        for topictag in question.get_topics():
            if not topicBloom.is_element_exist(topictag.get_topic_id()):
                DataBase.put_topic_in_db(topictag)
                topicBloom.insert_element(topictag.get_topic_id())
                Worm_status.record_status("topicBloom", topicBloom)
            DataBase.put_question_topic_in_db(question, topictag)

        Logging.info("Answers of question id %s" % question.get_question_id())
        for answer in question.get_answers():
            if not answerBloom.is_element_exist(answer.get_answer_id()):
                answerBloom.insert_element(answer.get_answer_id())
                Worm_status.record_status("answerBloom", answerBloom)
            if not userBloom.is_element_exist(answer.get_author_id()):
                DataBase.put_user_in_db(answer.get_author())
                userBloom.insert_element(answer.get_author_id())
                Worm_status.record_status("userBloom", userBloom)
            DataBase.put_answer_in_db(answer)
            for user in answer.get_upvoters():
                if not userBloom.is_element_exist(user.get_user_id()):
                    DataBase.put_user_in_db(user)
                    userBloom.insert_element(user.get_user_id())
                    Worm_status.record_status("userBloom", userBloom)
                DataBase.put_vote_in_db(answer, user)

        Logging.info("Follower of question id %s" % question.get_question_id())
        for follower in question.get_followers():
            if not userBloom.is_element_exist(follower.get_user_id()):
                DataBase.put_user_in_db(follower)
                userBloom.insert_element(follower.get_user_id())
                Worm_status.record_status("userBloom", userBloom)
            DataBase.put_follow_question_in_db(question, follower)
    else:
        Logging.debug("Exist Question")

p = Pool(size = 20)
topic = Topic("http://www.zhihu.com/topic/19554927")
if not topicBloom.is_element_exist(topic.get_topic_id()):
    topicBloom.insert_element(topic.get_topic_id())
    Worm_status.record_status("topicBloom", topicBloom)
DataBase.put_topic_in_db(topic)
go = topic.get_questions()
num = topic.get_question_num()
while num:
    p.map(spider,itertools.islice(go,20))
    num -= 20
