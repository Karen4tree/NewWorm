# -*- coding: utf-8 -*-_
_author__ = 'ZombieGroup'

import MySQLdb

# TODO: 改成类方法
class ReadData:
    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.connect = MySQLdb.connect(host, user, password, dbname, port = 3306, charset = 'utf8')

    def read_from_user(self, user_id):
        connect = self.connect
        cursor = connect.cursor()
        cursor.execute('select * from Users where user_id="%s"' % user_id)
        return cursor.fetchone()

    def followers_of_user_question(self, user_id):
        connect = self.connect
        cursor = connect.cursor()

        cursor.execute(
            'select follower_id from Follow_Question where question_id in (select question_id from Question where '
            'asker_id="%s")' % user_id)
        return cursor.fetchall()

    def followers_of_user(self, user_id):
        connect = self.connect
        cursor = connect.cursor()

        cursor.execute('select follower_id from Follow_User where followee_id="%s"' % user_id)

        return cursor.fetchall()

    def voters_of_user_answer(self, user_id):
        connect = self.connect
        cursor = connect.cursor()

        cursor.execute(
            'select voter_id from Vote_Answer where answer_id in (select answer_id from Answers where '
            'author_id="%s")' % user_id)

        return cursor.fetchall()
