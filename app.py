# -*- coding: utf-8 -*-

#进入环境
#source ../venv/bin/activate

import datetime

import pymongo
from flask import Flask, jsonify, request,render_template
from flask_cors import *
from datetime import timedelta


app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})

app.send_file_max_age_default = timedelta(seconds=1)    #设置缓存文件过期时间，解决CSS不动态刷新的问题

con = pymongo.MongoClient("localhost",27017)
miku = con.miku

#主页
@app.route("/")
def hello():
    return render_template("index.html")


#404页面
@app.errorhandler(404)
def notFound(e):
    return render_template("404.html")

#获取网页图标
@app.route('/favicon.ico')
def get_fav():
    return app.send_static_file('favicon.ico')

#读取弹幕
@app.route("/api/danmu_read",methods=["GET","POST"])
def danmu_read():
    col = miku.danmu
    results = col.find()
    danmu = []
    for r in results:
        danmu.append(r['text'])
    print(danmu)
    return jsonify({'danmu':danmu})

#保存弹幕
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

#发送留言
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

#获取留言
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



#启动配置
if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0",debug=True)
