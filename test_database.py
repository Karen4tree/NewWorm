# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from DataBase import DataBase
from User import User
from Question import Question


def main():
    user = 'root'
    host = 'localhost'
    password = ''
    dbname = 'zhihu'
    database = DataBase(user, host, password, dbname)
    user_msg = User(u"http://www.zhihu.com/people/Fooying")
    question_msg = Question(u"http://www.zhihu.com/question/31918396")
    # database.put_user_in_db(user_msg)
    database.put_follow_user_in_db(user_msg)
    # database.put_user_answer_in_db(user_msg)
    # database.put_user_ask_in_db(user_msg)
    # database.put_question_in_db(question_msg)
if __name__ == '__main__':
    main()
