#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.Topic import Topic
from zhihu_api.Question import Question
from zhihu_api.Answer import Answer
from zhihu_api.User import User
from database_operation.DataBase import DataBase
from database_operation.ReadData import ReadData

def spider():
    topic = Topic("http://www.zhihu.com/topic/20038840")
    questions = topic.get_questions()
    for question in questions:
        try:
            DataBase.put_question_in_db(question)
            for answer in question.get_answers():
                DataBase.put_answer_in_db(answer)
                answerer = answer.get_author()
                DataBase.put_user_in_db(answerer)
                DataBase.put_user_answer_in_db(answerer,answerer)
            for _topic in question.get_topics():
                DataBase.put_topic_in_db(_topic)
                DataBase.put_question_topic_in_db(question,_topic)
        except:
            pass

if __name__ == "__main__":
    spider()
