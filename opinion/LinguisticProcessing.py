#!/usr/bin/env python
# -*- coding:utf-8 -*-
import nltk
from nltk.tag import StanfordPOSTagger
from nltk.tokenize.stanford_segmenter import StanfordSegmenter


class LinguisticProcessing:
    def __init__(self, raw_text):
        self.pos_tager = StanfordPOSTagger('opinion/stanford-postagger/models/chinese-nodistsim.tagger',
                                           path_to_jar = "opinion/stanford-postagger/stanford-postagger.jar")
        self.raw = raw_text
        self.segmenter = StanfordSegmenter(path_to_jar="opinion/stanford-segmenter/stanford-segmenter-3.6.0.jar",
                                           path_to_sihan_corpora_dict="opinion/stanford-segmenter/data",
                                           path_to_model="opinion/stanford-segmenter/data/ctb.gz",
                                           path_to_dict="opinion/stanford-segmenter/data/dict-chris6.ser.gz")
        self.pos_teg =self.tag_raw_file()

    def tag_raw_file(self, file_to_be_tagged=None):
        if file_to_be_tagged is None:
            token = self.segmenter.segment(self.raw)
        else:
            token = self.segmenter.segment(file_to_be_tagged)
        return self.pos_tager.tag(token)

    def mbf_reduction(self):
        pass

    def identification_negation_scopes(self):
        pass
