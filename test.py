# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
from msg_from_web import User
from msg_from_web import Questions
from msg_from_web import Answers
from msg_from_web import Topics

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
#    asks = user.get_asks()
#    answers = user.get_answers()

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

def main():
    #user_url = "http://www.zhihu.com/people/xiepanda"
    #test_user(user_url)
    #answer_url = "http://www.zhihu.com/question/36669529/answer/68811311"
    #test_answer(answer_url)
    topic_url = "http://www.zhihu.com/topic/19564496"
    topic_test(topic_url)

if __name__ == '__main__':
    main()
