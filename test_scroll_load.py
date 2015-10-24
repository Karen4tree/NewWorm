# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from User import User
from Questions import Questions
from Answers import Answers
from Topics import Topics
from Collections import Collections
from Article import Article
from ScrollLoader import ScrollLoader


def test_user(user_url):
    user = User(user_url)
    followers = user.get_followers()
    print followers


def main():
    user_url = "http://www.zhihu.com/people/JK.Ryan"
    test_user(user_url)


if __name__ == '__main__':
    main()
