# coding: utf-8

from datetime import datetime

import requests
from flask import Flask
from flask import render_template
from flask_sockets import Sockets
from views.todos import todos_view
from flask_bootstrap import Bootstrap

import one_email

app = Flask(__name__)
sockets = Sockets(app)
bootstrap = Bootstrap(app)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')

# 变量
android_page = 1
girl_page = 1


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/android')
def get_android():
    global android_page
    # 随机获取10条 Android 的推荐
    results = requests.get('http://gank.io/api/data/Android/10/' + str(android_page)).json().get('results')
    # 仅需要标题和 url
    data = [{'desc': result.get('desc'), 'url': result.get('url')} for result in results]
    android_page += 1

    # 渲染 HTML 模板
    return render_template('android.html', datas=data)


@app.route('/girls')
def get_girls():
    # gank.io 妹子
    global girl_page
    results = requests.get('http://gank.io/api/data/%E7%A6%8F%E5%88%A9/10/' + str(girl_page)).json().get('results')
    data = [{'url': result.get('url')} for result in results]
    girl_page += 1
    return render_template('girls.html', datas=data)


@app.route('/one')
def get_one():
    return render_template('one.html', data=one_email.get_one_page())


@app.route('/save_email')
def save_email():
    return render_template('save_email.html')
