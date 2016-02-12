#!/usr/bin/env python
# -*- coding:utf-8 -*-

class ContextIdentifier:
    def __init__(self,tagged_file):
        self.bag_of_context_words ={'Features':[],'Adjectives':[],'Verbs':[]}

class FeatureSentimentIdentifier:
    def __init__(self,tagged_file):
        self.tuples = {'timestamp': None,
                       'Text': None,
                       'List_of_Feature_Sentiments': [],
                       'Overall_sentiment': None,
                       'Bag_of_context_words': None}
        self.contex_identifier = ContextIdentifier(tagged_file)

    def sentiment_word_detection(self):

    def feature_identification(self):

    def sentiment_to_feature_attribution(self):

    def sentiment_for_whole_text(self):

    def feature_sentiments(self):