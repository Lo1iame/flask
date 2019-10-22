# -*- coding: utf-8 -*-

from connection import con
from bson.objectid import ObjectId

db = con.loriame
col = db.post

#按数量查询文章
def find_byNum(num):
    posts = col.find(limit=num).sort([("create_time",-1)])
    post_list = []
    for post in posts:
        post["_id"] = str(post["_id"])
        post["create_time"] = str(post["create_time"])[0:16]
        post_list.append(post)
    return post_list

#按_id查询文章
def find_byId(id):
    posts = col.find({"_id":ObjectId(id)}).sort([("create_time",-1)])
    post_list = []
    for post in posts:
        post["_id"] = str(post["_id"])
        post["create_time"] = str(post["create_time"])
        post_list.append(post)
    return post_list

# print(find_byNum(0))