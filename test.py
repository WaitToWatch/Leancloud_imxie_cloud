# coding: utf-8
import model
import proxy_chicken
import cloud
import time
from multiprocessing import Pool as ThreadPool
import requests
from lxml import etree
import Queue
from lxml import html
import logging

header_info = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Content-Type': 'ext/html; charset=utf-8'
}

logging.getLogger(__name__)


def check_delete_proxy():
    for i in model.query_proxy():
        print i
        if proxy_chicken.parse_proxy(i) is False:
            model.delete_proxy(i)


# proxy_chicken.pool_load(5)

# 这里需要清除 tbody
# model.save_proxy_item('http://www.xicidaili.com/nn/%s', '//*[@id="ip_list"]/tr',
#                       '//*[@id="ip_list"]/tr[%d]/td[2]/text()',
#                       '//*[@id="ip_list"]/tr[%d]/td[3]/text()')
#
# model.save_proxy_item('http://www.kuaidaili.com/free/inha/%s/', '//*[@id="list"]/table/tbody/tr',
#                       '//*[@id="list"]/table/tbody/tr[%d]/td[1]/text()',
#                       '//*[@id="list"]/table/tbody/tr[%d]/td[2]/text()')


# r = requests.get('http://www.kuaidaili.com/free/inha/1/', headers=header_info)
# print r.status_code
# text = etree.HTML(r.text)
#
# # logging.info(r.text)
#
# logging.info(text.xpath('//*[@id="list"]/table/tbody/tr'))


def test_for_new():
    r = requests.get('http://www.xicidaili.com/nn/1', headers=header_info)
    print r.status_code
    text = etree.HTML(r.text)
    # logging.info(r.text)
    count = len(text.xpath('//*[@id="ip_list"]/tr'))
    print count
    logging.info(text.xpath('//*[@id="ip_list"]/tr'))
    for i in range(count):
        if len(text.xpath('//*[@id="ip_list"]/tr[%d]/td[2]/text()' % i))!=0:
            logging.info(text.xpath('//*[@id="ip_list"]/tr[%d]/td[2]/text()' % i)[0])


# test_for_new()
