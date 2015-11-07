# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from User import User
from DataBase import DataBase
from Queue import Queue

user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
db = DataBase(user, host, password, dbname)
queue = Queue()

def run(queue):
    while not queue.empty():
        user = queue.get()
        for follower in user.get_followers():
            queue.put(follower)
        for answer in user.get_answers():
            for voter in answer.get_upvoters():
                queue.put(voter)
            db.put_answer_in_db(answer)
            db.put_vote_in_db(answer)

        get_info(user)

def get_info(user):
    db.put_user_in_db(user)
    db.put_follow_user_in_db(user)
    db.put_user_ask_in_db(user)

if __name__ == '__main__':
    user = User(u"http://www.zhihu.com/people/Fooying")
    queue.put(user)
    run(queue)
