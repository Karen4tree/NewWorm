#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from ConfigParser import ConfigParser
from BloomFliter import BloomFilter


class Worm_status:
    config_file = "worminit.ini"

    @classmethod
    def read_status(cls, section):
        cf = ConfigParser()
        if os.path.exists(cls.config_file) and os.path.isfile(cls.config_file):
            cf.read(cls.config_file)
            bit_num = cf.get(section, "bit_num")
            bit_array = cf.get(section, "bit_array")
            hash_num = cf.get(section, "hash_num")
            hash_seeds = cf.get(section, "hash_seeds")
            ERROR_RATE = cf.get("basic", "ERROR_RATE")
            ITEM_NUM = cf.get("basic", "ITEM_NUM")
            return BloomFilter(ERROR_RATE, ITEM_NUM, bit_num = bit_num, bit_array = bit_array, hash_num = hash_num,
                               hash_seeds = hash_seeds)
        else:
            ERROR_RATE = cf.get("basic", "ERROR_RATE")
            ITEM_NUM = cf.get("basic", "ITEM_NUM")
            return BloomFilter(ERROR_RATE,ITEM_NUM)

    @classmethod
    def record_status(cls, section, value):
        cf = ConfigParser()
        cf.set(section, "bit_num", value = value.bit_num)
        cf.set(section, "bit_array", value = value.bit_array)
        cf.set(section, "hash_num", value = value.hash_num)
        cf.set(section, "hash_seeds", value = value.hash_seeds)
