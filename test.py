# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'

from zhihu_api.User import User
from zhihu_api.Logging import Logging
from zhihu_api.Question import Question
from zhihu_api.Answer import Answer
from zhihu_api.Topic import Topic
from zhihu_api.Collection import Collection
from zhihu_api.Article import Article


def test_user(user_url):
    Logging.info(u"test_user:")
    user = User(user_url)
    print user.url
    for follower in user.get_followers():
        print follower.url

    answer_num = user.get_answer_num()
    print answer_num
    ask_num = user.get_ask_num()
    print ask_num
    followee_num = user.get_followee_num()
    article_num = user.get_articles_num()
    print article_num
    print followee_num
        # follower_num = user.get_follower_num()
        # print follower_num
        # collection_num = user.get_collection_num()
        # print collection_num
        # thanks_num = user.get_thanks_num()
        # print thanks_num
        # vote_num = user.get_vote_num()
        # print vote_num
        # location = user.get_location()
        # print location
        # print type(location)
        # business = user.get_business()
        # print business
        # print type(business)
        # employment = user.get_employment()
        # print employment
        # print type(employment)
        # position = user.get_position()
        # print position
        # print type(position)
        # education = user.get_education()
        # print education
        # print type(education)
        # education_extra = user.get_education_extra()
        # print education_extra
        # print type(education_extra)
        # following_topic_num = user.get_following_topic_num()
        # print following_topic_num
        # following_column_num = user.get_following_column_num()
        # print following_column_num
        # Logging.info(u"followeing_topics:")
        # for followeing_topics in user.get_followeing_topics():
        #     print followeing_topics

        # Logging.info(u"Columns and Articles of User")
        # for column in user.get_columns():
        #     for article in column.get_articles():
        #         print article

        # user_id = user.get_user_id()
        # print user_id
        # asks = user.get_asks()

        # Logging.info(u"Questions of User")
        # for question in asks:
        #    print question.get_title()
        # answers = user.get_answers()

        # Logging.info(u"Answers of User")
        # for answer in answers:
        #    print answer.get_answer_id()


'''
    Logging.info(u"Followers of User")
    for follower in user.get_followers():
        print follower.get_user_id()

    Logging.info(u"Followee of User")
    for followee in user.get_followees():
        print followee.get_user_id()

    Logging.info(u"Columns and Articles of User")
    for column in user.get_columns():
        print column.url
        for article in column.get_article():
            print article'''


def test_answer(answer_url):
    Logging.info(u"test_answer:")
    answer = Answer(answer_url)
    answer_id = answer.get_answer_id()
    print answer_id
    question_id = answer.get_question_id()
    print question_id
    author_id = answer.get_author_id()
    print author_id
    detail = answer.get_detail()
    print detail
    upvote_num = answer.get_upvote_num()
    print upvote_num
    visited_times = answer.get_visited_times()
    print visited_times
    # upvoters = answer.get_upvoters()
    # for upvoter in upvoters:
    # print upvoter.get_user_id()


def topic_test(topic_url):
    Logging.info(u"topic_test:")
    topic = Topic(topic_url)
    topic_id = topic.get_topic_id()
    print topic_id
    topic_name = topic.get_topic_name()
    print topic_name
    question_num = topic.get_question_num()
    print question_num
    follower_num = topic.get_follower_num()
    print follower_num
    questions = topic.get_questions()


#    for question in questions:
#        print question.get_question_id()


def question_test(question_url):
    Logging.info(u"question_test:")
    question = Question(question_url)
    question_id = question.get_question_id()
    print question_id
    follower_num = question.get_follower_num()
    print follower_num
    title = question.get_title()
    detail = question.get_detail()
    print title
    print detail
    answer_num = question.get_answer_num()
    print answer_num
    topics = question.get_topics()
    for topic in topics:
        print topic.get_topic_id()
    # answers = question.get_answers()
    # for answer in answers:
    #    print answer.get_detail()
    followers = question.get_followers()
    for follower in followers:
        print follower.get_user_id()

    question.get_followers()


def collection_test(collection_url):
    Logging.info(u"collection_test:")
    collection = Collection(collection_url)
    collection_id = collection.get_collection_id()
    print collection_id
    collection_name = collection.get_collection_name()
    print collection_name
    creator = collection.get_creator()
    print creator.get_user_id()
    answers = collection.get_answers()
    for answer in answers:
        print answer.get_answer_id()


def article_test(article_url):
    Logging.info(u"article_test:")
    article = Article(article_url)
    article_id = article.get_article_id()
    print article_id
    title = article.get_article_title()
    print title


def test_topic(topic_url):
    Logging.info(u"topic_test:")
    topic = Topic(topic_url)
    for question in topic.get_questions():
        print question.get_question_id()


def main():
    user_url = "http://www.zhihu.com/people/li-ji-87-69-14"
    answer_url = "http://www.zhihu.com/question/36713461/answer/68820809"
    topic_url = "http://www.zhihu.com/topic/19554927"
    question_url = "http://www.zhihu.com/question/23623967"
    collection_url = "http://www.zhihu.com/collection/19689137"
    article_url = "http://zhuanlan.zhihu.com/seasee/20275752"
    test_user(user_url)
    # test_answer(answer_url)
    # topic_test(topic_url)
    # question_test(question_url)
    # collection_test(collection_url)
    # article_test(article_url)


if __name__ == '__main__':
    #main()

    from zhihu_api.Requests import requests

    print requests.get("http://www.zhihu.com/people/li-ji-87-69-14")
    from zhihu_api.Login import Login
    print Login.islogin()
