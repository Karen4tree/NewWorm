#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __init__ import timeseries
from LinguisticProcessing import LinguisticProcessing


class ContextIdentifier:
    def __init__(self, s_tree):
        self.bag_of_context_words = {'Features': [], 'Adjectives': [], 'Verbs': []}


class FeatureSentimentIdentifier:
    def __init__(self, raw_text):
        self.sentence_trees = LinguisticProcessing(raw_text).sent_tree
        self.tuples = {'timestamp': None, 'Text': None, 'List_of_Feature_Sentiments': [], 'Overall_sentiment': None,
                       'Bag_of_context_words': None}
        self.contex_identifier = ContextIdentifier(self.sentence_trees)

    def sentiment_word_detection(self, sentiment_word_disc):
        pass

    def feature_identification(self):
        candidate = []
        pos_tagged = self.sentence_trees.pos()
        for pair in pos_tagged:
            if pair[-1] == 'NN' or 'NR' or 'NT':
                candidate.append(pair[0])

    def pattern_extracting(self, L_t, L_s):
        """
        Function to extract candidate patterns for individual features
        :param L_t: List of ordered time stamps(for one feature)
        :param L_s: Corresponding list of sentiment values multiplied with certainty values
        """
        pass

    def sentiment_to_feature_attribution(self):
        pass

    def sentiment_for_whole_text(self):
        pass

    def feature_sentiments(self):
        pass
