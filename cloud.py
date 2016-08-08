# coding: utf-8

from leancloud import Engine

from app import app

import one_email
import time

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
