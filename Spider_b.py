# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from User import User
from DataBase import DataBase
from Queue import Queue


def wow(inituser):
    user = 'root'
    host = 'localhost'
    password = ''
    dbname = 'zhihu'
    db = DataBase(user, host, password, dbname)
    queue = Queue()
    queue.put(inituser)
    while not queue.empty():
        user = queue.get()

        for follower in user.get_followers():
            queue.put(follower)

        db.put_user_in_db(user)
        db.put_follow_user_in_db(user)
        db.put_user_ask_in_db(user)
        db.put_user_answer_in_db(user)


if __name__ == '__main__':
    user = User(u"http://www.zhihu.com/people/Fooying")
    wow(user)
