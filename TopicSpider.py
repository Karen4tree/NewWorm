#!/usr/bin/env python
# -*- coding:utf-8 -*-

if __name__ == '__main__':
    THREADS = 8
    p = mp.Pool(THREADS)
    topic = Topic("http://www.zhihu.com/topic/19736651")
    if not topicBloom.is_element_exist(topic.get_topic_id()):
        topicBloom.insert_element(topic.get_topic_id())
        Worm_status.record_status("topicBloom", topicBloom)
        DataBase.put_topic_in_db(topic)
    go = topic.get_questions()
    N = 20
    while True:
        try:
            p.map_async(spider, itertools.islice(go, N))
        except TypeError:
            continue