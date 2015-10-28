# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from DataBase import DataBase
from User import User


def main():
    user = 'root'
    host = 'localhost'
    password = ''
    dbname = 'zhihu'
    database = DataBase(user, host, password, dbname)
    user_msg = User("http://www.zhihu.com/people/Fooying")
    database.put_user_in_db(user_msg)

if __name__ == '__main__':
    main()
