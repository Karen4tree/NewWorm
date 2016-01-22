# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from database_operation.DataBase import DataBase
from zhihu_api.User import User
from zhihu_api.Topic import Topic

from database_operation.ReadData import ReadData
from zhihu_api.Question import Question


def main():
    #user_msg = User(u"http://www.zhihu.com/people/Fooying")
    topic = Topic("http://www.zhihu.com/topic/19553732")
    DataBase.put_topic_in_db(topic)
    #question_msg = Question(u"http://www.zhihu.com/question/31918396")
    #DataBase.put_user_in_db(user_msg)
    # database.put_follow_user_in_db(user_msg)

    # for user in user_msg.get_followers():
    #   database.put_follow_user_in_db(user)

    # database.put_user_answer_in_db(user_msg)
    # database.put_user_ask_in_db(user_msg)

    # database.put_question_in_db(question_msg)


if __name__ == '__main__':
    main()
