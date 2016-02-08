# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from database_operation.DataBase import DataBase
from zhihu_api.User import User
from zhihu_api.Topic import Topic

from database_operation.IfExist import IfExist
from zhihu_api.Question import Question


def main():
    #user_msg = User(u"http://www.zhihu.com/people/Fooying")
    topic = Topic("http://www.zhihu.com/topic/19553732")
    DataBase.put_topic_in_db(topic)


if __name__ == '__main__':
    main()
