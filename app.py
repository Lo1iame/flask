# -*- coding: utf-8 -*-
import datetime

import pymongo
from flask import Flask, jsonify, request
from flask_cors import *

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})

con = pymongo.MongoClient("localhost",27017)
miku = con.miku

@app.route("/")
def hello():
    return "<h1>辣鸡姥爷git成功了</h1>"

# @app.route("/201966")
# def mie():
#     return "<p style='text-align:center;margin-top:20px;'><b style='font-size:20px;'>给小呆</b><br/><b>6.11</b><br/>夏天<br/>很热，但在遇见你之后，我的心在34℃的天气里滚烫沸腾成了100℃。<br/><b>6.12</b><br/>假如程序员用霸道总裁的语气说话<br/>大概就是：这个游戏对我女朋友来说太难了，给她写个无尽版本的。<br/><b>6.13</b><br/>我生活的目标就是不辜负你对我的喜爱<br/>以及把对你的爱
# 装的更满一点<br/><b>6.14</b><br/>想念使夜晚变得漫长<br/><b>6.15</b><br/>我长大又变小，一切在你眼里都变得渺小<br/><b>6.16</b><br/>你表达爱意的方式其实我都知道<br/>就在每一日的餐饭中<br/><b>6.17</b><br/>我希望能变成你的小骄傲<br/><b>6.19</b><br/>时间本该在两人的世界里静谧，却在你的心跳声中变得喧闹起来。<br/><b>6.20</b><br/>我真喜欢吓唬你，总是问你怕不怕。<br/>因为知道你心疼
# 我，你会很不舍得。</p>"


@app.route("/api/danmu_read",methods=["GET","POST"])
def danmu_read():
    col = miku.danmu
    results = col.find()
    danmu = []
    for r in results:
        danmu.append(r['text'])
    print(danmu)
    return jsonify({'danmu':danmu})

@app.route("/api/danmu_save",methods=["POST"])
def danmu_save():
    text = request.form['text']
    try:
        col = miku.danmu
        col.insert({'text': text})
        code = 1
    except:
        code = 0
    return jsonify({'code':code})

@app.route("/api/post_send",methods=["POST"])
def post_send():
    username = request.form['username']
    post = request.form['post']
    try:
        col = miku.post
        data = {
           'username':username,
           'post':post,
           'date':datetime.datetime.now().strftime('%Y/%m/%d')
        }
        col.insert(data)
        code = 1
    except:
        code = 0
    return jsonify({'code':code})

@app.route("/api/post_get",methods=["GET","POST"])
def post_get():
    col = miku.post
    results = col.find()
    posts = []
    for r in results:
        post = {
           'username':r['username'],
            'post':r['post'],
            'date':r['date']
        }
        posts.append(post)
    return jsonify({'posts':posts})



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0",debug=True)
