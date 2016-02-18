#!/usr/bin/env python
# -*- coding:utf-8 -*-
from nltk.tokenize.stanford_segmenter import StanfordSegmenter
from nltk.parse.stanford import StanfordParser


class LinguisticProcessing:
    """
    >>使用标记与宾州树库一致,常用标记如下:
    ROOT:要处理文本的语句
    IP:简单从句
    NP:名词短语
    VP:动词短语
    PU:断句符
    LCP:方位词短语
    PP:介词短语
    CP:由'的'构成的表示修饰性关系的短语
    DNP:由'的'构成的表示所属关系的短语
    ADVP:副词短语
    ADJP:形容词短语
    DP:限定词短语
    QP:量词短语
    NN:常用名词
    NR:固有名词
    NT:时间名词
    PN:代词
    VV:动词
    VC:是
    CC:不是
    VE:有
    VA:表语形容词
    AS:内容标记
    VRD:动补复合词
    """
    def __init__(self, raw_text):
        self.raw = raw_text
        self.segmenter = StanfordSegmenter(
                path_to_jar = u"opinion/stanford-segmenter/stanford-segmenter.jar",
                path_to_sihan_corpora_dict = u"opinion/stanford-segmenter/data",
                path_to_model = u"opinion/stanford-segmenter/data/ctb.gz",
                path_to_dict = u"opinion/stanford-segmenter/data/dict-chris6.ser.gz")
        self.parser = StanfordParser(
                path_to_jar = u'/usr/local/Cellar/stanford-parser/3.5.2/libexec/stanford-parser.jar',
                path_to_models_jar = u'/usr/local/Cellar/stanford-parser/3.5.2/libexec/stanford-parser-3.5.2-models.jar',
                model_path = u'edu/stanford/nlp/models/lexparser/chinesePCFG.ser.gz')
        self.sent_tree = self.parse()
        self.negation = {'word': [], 'scope': []}

    def parse(self):
        segmented_sent = self.segmenter.segment(self.raw)
        sent_tree = list(self.parser.raw_parse(sentence = segmented_sent))[0]
        return sent_tree

    def identification_negation_scopes(self, predefined_disc):
        positions = self.sent_tree.treepositions()
        for position in positions:
            if self.sent_tree[position][::-1] in predefined_disc:
                self.negation['word'].append(self.sent_tree[position][::-1])
                self.negation['scope'].append(position)
