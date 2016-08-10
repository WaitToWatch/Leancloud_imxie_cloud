# coding: utf-8

from leancloud import Engine

from app import app
import time

import one_email
import proxy_chicken
import one_save_email

engine = Engine(app)


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.define
def send_one_email():
    one_email.http('http://wufazhuce.com/')
    print '========================================'
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print '完成邮件发送'


@engine.define
def send_test_email(email):
    one_email.test_email(email)


@engine.define
def check_save_proxy():
    for i in range(1, 20):
        proxy_chicken.get_proxy_ip(i)
    can_be_use = proxy_chicken.get_list()
    for value in can_be_use:
        one_save_email.save_proxy(value)
