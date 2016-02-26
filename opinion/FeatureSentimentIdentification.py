#!/usr/bin/env python
# -*- coding:utf-8 -*-

from LinguisticProcessing import LinguisticProcessing

class FeatureSentimentIdentifier:
    def __init__(self, raw_text):
        self.sentence_trees = LinguisticProcessing(raw_text).sent_tree
        self.tuples = {'timestamp': None, 'Text': None, 'List_of_Feature_Sentiments': [], 'Overall_sentiment': None,
                       'Bag_of_context_words': None}
        self.contex_identifier = {'Features': [], 'Adjectives': [], 'Verbs': []}

    def sentiment_word_detection(self, sentiment_word_disc):
        pass

    def feature_identification(self):
        pos_tagged = self.sentence_trees.pos()
        for pair in pos_tagged:
            if pair[-1] == 'NN' or 'NR' or 'NT':
                self.contex_identifier['Features'].append(pair[0])


    def pattern_extracting(self, L_t, L_s):
        """
        Function to extract candidate patterns for individual features
        :param L_t: List of ordered time stamps(for one feature)
        :param L_s: Corresponding list of sentiment values multiplied with certainty values
        """
        L_d =
        d_avg =
        L_p =
        p_tmp =


    def sentiment_to_feature_attribution(self):
        pass

    def sentiment_for_whole_text(self):
        pass

    def feature_sentiments(self):
        pass
