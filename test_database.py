# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from database_operation.DataBase import DataBase
from zhihu_api.User import User

from database_operation.ReadData import ReadData
from zhihu_api.Question import Question


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

    user_id = user_msg.get_user_id()
    print "follower of user"
    for follower_id in readdata.followers_of_user(user_id):
        print follower_id

    print "follower of user's question"
    for follower_id in readdata.followers_of_user_question(user_id):
        print follower_id

    print "voter of user's answer"
    for voter_id in readdata.voters_of_user_answer(user_id):
        print voter_id

    # database.put_user_in_db(user_msg)
    # database.put_follow_user_in_db(user_msg)

    # for user in user_msg.get_followers():
    #   database.put_follow_user_in_db(user)

    # database.put_user_answer_in_db(user_msg)
    # database.put_user_ask_in_db(user_msg)

    # database.put_question_in_db(question_msg)


if __name__ == '__main__':
    main()
