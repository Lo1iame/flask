# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request,render_template
from flask_cors import *
from datetime import timedelta
import json
import blog

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})
app.send_file_max_age_default = timedelta(seconds=1)    #设置缓存文件过期时间，解决CSS不动态刷新的问题

#获取主页访问次数
@app.route("/visited_times/")
def visited_times():
    with open("./sever.json",'r') as sever_json:
        sever = json.load(sever_json)
    return jsonify({"visited_times":sever["visited_times"]})

#主页
@app.route("/")
def index():
    #从server.json得到当前访问次数
    with open("./sever.json",'r') as sever_json:
        sever = json.load(sever_json)
    #访问次数+1 并写入sever.json
    sever["visited_times"] = sever["visited_times"] + 1
    with open("./sever.json","w") as sever_json:
        json.dump(sever,sever_json)
    return render_template("index.html")

#404页面
@app.errorhandler(404)
def notFound(e):
    return render_template("404.html")

#获取网页图标
@app.route('/favicon.ico')
def get_fav():
    return app.send_static_file('favicon.ico')

#获取文章
@app.route('/api/get_posts/<num>')
def get_posts(num):
    print(num)
    try:
        #num=0时获取全部文章
        num = int(num)
        posts = blog.find_byNum(num)
        return jsonify({"code":1,"posts":posts})
    except:
        return jsonify({"code":0})



#启动配置
if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0",debug=True)
