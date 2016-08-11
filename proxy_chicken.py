# coding: utf-8
import requests
from  bs4 import BeautifulSoup
from lxml import etree
import model

proxies = {
    'http': ''
}

can_be_use = []


def parse_proxy(proxies_url):
    proxies['http'] = proxies_url
    check = False
    try:
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=5)
        if r and r.status_code == 200:
            print '===========Successful==============='
            print '|| 访问成功 ||----> 耗时: (%f)s  当前IP: (%s) ' % (r.elapsed.total_seconds(), proxies['http'])
            print '===================================='
            can_be_use.append(proxies['http'])
            check = True
    except (requests.ConnectionError, requests.Timeout):
        print '|| 超时 or 代理出错 抛弃 ||----> 当前IP: (%s) ' % proxies['http']
        pass
    except Exception as e:
        print e
        pass
    return check


def get_proxy_ip(page_num):
    print '====================当前 %s 页======================' % page_num
    global can_be_use
    can_be_use = []
    try:
        r = requests.get('http://www.kuaidaili.com/proxylist/%s/' % page_num, timeout=5)
        page = etree.HTML(r.text.lower())
        tb_list = page.xpath('//*[@id="index_free_list"]/table/tbody/tr')
        count = len(tb_list)
        for i in range(1, count + 1):
            ip_address = page.xpath('//*[@id="index_free_list"]/table/tbody/tr[%d]/td[1]/text()' % i)[0]
            ip_port = page.xpath('//*[@id="index_free_list"]/table/tbody/tr[%d]/td[2]/text()' % i)[0]
            url = "http://" + ip_address + ":" + ip_port
            # print url
            parse_proxy(url)
        print '=================================================='
    except Exception as e:
        print e
        pass


def get_list():
    return can_be_use
