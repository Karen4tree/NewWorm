# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'

from zhihu_api.User import User
from zhihu_api.Topic import Topic
from zhihu_api.Question import Question
from zhihu_api.Answer import Answer

from database_operation.IfExist import IfExist
from database_operation.DataBase import DataBase


def topic_crawler(topic):
    print topic.get_topic_name()
    for child_topic in topic.get_child():
        if not DataBase.topic_exist(child_topic):
            DataBase.put_topic_in_db(child_topic)
        DataBase.put_topic_topic_in_db(topic,child_topic)
    DataBase.topic_checked(topic)


def main():
    root_url = "http://www.zhihu.com/topic/19776749"
    topic = Topic(root_url)
    DataBase.put_topic_in_db(topic)
    topic_id = DataBase.one_topic_id_unvisited()
    while topic_id is not None:
        topic_crawler(Topic("http://www.zhihu.com/topic/{0}".format(topic_id)))
        topic_id = DataBase.one_topic_id_unvisited()

if __name__ == '__main__':
    main()
