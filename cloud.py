# coding: utf-8

from leancloud import Engine

from app import app
import time
from multiprocessing.dummy import Pool as ThreadPool

import one_email
import proxy_chicken
import model

engine = Engine(app)


# @engine.define
# def hello(**params):
#     if 'name' in params:
#         return 'Hello, {}!'.format(params['name'])
#     else:
#         return 'Hello, LeanCloud!'


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
    # 保持我的池子活着 5 个代理
    if len(model.query_proxy()) < 5:
        print '========寻找代理启动=========='
        proxy_chicken.pool_load(10)
        can_be_use = proxy_chicken.get_list()
        for value in can_be_use:
            model.save_proxy(value)
        print '===========存储完毕==========='
        check_delete_proxy()


@engine.define
def check_delete_proxy():
    print '===========检查启动==========='
    for i in model.query_proxy():
        if proxy_chicken.parse_proxy(i) is False:
            model.delete_proxy(i)
    print '===========再检完毕==========='
