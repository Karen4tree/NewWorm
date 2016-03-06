#!/usr/bin/env python
# -*- coding:utf-8 -*-
from numpy import *
import pandas.io.sql as pandasql
from pandas import DataFrame,Series
from database_operation.ReadData import ReadData


class UserInfluence:
    """
    This class is used to calculate the influence of users on Zhihu
    The algorithm used here is inspired by Page Ranking and Klaut
    """
    def __init__(self):
        self.user_frame = pandasql.read_sql('select user_id,thanks_num,agrees_num from Users', ReadData.connect)
        self.user_follow = pandasql.read_sql('select * from Follow_User', ReadData.connect)
        self.user_series = self.user_frame.user_id
        self.user_frame = self.user_frame.rename(index = self.user_series)
        self.user_matrix = DataFrame(index = self.user_series,columns = self.user_series)
        self.epsilon = 0.87

    def matrix_init(self):
        self.user_matrix=self.user_matrix.fillna(0)
        for relation in self.user_follow:
            power = self.user_frame['thanks_num'][relation.follower_id]+self.user_frame['agrees_num'][relation.follower_id]
            self.user_matrix[relation['follower_id']][relation['followee_id']] = power

        for column in self.user_matrix.columns:
            power_sum = sum(self.user_matrix[column])
            for item in self.user_matrix[column]:
                item = float(item)/float(power_sum)

    def iterate(self):
        m = self.user_matrix.values
        v = ones(len(m),dtype = float)
        v = v.reshape(len(v),1)
        tmp = None
        power_sum = sum(v)
        for item in v:
            item /= power_sum
        while v != tmp:
            tmp = v
            v = dot(m,v) * self.epsilon + (1-self.epsilon)
        self.user_frame['influence'] = Series(v)

    def write_to_db(self):
        cursor = ReadData.connect.cursor()
        cursor.execute('')

