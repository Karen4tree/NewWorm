#!/usr/bin/env python
# -*- coding:utf-8 -*-
from zhihu_api.User import User


# User Influence is caculated with similar method used in Klout
# http://klout.com/home, published in May, 2014


class ExtendUser(User):
    def __init__(self, url=None, user=None):
        #if url is None:
        #    User.__init__(self, user.url)
        #elif user is None:
        User.__init__(self, url)
        self.influence = 0
        self.caculate_influence()

    def caculate_influence(self):
        self.influence = self.reach_score()+self.amplification_score()+self.network_score()
        return self.influence

    def reach_score(self):
        # Reach means the average number of people which <user> can reach with his/her content.
        answers = self.get_answers()
        questions = self.get_asks()
        averange_answer_reach = averange_question_reach = 0
        for answer in answers:
            answer_reach = answer.get_visited_times()
            answer_reach += answer.get_upvote_num()
            averange_answer_reach += answer_reach
        averange_answer_reach = float(averange_answer_reach)/ float(self.get_answer_num())
        for question in questions:
            question_reach = 0
            answer_of_question = question.get_answers()
            for item in answer_of_question:
                question_reach += item.get_visited_times()
                question_reach += item.get_upvote_num()
            question_reach += question.get_follower_num()
        averange_question_reach = float(averange_question_reach)/ float(self.get_ask_num())
        return averange_answer_reach * 1 + averange_question_reach * 1

    def amplification_score(self):
        # How likely the audience will respond.
        answers = self.get_answers()
        questions = self.get_asks()
        amp_answer = amp_question = 0
        for answer in answers:
            answer_reach = answer.get_visited_times()
            answer_reach += answer.get_upvote_num()
            amp_answer += float(answer.get_upvote_num()) / float(answer_reach)
        amp_answer = amp_answer / self.get_answer_num()
        for question in questions:
            for answer in question.get_answers():
                answer_reach = answer.get_visited_times()
                answer_reach += answer.get_upvote_num()
                amp_question += float(answer.get_upvote_num()) / float(answer_reach)
        amp_question = amp_question / self.get_ask_num()
        return amp_answer + amp_question

    def network_score(self):
        # A measurement of the influence of a user's audience.
        follower_influence = []
        for follower in self.get_followers():
            follower_influence.append(follower.caculate_influence())
            # TODO:互相关注怎么解决?
        score = float(sum(follower_influence))/float(len(follower_influence))
        return score
