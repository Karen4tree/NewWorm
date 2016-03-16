#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy
from numpy import *
from pandas import DataFrame, Series
import pandas.io.sql as pandasql
from database_operation.ReadData import ReadData


class TopicSimilarity:
    """
    This is used to measure the similarity among Topics, which is calculated by the distance on the graph
    """

    def __init__(self):
        self.topic_relation_frame = pandasql.read_sql("SELECT * FROM Topic_Topics", ReadData.connect)
        self.topic_list = pandasql.read_sql("SELECT topic_id FROM Topic", ReadData.connect)
        self.topic_graph = {}
        self.topic_relation_matirx = DataFrame(index = self.topic_list["topic_id"],
                                               columns = self.topic_list["topic_id"])
        self.init_graph()
        self.init_matrix()

    def init_graph(self):
        """
        The Graph is described by a disc:
        graph = {
        'A':['B','C'],
        'B':['D']
        }
        """
        for item in self.topic_relation_frame:
            if item['father_topic_id'] in self.topic_graph:
                self.topic_graph[item['father_topic_id']] = []
            self.topic_graph[item['father_topic_id']].append(item['child_topic_id'])

    def shortest_path(self, start, end, path=None):
        """
        :param start: the beganing of path
        :param end: the end of path
        :param path: existing path before start
        :return: the path,looks like(['A','B','C'])
        """
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return path
        if not self.topic_graph.has_key(start):
            return None
        shortest = None
        for node in self.topic_graph[start]:
            if node not in path:
                newpath = self.shortest_path(self.topic_graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def init_matrix(self):
        """
        A Pandas DataFrame, with both index and columns are Series of User, each item is the simularity of topics.
        """
        for index in self.topic_list:
            for column in self.topic_list:
                if self.shortest_path(column,index) is not None:
                    self.topic_relation_matirx[column][index] = len(self.shortest_path(column,index))-1
                    self.topic_relation_matirx[index][column] = len(self.shortest_path(column,index))-1

    def get_similarity(self,topic_u,topic_v):
        """
        get the similarity between two topic
        :param topic_u: id of topic_u
        :param topic_v: id of topic_v
        :return: the value of similarity
        """
        return self.topic_relation_matirx[topic_u][topic_v]
