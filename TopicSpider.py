#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Topic import Topic
from database_operation.DataBase import DataBase


def store(topic):
    if topic is not None:
        for item in topic.get_child():
            store(item)
        try:
            DataBase.put_topic_in_db(topic)
            print topic.get_topic_name()
        except:
            pass


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(1000000)
    rootTopic = Topic("http://www.zhihu.com/topic/19776749")
    store(rootTopic)
