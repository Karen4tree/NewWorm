#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.User import User
from database_operation.DataBase import DataBase


def store(user):
    if user is not None:
        print user.get_user_id()
        try:
            DataBase.put_user_in_db(user)
            for item in user.get_followers():
                store(item)
                DataBase.put_follow_user_in_db(user,item)
        except:
            pass


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(1000000)
    startUser = User("http://www.zhihu.com/people/tian-yuan-dong")
    store(startUser)
