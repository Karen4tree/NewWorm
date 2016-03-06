#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy
from numpy import *
from pandas import DataFrame,Series
from database_operation.ReadData import ReadData
class OpinionStrip:
    """
    This is used to caculate the width of strips and the transition lines between Topics
    """
    def __init__(self,topic):
        self.width = 0
        self.graph = DataFrame(columns = ['topic_U','topic_V','Similarity'])
        self.topic = topic
        cursor = ReadData.connect.cursor()
        self.keywords = cursor.execute('select ')


    def width_of_strip(self):