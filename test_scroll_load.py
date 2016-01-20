# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from zhihu_api.User import User


def test_user(user_url):
    user = User(user_url)
    followers = user.get_followers()
    print followers


def main():
    user_url = "http://www.zhihu.com/people/JK.Ryan"
    test_user(user_url)


if __name__ == '__main__':
    main()
