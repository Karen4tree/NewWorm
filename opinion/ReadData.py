#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import re


class DataReader:
    # datafile: location of the file storing (text,timestamp) pairs.
    #           every single pair takes one line.
    #           text and timestamp are wrapped separately by {}.
    def __init__(self, data_file):
        self.file = codecs.open(data_file, encoding = 'utf8')
        self.data = []
        self.extract_into_pairs()

    def extract_into_pairs(self):
        for line in self.file:
            pair = re.match(r'\{.*\}.*\{.*\}', line)
            time = pair.group(2)
            text = pair.group(1)
            self.data.append({'time': time, 'text': text})
