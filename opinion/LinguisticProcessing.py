#!/usr/bin/env python
# -*- coding:utf-8 -*-
import nltk
from nltk.tag import StanfordPOSTagger


class LinguisticProcessing:
    def __init__(self, raw_text):
        self.pos_tager = StanfordPOSTagger('chinese-nodistsim.tagger')
        self.raw = raw_text
        self.pos_teg =self.tag_raw_file()

    def divide(self):
        # Divide sentences in Chinese into words
        pass

    def tag_raw_file(self, file = None):
        if file is None:
            return self.pos_tager.tag(self.divide())
        else:
            return self.pos_tager.tag(file)

    def mbf_reduction(self):
        pass

    def identification_negation_scopes(self):
        pass
