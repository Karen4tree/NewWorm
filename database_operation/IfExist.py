# -*- coding: utf-8 -*-_
import MySQLdb
__author__ = 'ZombieGroup'

class IfExist:

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
    def user_exist(cls, user):
        connect = cls.connect
        cursor = connect.cursor()
        cursor.execute('select count(*) from Users where user_id LIKE "%s"' % user.get_user_id())
        r = cursor.fetchone()
        if r[0] != 0:
            return True
        else:
            return False

    @classmethod
    def question_exist(cls, question):
        connect = cls.connect
        cursor = connect.cursor()
        cursor.execute('select count(*) from Questions where question_id = %s' % question.get_question_id())
        r = cursor.fetchone()
        if r[0] != 0:
            return True
        else:
            return False

    @classmethod
    def random_users(cls):
        connect = cls.connect
        cursor = connect.cursor()
        cursor.execute('SELECT user_id FROM Users ORDER BY RAND() LIMIT 80')
        result = cursor.fetchall()
        return result

