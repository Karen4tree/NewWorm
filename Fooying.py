# -*- coding: utf-8 -*-_
__author__ = 'ZombieGroup'

from DataBase import DataBase
from Topic import Topic

user = 'root'
host = 'localhost'
password = ''
dbname = 'zhihu'
db = DataBase(user, host, password, dbname)


def spider(questions):
    for question in questions:
        db.put_question_in_db(question)
        for answer in question.get_answers():
            db.put_answer_in_db(answer)
            db.put_vote_in_db(answer)


if __name__ == '__main__':
    topic = Topic("http://www.zhihu.com/topic/19554927")
    db.put_topic_in_db(topic)
    questions = topic.get_questions()
    spider(questions)
