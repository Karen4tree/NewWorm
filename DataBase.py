# -*- coding: utf-8 -*-_
_author__ = 'ZombieGroup'

import MySQLdb


class DataBase:

    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.connect = MySQLdb.connect(
            host, user, password, dbname, port=3306, charset='utf8')

    def put_user_in_db(self, user):
        connect = self.connect
        cursor = connect.cursor()

        user_id = user.get_user_id()
        location = user.get_location()
        business = user.get_business()
        employment = user.get_employment()
        position = user.get_position()
        education = user.get_education()
        education_extra = user.get_education_extra()

        follower_num = user.get_follower_num()
        followee_num = user.get_followee_num()
        thanks_num = user.get_thanks_num()
        vote_num = user.get_vote_num()
        ask_num = user.get_ask_num()
        answer_num = user.get_answer_num()
        article_num = user.get_articles_num()
        collection_num = user.get_collection_num()
        following_topic_num = user.get_following_topic_num()
        following_column_num = user.get_following_column_num()

        asks = user.get_asks()
        answers = user.get_answers()

        value = (user_id, follower_num, followee_num, vote_num, thanks_num, ask_num, answer_num, article_num, collection_num,
                 following_topic_num, following_column_num, education, education_extra, location, business, position, employment)
        cursor.execute(
            '''insert into Users values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', value)

        cursor.close()
        connect.commit()

    def put_follow_user(self, user):
        connect = self.connect
        cursor = connect.cursor()
        for follower in user.get_followers():
            follower_id = follower.get_user_id()
            if cursor.execute('''select user_ID from users where user_ID=%s''' % follower_id) is not follower_id:
                self.put_user_in_db(follower)
            cursor.execute('''insert into follow_user values (%s, %s)''',
                           (follower_id, user.get_user_id()))
        cursor.close()
        connect.commit()

    def alter_user_in_db(self):
        connect = self.connect
        cursor = connect.cursor()
        # TODO: properties to be changed
        cursor.excute()
        # TODO: write SQL statements in the ()
        cursor.close()
        connect.commit()
