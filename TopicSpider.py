#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Topic import Topic
from database_operation.DataBase import DataBase


def store(topic):
    if topic is not None:
        try:
            DataBase.put_topic_in_db(topic)
            print topic.get_topic_name()
        except:
            pass
        finally:
            for item in topic.get_child():
                store(item)
                DataBase.put_topic_topic_in_db(topic,item)



if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(1000000)
    rootTopic = Topic("http://www.zhihu.com/topic/20038840")
    store(rootTopic)
