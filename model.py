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


# =========================================

class Proxy_Item(Object):
    last_page = 20
    urls = []

    @property
    def urls(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('urls')

    @urls.setter
    def urls(self, value, last_page=last_page):
        """
        example : http://www.kuaidaili.com/proxylist/%s/
        """
        for page in range(last_page):
            self.urls.append(value % page)
        self.set('urls', self.urls)

    @property
    def xp_count(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('xp_count')

    @xp_count.setter
    def xp_count(self, value):
        # 同样的，可以给对象的score增加setter
        self.set('xp_count', value)

    @property
    def xp_tb1(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('xp_tb1')

    @xp_tb1.setter
    def xp_tb1(self, value):
        # 同样的，可以给对象的score增加setter
        self.set('xp_tb1', value)

    @property
    def xp_tb2(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('xp_tb2')

    @xp_tb2.setter
    def xp_tb2(self, value):
        # 同样的，可以给对象的score增加setter
        self.set('xp_tb2', value)

    @property
    def host(self):
        # 可以使用property装饰器，方便获取属性
        return self.get('host')

    @host.setter
    def host(self, value):
        # 同样的，可以给对象的score增加setter
        self.set('host', value)


def save_proxy_item(url, count, tb1, tb2):
    item = Proxy_Item()
    urls = []
    for i in range(1, 11):
        urls.append(url % i)
    item.set('urls', urls)
    item.set('xp_count', count)
    item.set('xp_tb1', tb1)
    item.set('xp_tb2', tb2)
    item.set('host', url)
    query = Query(Proxy_Item)
    try:
        if query.equal_to('host', url).first() is not None:
            print '重复的 Host'
    except leancloud.LeanCloudError:
        item.save()


def query_proxy_item():
    proxy_list = []
    query = Query(Proxy_Item)
    for i in query.find():
        if isinstance(i, Proxy_Item):
            proxy_list.append(i)
    return proxy_list
