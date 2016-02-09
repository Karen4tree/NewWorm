#!/usr/bin/env python
# -*- coding:utf-8 -*-

from zhihu_api.Topic import Topic
from database_operation.DataBase import DataBase


def store(topic):
    for item in topic.get_child():
        store(item)
    DataBase.put_topic_in_db(topic)

rootTopic = Topic("http://www.zhihu.com/topic/19776749")

if __name__ == "__main__":
    rootTopic = Topic("http://www.zhihu.com/topic/19776749")
    store(rootTopic)
