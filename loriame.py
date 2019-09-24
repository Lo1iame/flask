import pymongo
from datetime import datetime

con = pymongo.MongoClient("47.102.136.23",27017)
loriame = con.loriame
post = loriame.post

print(datetime.utcnow())

# re = post.find({"create_time":{"$gte":datetime(2019,9,23),"$lt":datetime(2019,9,24)}})
# for r in re:
#     print(r)

data = {
    "cover":"miku.png",
    "title":"这是一个插入测试",
    "content":"从零开始一行行代码堆的博客",
    "create_time":datetime.utcnow(),
    "author":"Loriame",
    "views":1,
    "like":0
}

post.insert(data)
    