#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy
from numpy import *
from pandas import DataFrame,Series
import pandas.io.sql as pandasql
from database_operation.ReadData import ReadData
class OpinionStrip:
    """
    This is used to calculate the width of strips and the transition lines between Topics.
    For output, we use a tuple of {'time_slice':[],'width':[]} to show the strip, such tuple should be converted into pandas.
    """
    def __init__(self,topic,time_slice):
        self.width = 0
        self.graph = DataFrame(columns = ['topic_U','topic_V','Similarity'])
        self.topic = topic
        self.time_slice = time_slice
        self.connect = ReadData.connect

    def width_of_strip(self,t):
        frame = pandasql.read_sql('select answer_id,author_id from Answers WHERE '
                                  '(post_time = %s and question_id in '
                                  '(select question_id from Question_Topics WHERE topic_id = %s))'%
                                  (t,self.topic.get_topic_id()), self.connect)