# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from msg_from_web import User
from msg_from_web import Questions

def test_user(user_url):
    user = User(user_url)
    answer_num = user.get_answer_num()
    print answer_num
    ask_num = user.get_ask_num()
    print ask_num
    followee_num = user.get_followee_num()
    print followee_num
    follower_num = user.get_follower_num()
    print follower_num
    collection_num = user.get_collection_num()
    print collection_num
    thanks_num = user.get_thanks_num()
    print thanks_num
    vote_num = user.get_vote_num()
    print vote_num

#    asks = user.get_asks()
#    answers = user.get_answers()

def main():
    user_url = "http://www.zhihu.com/people/gioroulden"
    test_user(user_url)

if __name__ == '__main__':
    main()
