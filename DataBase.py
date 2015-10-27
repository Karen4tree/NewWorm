# -*- coding: utf-8 -*-_
_author__ = 'ZombieGroup'

import MySQLdb


class ConnectItem:
    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.user = user
        self.host = host
        self.password = password
        self.dbname = dbname

    def get_item(self):
        return self.user, self.host, self.password, self.dbname


class DataBase:
    def __init__(self, user=None, host=None, password=None, dbname=None):
        self.connect = MySQLdb.connect(host, user, password, dbname, port = 3306)

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

        followers = user.get_followers()
        followees = user.get_followees()
        asks = user.get_asks()
        answers = user.get_answers()

        cursor.execute("insert into Users values (%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%s,%s,%s,%s,%s)" % (
            user_id, follower_num, followee_num, vote_num, thanks_num, ask_num, answer_num, article_num, collection_num,
            following_topic_num, following_column_num, education, education_extra, location, business, position,
            employment))

        for follower in followers:
            follower_id = follower.get_user_id()
            cursor.execute("insert into Follow_User values (%s, %s)" % (follower_id, user_id))
        for followee in followees:
            followee_id = followee.get_user_id()
            cursor.execute("insert into Follow_User values (%s, %s)" % (user_id, followee_id))
        for question in asks:
            question_id = question.get_question_id()
            cursor.execute("update Questions set asker_ID=%s where question_ID=%s" % (user_id, question_id))
        for answer in answers:  # this maybe don't need to be here
            answer_id = answer.get_answer_id()
            cursor.execute("update Answers set author_ID=%s where answer_ID=%s" % (user_id, answer_id))
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
