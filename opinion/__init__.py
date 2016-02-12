#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pandas import DataFrame
from ReadData import DataReader
from LinguisticProcessing import LinguisticProcessing
"""
datafile: location of the file storing (topics,text,timestamp,author) pairs.
           text timestamp and author are wrapped separately by {}.
           topics are formatted as hash-tags.
           answers and comments share same topics with question.
"""
"""file_path = 'path to file'
pairs = DataReader(file_path)

predifined_negation_disc = ['']

dataframe = DataFrame(pairs.data, columns=['time', 'text', 'topics', 'author', 'opinion'])
textseries = dataframe.text
timeseries = dataframe.time
authorseries = dataframe.author
topicstringseries = dataframe.topics

linguistic_process = LinguisticProcessing(text for text in textseries)
"""

