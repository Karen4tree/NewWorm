# -*- coding: utf-8 -*-
__author__ = 'ZombieGroup'

import MySQLdb
import json
from zhihu_api.Topic import Topic

connect = MySQLdb.connect('localhost', 'root', '', 'zhihu', port=3306, charset='utf8')
cursor = connect.cursor()


def recursive_dic(father_topid_id):
    try:
        cursor.execute('select topic_name,question_num,followers_num from Topic'
                       ' where topic_id=%s', father_topid_id)
        result_info = cursor.fetchone()
        tree = {}
        tree["url"] = "https://www.zhihu.com/topic/{0}".format(father_topid_id)
        tree["name"] = result_info[0]
        tree["question_num"] = result_info[1]
        tree["followers_num"] = result_info[2]
        tree["children"] = []

        cursor.execute('select child_topid_id from Topic_Topics where father_topid_id=%s', father_topid_id)
        result = cursor.fetchall()
        if result is not None:
            for child_topid_id in result:
                if child_topid_id is not None:
                    tree["children"].append(recursive_dic(child_topid_id))
        return tree;
    except:
        return {}


if __name__ == '__main__':
    root_id = 19776749
    result_dic = recursive_dic(root_id)
    with open('result.json','w') as f:
        f.write(json.dumps(result_dic))
