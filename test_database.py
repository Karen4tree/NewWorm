# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from DataBase import DataBase
from ReadData import ReadData
from User import User
from Question import Question


def main():
    user = 'root'
    host = 'localhost'
    password = ''
    dbname = 'zhihu'
    database = DataBase(user, host, password, dbname)
    readdata = ReadData(user, host, password, dbname)
    user_msg = User(u"http://www.zhihu.com/people/Fooying")
    question_msg = Question(u"http://www.zhihu.com/question/31918396")

    '''user_id, follower_num, followee_num, vote_num, thanks_num, ask_num, answer_num, article_num, collection_num, \
    following_topic_num, following_column_num, education, education_extra, location, business, position, employment =\
        readdata.read_from_user(
        user_msg.get_user_id())
    value = (
        user_id, follower_num, followee_num, vote_num, thanks_num, ask_num, answer_num, article_num, collection_num,
        following_topic_num, following_column_num, education, education_extra, location, business, position, employment)
    print value'''
    
    # database.put_user_in_db(user_msg)
    # database.put_follow_user_in_db(user_msg)

    # for user in user_msg.get_followers():
    #   database.put_follow_user_in_db(user)

    # database.put_user_answer_in_db(user_msg)
    # database.put_user_ask_in_db(user_msg)

    # database.put_question_in_db(question_msg)


if __name__ == '__main__':
    main()
