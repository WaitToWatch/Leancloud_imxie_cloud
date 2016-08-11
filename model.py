# -*- coding: utf-8 -*-

import leancloud
from leancloud import Object
from leancloud import Query

leancloud.init("6QyCCKpBBtpekBDNESzjsJ51-gzGzoHsz", "sy11owBJh0v09YY0bmAWdFhE")


class Email(Object):
    @property
    def src(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('src')

    @src.setter
    def src(self, value):
        # 同样的，可以给对象的score增加setter
        return self.set('src', value)


def save(value):
    Email = leancloud.Object.extend('Email')
    email = Email()
    email.set('src', value)
    is_exist = False
    try:
        query = Query(Email)
        if query.equal_to('src', value=value).first() is not None:
            print '数据库已存在 %s 账户' % value
    except Exception as e:
        # 找不到后插入
        print e
        email.save()
        is_exist = True
        pass
    return is_exist


def query_email():
    query = Query(Email)
    query.select("src")
    result = query.find()
    url_list = []
    print '====================待发送名单====================='
    for i in result:
        print u'丨 %s' % i.get('src')
        url_list.append(i.get('src'))
    print '================================================='
    return url_list


# ============================================


class Proxy(Object):
    @property
    def src(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('src')

    @src.setter
    def src(self, value):
        # 同样的，可以给对象的score增加setter
        return self.set('src', value)


def save_proxy(value):
    Proxy = leancloud.Object.extend('Proxy')
    proxy = Proxy()
    proxy.set('src', value)
    is_exist = False
    try:
        query = Query(Proxy)
        if query.equal_to('src', value=value).first() is not None:
            print '数据库已存在 (%s) IP 地址' % value
    except Exception as e:
        # 找不到后插入
        print e
        proxy.save()
        is_exist = True
        pass
    return is_exist


def query_proxy():
    proxy_list = []
    query = Query(Proxy)
    query.select('src')
    reslut = query.find()
    for i in reslut:
        proxy_list.append(i.get('src'))
    return proxy_list


def delete_proxy(value):
    query = Query(Proxy)
    this = query.equal_to('src', value=value).first()
    if this is not None:
        this.destroy()
        print '!!=====> 已经删除 %s' % value
