# coding: utf-8

from datetime import datetime

import requests
from flask import Flask
from flask import render_template
from flask_sockets import Sockets
from views.todos import todos_view
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, DataRequired, Email

import one_email
import model

app = Flask(__name__)
sockets = Sockets(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'Key+1s'


# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')

# 变量
android_page = 1
girl_page = 1

receiver = ''


class EmailForm(Form):
    address = StringField('您的邮箱是?', validators=[Email()])
    submit = SubmitField('提交邮箱')


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


@app.route('/save_email', methods=['GET', 'POST'])
def save_email():
    form = EmailForm()
    feed_back = ''
    global receiver
    if form.validate_on_submit():
        # 提交内容合理则进行的操作
        address = form.address.data
        form.address.data = ''
        if model.save(address) is True:
            feed_back = '存入完毕,并且已经发送一个测试邮件,请查收 \n 可能会被误认为垃圾邮件'
            one_email.test_email(address)
        else:
            feed_back = '当前 %s 已存在数据库' % address
        receiver = address
    return render_template('save_email.html', form=form, feedback=feed_back)


@app.route('/test_email', methods=['GET', 'POST'])
def test_email():
    result = one_email.test_email(receiver)
    return result
