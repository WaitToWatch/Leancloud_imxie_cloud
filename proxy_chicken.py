# coding: utf-8
import requests
from  bs4 import BeautifulSoup
from lxml import etree
import one_save_email

proxies = {
    'http': ''
}

can_be_use = []


def parse_proxy(proxies):
    try:
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=5)
        if r and r.status_code == 200:
            print '===========Successful==============='
            print '当前IP: (%s)  耗时: (%d)s' % (proxies['http'], r.elapsed.total_seconds())
            print '===================================='
            can_be_use.append(proxies['http'])
    except Exception as e:
        print e
        pass


def get_proxy_ip(page_num):
    try:
        r = requests.get('http://www.kuaidaili.com/proxylist/%s/' % page_num, timeout=5)
        page = etree.HTML(r.text.lower())
        tb_list = page.xpath('//*[@id="index_free_list"]/table/tbody/tr')
        count = len(tb_list)
        # 第一栏 //*[@id="index_free_list"]/table/tbody/tr[1]/td[1] tb[2]
        # 第二栏 //*[@id="index_free_list"]/table/tbody/tr[2]/td[1] tb[2]
        for i in range(1, count + 1):
            ip_address = page.xpath('//*[@id="index_free_list"]/table/tbody/tr[%d]/td[1]/text()' % i)[0]
            ip_port = page.xpath('//*[@id="index_free_list"]/table/tbody/tr[%d]/td[2]/text()' % i)[0]
            url = "http://" + ip_address + ":" + ip_port
            print url
            proxies['http'] = url
            parse_proxy(proxies)
        print '====================下一页======================='
    except Exception as e:
        print e


def get_list():
    return can_be_use
