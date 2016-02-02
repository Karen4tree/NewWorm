#!/usr/bin/env python
# -*- coding:utf-8 -*-
from database_operation.ReadData import ReadData


class UserRelation:
    def __init__(self, user1, user2):
        self.user1 = user1.get_user_id()
        self.user2 = user2.get_user_id()
        self.user1_to_user2 = self.user2_to_user1 = self.strength = 0
        self.connect = ReadData.connect

    def is_mutual_follow_exist(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Follow_User WHERE followee_id in (%s,%s) and follower_id in (%s,%s)",
                       (self.user1, self.user2, self.user1, self.user2))
        result = cursor.fetchone()
        if result[0] is 2:
            return True
        else:
            return False

    def is_1_follow_2(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Follow_User where follower_id = %s AND followee_id = %s",
                       (self.user1, self.user2))
        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

    def is_2_follow_1(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Follow_User where follower_id = %s AND followee_id = %s",
                       (self.user2, self.user1))
        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

    def num_1_answer_2(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Answers WHERE author_id is %s and question_id "
                       "in (SELECT question_id from Questions WHERE asker_id is %s)", (self.user1, self.user2))
        return cursor.fetchone()[0]

    def num_2_answer_1(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Answers WHERE author_id is %s and question_id "
                       "in (SELECT question_id from Questions WHERE asker_id is %s)", (self.user2, self.user1))
        return cursor.fetchone()[0]

    def num_1_vote_2(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Vote_Answer WHERE voter_id is %s and answer_id in "
                       "(SELECT answer_id from Answers WHERE author_id is %s)", (self.user1, self.user2))
        return cursor.fetchone()[0]

    def num_2_vote_1(self):
        cursor = self.connect.cursor()
        cursor.execute("select count(*) from Vote_Answer WHERE voter_id is %s and answer_id in "
                       "(SELECT answer_id from Answers WHERE author_id is %s)", (self.user2, self.user1))
        return cursor.fetchone()[0]

    def caculate_strength(self):
        answerPower = 1
        votePower =1
        if self.is_1_follow_2():
            self.user1_to_user2 += 1
        if self.is_2_follow_1():
            self.user2_to_user1 += 1
        self.user1_to_user2 += self.num_1_answer_2()*answerPower + self.num_1_vote_2()*votePower
        self.user2_to_user1 += self.num_2_answer_1()*answerPower + self.num_2_vote_1()*votePower
        self.strength = self.user1_to_user2 + self.user2_to_user1
        
        return self.strength, self.user1_to_user2, self.user2_to_user1
