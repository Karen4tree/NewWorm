# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'

from zhihu_api.User import User
from zhihu_api.Topic import Topic
from zhihu_api.Question import Question
from zhihu_api.Answer import Answer

from database_operation.IfExist import IfExist
from database_operation.DataBase import DataBase


def main():
    answer_url = "http://www.zhihu.com/question/36713461/answer/68820809"
    answer = Answer(answer_url)
    question = Question("http://www.zhihu.com/question/36713461")
    DataBase.put_user_in_db(answer.get_author())
    DataBase.put_question_in_db(question)
    DataBase.put_answer_in_db(answer)


if __name__ == '__main__':
    main()
