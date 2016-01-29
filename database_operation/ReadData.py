# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

import MySQLdb

class ReadData:

    connect = MySQLdb.connect('localhost', 'root', '',
                              'zhihu', port=3306, charset='utf8')

    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.connect = MySQLdb.connect(
            host, user, password, dbname, port=3306, charset='utf8')

    @classmethod
    def read_from_user(cls, user_id):
        connect = cls.connect
        cursor = connect.cursor()
        cursor.execute('select * from Users where user_id=%s' % user_id)
        return cursor.fetchone()

    @classmethod
    def followers_of_user_question(cls, user_id):
        connect = cls.connect
        cursor = connect.cursor()

        cursor.execute(
            'select follower_id from Follow_Question where question_id in (select question_id from Questions where '
            'asker_id=%s)' % user_id)
        result = cursor.fetchall()
        return result

    @classmethod
    def followers_of_user(cls, user_id):
        connect = cls.connect
        cursor = connect.cursor()

        cursor.execute(
            'select followee_id from Follow_User where follower_id=%s' % user_id)
        result = cursor.fetchall()
        return result

    @classmethod
    def voters_of_user_answer(cls, user_id):
        connect = cls.connect
        cursor = connect.cursor()
        cursor.execute('select voter_id from Vote_Answer where answer_id in (select answer_id from Answers where '
                       'author_id=%s)' % user_id)

        result = cursor.fetchall()
        return result

    @classmethod
    def random_users(cls):
        connect = cls.connect
        cursor = connect.cursor()
        cursor.execute('SELECT user_id FROM Users ORDER BY RAND() LIMIT 80')
        result = cursor.fetchall()
        return result

    # 暂时用不到
    @classmethod
    def read_unreached_users(cls, num):
        connect = cls.connect
        # TODO:数据库中额外的标签表示已访问
        cursor = connect.cursor()
        cursor.execute(
            'select user_id from Users where reached_flag is False limit %s' % num)  # 字段尚未定义
        result = cursor.fetchall()
        return result
