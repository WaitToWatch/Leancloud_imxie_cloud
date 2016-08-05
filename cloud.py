# coding: utf-8

from leancloud import Engine

from app import app

import one_email;


engine = Engine(app)


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.define
def log_timer():
    one_email.http('http://wufazhuce.com/')
    print 'Log in timer.'



