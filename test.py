# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from User import User
from Questions import Questions
from Answers import Answers
from Topics import Topics
from Collections import Collections
from Article import Article

def test_user(user_url):
    user = User(user_url)
    answer_num = user.get_answer_num()
    print answer_num
    ask_num = user.get_ask_num()
    print ask_num
    followee_num = user.get_followee_num()
    article_num = user.get_articles_num()
    print article_num
    print followee_num
    follower_num = user.get_follower_num()
    print follower_num
    collection_num = user.get_collection_num()
    print collection_num
    thanks_num = user.get_thanks_num()
    print thanks_num
    vote_num = user.get_vote_num()
    print vote_num
    location = user.get_location()
    print location
    business = user.get_business()
    print business
    employment = user.get_employment()
    print employment
    position = user.get_position()
    print position
    education = user.get_education()
    print education
    education_extra = user.get_education_extra()
    print education_extra

    following_topic_num = user.get_following_topics_num()
    print following_topic_num
    following_column_num = user.get_following_columns_num()
    print following_column_num
    user_id = user.get_user_id()
    print user_id
    asks = user.get_asks()
    for question in asks:
        print question.get_title()
    answers = user.get_answers()
    for answer in answers:
        print answer.get_answer_id()

    #articles = user.get_articles()
    #for article in articles:
    #    print article.get_title()


def test_answer(answer_url):
    answer = Answers(answer_url)
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
    upvoters = answer.get_upvoters()
    for upvoter in upvoters:
        print upvoter.get_user_id()


def topic_test(topic_url):
    topic = Topics(topic_url)
    topic_id = topic.get_topic_id()
    print topic_id
    topic_name = topic.get_topic_name()
    print topic_name
    question_num = topic.get_questions_num()
    print question_num
    follower_num = topic.get_followers_num()
    print follower_num
    questions = topic.get_questions()
    for question in questions:
        print question.get_question_id()
    # followers = topic.get_followers()
    # print followers

def question_test(question_url):
    question = Questions(question_url)
    question_id = question.get_question_id()
    print question_id
    follower_num = question.get_follower_num()
    print follower_num
    title = question.get_title()
    detail = question.get_detail()
    print title
    print detail
    answer_num = question.get_answers_num()
    print answer_num
    topics = question.get_topics()
    #for topic in topics:
    #    print topic.get_topic_id()
    #answers = question.get_answers()
    #for answer in answers:
    #    print answer.get_detail()
    #followers = question.get_followers()
    #for follower in followers:
    #    print follower.get_user_id()

def collection_test(collection_url):
    collection = Collections(collection_url)
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
    article = Article(article_url)
    article_id = article.get_article_id()
    print article_id
    title = article.get_article_title()
    print title


def main():
    user_url = "http://www.zhihu.com/people/xiepanda"
    answer_url = "http://www.zhihu.com/question/36713461/answer/68820809"
    topic_url = "http://www.zhihu.com/topic/19550376"
    question_url = "http://www.zhihu.com/question/31918396"
    collection_url = "http://www.zhihu.com/collection/19689137"
    article_url = "http://zhuanlan.zhihu.com/seasee/20275752"
    #test_user(user_url)
    #test_answer(answer_url)
    #topic_test(topic_url)
    #question_test(question_url)
    #collection_test(collection_url)
    article_test(article_url)


if __name__ == '__main__':
    main()
