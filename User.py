# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'
# Build-in / Std

from ScrollLoader import ScrollLoader
from Requests import *
from Answer import Answer

# 从User个人主页抓取信息


class User:

    def __init__(self, url):
        if not re.match("http://www.zhihu.com/people/.+", url):
            raise ValueError("\"" + url + "\"" + " : it isn't a user url.")
        else:
            self.url = url
        self.parser()

    def parser(self):
        try:
            r = requests.get(self.url)
            self.soup = BeautifulSoup(r.content)
        except:
            self.parser()

    def get_user_id(self):
        tmp = re.match(r'^(http://www.zhihu.com/people/)(.+)$', self.url)
        user_id = tmp.group(2)
        return user_id

    def get_follower_num(self):
        soup = self.soup
        followers_num = 0
        try:
            followers_num = int(soup.find(
                "div", class_="zm-profile-side-following zg-clear").find_all("a")[1].strong.string)
        except:
            pass
        finally:
            return followers_num

    def get_followee_num(self):
        soup = self.soup
        followee_num = 0
        try:
            followee_num = int(
                soup.find("div", class_="zm-profile-side-following zg-clear").find_all("a")[0].strong.string)
        except:
            pass
        finally:
            return followee_num

    def get_thanks_num(self):
        soup = self.soup
        thanks_num = 0
        try:
            thanks_num = int(
                soup.find("span", class_="zm-profile-header-user-thanks").strong.string)
        except:
            pass
        finally:
            return thanks_num

    def get_vote_num(self):
        soup = self.soup
        agree_num = 0
        try:
            agree_num = int(
                soup.find("span", class_="zm-profile-header-user-agree").strong.string)
        except:
            pass
        finally:
            return agree_num

    def get_ask_num(self):
        soup = self.soup
        ask_num = 0
        try:
            ask_num = int(soup.find_all("span", class_="num")[0].string)
        except:
            pass
        finally:
            return ask_num

    def get_answer_num(self):
        soup = self.soup
        answer_num = 0
        try:
            answer_num = int(soup.find_all("span", class_="num")[1].string)
        except:
            pass
        finally:
            return answer_num

    def get_articles_num(self):
        soup = self.soup
        articles_num = 0
        try:
            articles_num = int(soup.find_all("span", class_="num")[2].string)
        except:
            pass
        finally:
            return articles_num

    def get_collection_num(self):
        soup = self.soup
        collection_num = 0
        try:
            collection_num = int(soup.find(
                "div", class_="profile-navbar clearfix").find_all("a")[3].span.string)
        except:
            pass
        finally:
            return collection_num

    def get_following_topic_colum_num(self):
        soup = self.soup
        topic_num = 0
        column_num = 0
        try:
            tag_strings = soup.find_all(
                "div", class_="zm-profile-side-section-title")
            for tag_string in tag_strings:
                string = tag_string.find("a").strong.string
                substr = re.split("\s+", string)
                num = int(substr[0])
                if substr[1] is '个话题':
                    topic_num = num
                elif substr[1] is '个专栏':
                    column_num = num
        except:
            pass
        finally:
            return topic_num, column_num

    def get_location(self):  # 所在地
        soup = self.soup
        location = None
        try:
            location = unicode(
                soup.find("span", class_="location item").string)
        except:
            pass
        finally:
            return location

    def get_business(self):  # 行业
        soup = self.soup
        business_item = None
        try:
            business_item = unicode(
                soup.find("span", class_="business item").string)
        except:
            pass
        finally:
            return business_item

    def get_employment(self):  # 公司
        soup = self.soup
        employment = None
        try:
            employment = unicode(
                soup.find("span", class_="employment item").string)
        except:
            pass
        finally:
            return employment

    def get_position(self):  # 职位
        soup = self.soup
        position = None
        try:
            position = unicode(
                soup.find("span", class_="position item").string)
        except:
            pass
        finally:
            return position

    def get_education(self):
        soup = self.soup
        education = None
        try:
            education = unicode(
                soup.find("span", class_="education item").string)
        except:
            pass
        finally:
            return education

    def get_education_extra(self):
        soup = self.soup
        education_extra = None
        try:
            education_extra = unicode(
                soup.find("span", class_="education-extra item").string)
        except:
            pass
        finally:
            return education_extra

    def get_followers(self):
        follower_page_url = self.url + '/followers'
        r = requests.get(follower_page_url)
        text = r.text
        soup = BeautifulSoup(text)
        hash_id = get_hash_id(soup)
        _xsrf = get_xsrf(soup)
        scroll_loader = ScrollLoader(
            "post", "http://www.zhihu.com/node/ProfileFollowersListV2", 20, _xsrf, hash_id)
        for response in scroll_loader.run():
            for each in response:
                text += each
        follower_url_list = re.findall(
            r'<a[^>]+href=\"([^>]*)\"\x20class=\"zg-link\"', text)
        for url in follower_url_list:
            if not user_bloom.is_element_exist(User(url)):
                user_bloom.insert_element(User(url))
                user_queue.put(User(url))
                # yield User(url)

    def get_followees(self):
        followee_page_url = self.url + '/followees'
        r = requests.get(followee_page_url)
        text = r.text
        soup = BeautifulSoup(text)
        hash_id = get_hash_id(soup)
        _xsrf = get_xsrf(soup)
        scroll_loader = ScrollLoader(
            "post", "http://www.zhihu.com/node/ProfileFolloweesListV2", 20, _xsrf, hash_id)
        for response in scroll_loader.run():
            for each in response:
                text += each
        followee_url_list = re.findall(
            r'<a[^>]+href=\"([^>]*)\"\x20class=\"zg-link\"', text)
        for url in followee_url_list:
            if not user_bloom.is_element_exist(User(url)):
                user_bloom.insert_element(User(url))
                user_queue.put(User(url))
                # yield User(url)

    def get_asks(self):
        asks_num = self.get_ask_num()
        if asks_num == 0:
            return
        else:
            for i in xrange((asks_num - 1) / 20 + 1):
                ask_url = self.url + "/asks?page=" + str(i + 1)
                r = requests.get(ask_url)
                soup = BeautifulSoup(r.content)
                for question in soup.find_all("a", class_="question_link"):
                    url = "http://www.zhihu.com" + question["href"]
                    from Question import Question
                    if not question_bloom.is_element_exist(Question(url)):
                        question_bloom.insert_element(Question(url))
                        question_queue.put(Question(url))
                        # yield Question(url)

    def get_answers(self):
        answers_num = self.get_answer_num()
        if answers_num == 0:
            return
        else:
            for i in xrange((answers_num - 1) / 20 + 1):
                answer_url = self.url + "/answers?page=" + str(i + 1)
                r = requests.get(answer_url)
                soup = BeautifulSoup(r.content)
                for answer_tag in soup.find_all("a", class_="question_link"):
                    answer_url = 'http://www.zhihu.com' + answer_tag["href"]
                    if not answer_bloom.is_element_exist(Answer(answer_url)):
                        answer_bloom.insert_element(Answer(answer_url))
                        answer_queue.put(Answer(answer_url))
                        # yield Answer(answer_url)

    def get_columns(self):
        post_url = self.url + '/posts'
        r = requests.get(post_url)
        soup = BeautifulSoup(r.content)
        for each_column in soup.find_all("a", "avatar-link"):
            from Column import Column
            if not column_bloom.is_element_exist(Column(each_column['href'])):
                column_bloom.insert_element(Column(each_column['href']))
                column_queue.put(Column(each_column['href']))
                # yield Column(each_column['href'])

    def get_followeing_topics(self):
        url = self.url + '/topics'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        _xsrf = get_xsrf(soup)
        text = r.text
        scroll_loader = ScrollLoader("post", url, 20, _xsrf=_xsrf, start=0)
        for response in scroll_loader.run():
            for each in response:
                text += each
        topic_list = re.findall(
            r'<a\x20class=\"zm-list-avatar-link\"\x20href=\"([^>]*)\">', text)
        from Topic import Topic
        for url in topic_list:
            if not topic_bloom.is_element_exist(Topic("http://www.zhihu.com" + url)):
                topic_bloom.insert_element(Topic("http://www.zhihu.com" + url))
                topic_queue.put(Topic("http://www.zhihu.com" + url))
                # yield Topic("http://www.zhihu.com" + url)

    # TODO: 缺少一个get_following_column()函数
