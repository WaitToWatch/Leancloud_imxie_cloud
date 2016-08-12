# coding: utf-8
import model
import proxy_chicken
import cloud
import time
from multiprocessing import Pool as ThreadPool
import requests
from lxml import etree
import Queue


# one_save_email.query_email()

# s = '还可以'
#
# print '测试%s 这个也是%f' % (s, 0.2323)
#
# proxy_chicken.get_proxy_ip(2)

# model.query_proxy()


def check_delete_proxy():
    for i in model.query_proxy():
        print i
        if proxy_chicken.parse_proxy(i) is False:
            model.delete_proxy(i)


# proxy_chicken.pool_load(5)

model.save_proxy_item('http://www.kuaidaili.com/free/inha/%s/', '//*[@id="list"]/table/tbody/tr',
                      '//*[@id="list"]/table/tbody/tr[%d]/td[1]/text()',
                      '//*[@id="list"]/table/tbody/tr[%d]/td[2]/text()')

model.save_proxy_item('http://www.xicidaili.com/nn/%s', '//*[@id="ip_list"]/tbody/tr',
                      '//*[@id="ip_list"]/tbody/tr[%d]/td[2]/text()',
                      '//*[@id="ip_list"]/tbody/tr[%d]/td[3]/text()')
