#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import re


class DataReader:

    def __init__(self, data_file):
        self.file = codecs.open(data_file, encoding = 'utf8')
        self.data = {'time': [], 'text': [], 'author': [], 'topics': []}
        self.extract_into_pairs()

    def extract_into_pairs(self):
        for line in self.file:
            pair = re.match(r'(\#.+)(\{.*\}).*(\{.*\}).*(\{.*\})', line)
            time = pair.group(3)
            text = pair.group(2)
            author = pair.group(4)
            topics = pair.group(1)
            self.data['time'].append(time)
            self.data['text'].append(text)
            self.data['author'].append(author)
            self.data['topics'].append(topics)
