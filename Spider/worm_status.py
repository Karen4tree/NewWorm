#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from ConfigParser import ConfigParser

from Spider.BloomFliter import BloomFilter


class Worm_status:
    config_file = "worminit.ini"

    @classmethod
    def read_status(cls, section):
        cf = ConfigParser()
        ERROR_RATE = 0.05
        ITEM_NUM = 10000
        if os.path.exists(cls.config_file) and os.path.isfile(cls.config_file):
            cf.read(cls.config_file)
            bit_num = cf.get(section, "bit_num")
            bit_array = cf.get(section, "bit_array")
            hash_num = cf.get(section, "hash_num")
            hash_seeds = cf.get(section, "hash_seeds")
            if bit_array != "" and bit_num != "" and hash_seeds != "" and hash_num != "":
                bit_num = int(bit_num)
                hash_num = int(hash_num)

                hash_seeds = re.split(r'[\[\]\,\s]', hash_seeds)
                tmp = []
                for each in hash_seeds:
                    if each is not '':
                        each = int(each)
                        tmp.append(each)
                hash_seeds = tmp

                return BloomFilter(ERROR_RATE, ITEM_NUM, bit_num = bit_num, bit_array = bit_array, hash_num = hash_num,
                                   hash_seeds = hash_seeds)
            else:
                return BloomFilter(ERROR_RATE, ITEM_NUM)

    @classmethod
    def record_status(cls, section, value):
        cf = ConfigParser()
        if os.path.exists(cls.config_file) and os.path.isfile(cls.config_file):
            cf.read(cls.config_file)
            cf.set(section = section, option = "bit_num", value = value.bit_num)
            cf.set(section = section, option = "bit_array", value = value.bit_array.get_text_from_bitvector())
            cf.set(section = section, option = "hash_num", value = value.hash_num)
            cf.set(section = section, option = "hash_seeds", value = value.hash_seeds)
            cf.write(open(cls.config_file, "w"))
