#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pandas import DataFrame
from nltk.corpus import PlaintextCorpusReader
from ReadData import DataReader
"""
datafile: location of the file storing (topics,text,timestamp,author) pairs.
           text timestamp and author are wrapped separately by {}.
           topics are formatted as hash-tags.
           answers and comments share same topics with question.
"""
"""file_path = 'path to file'
pairs = DataReader(file_path)
dataframe = DataFrame(pairs.data, columns=['time', 'text', 'topics', 'author', 'opinion'])
textseries = dataframe.text
timeseries = dataframe.time
authorseries = dataframe.author
topicstringseries = dataframe.topics


wordlists = PlaintextCorpusReader("opinion/disc",'.*')
positive_words = wordlists.words(catagories for catagories in ['positive_comment','positive_feeling'])
negative_words = wordlists.words(catagories for catagories in ['negative_comment','negative_feeling'])"""
