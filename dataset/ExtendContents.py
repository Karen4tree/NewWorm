#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from pandas import Series
from qcloudapi.QcloudApi.qcloudapi import QcloudApi
import pandas.io.sql as pandasql
from database_operation.ReadData import ReadData


class Opinion:
    def __init__(self):
        module = 'wenzhi'
        config = {
            'Region': 'gz',
            'secretId': 'AKIDS6fypYffcsCMxFmAsac9FOjEdncAlHMM',
            'secretKey': 'eu7cqU9zL90nMKodFwxGihRO62PNqTEB',
            'method': 'get'
        }
        # Limit 5 调试结束后可去掉
        self.answer_frame = pandasql.read_frame('select detail,author_id,last_edit_time from Answers LIMIT 5', ReadData.connect)
        self.service = QcloudApi(module, config)

    def caculate_opinion(self):
        opinion = []
        for text in self.answer_frame.detail:
            text = text.encode('utf8')
            params = {
                'content': text,
            }
            try:
                string = self.service.call('TextSentiment', params)
                tmp = re.match(u'.*\"positive\":(.*),\"negative\".*', string)
                opinion.append(float(tmp.group(1)))
            except:
                opinion.append(0.5)
        self.answer_frame['opinion'] = Series(opinion)
