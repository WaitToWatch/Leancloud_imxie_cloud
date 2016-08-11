# coding: utf-8
from multiprocessing import Pool as ThreadPool

import requests
from  bs4 import BeautifulSoup
from lxml import etree
import model

proxies = {
    'http': ''
}

urls = []
can_be_use = []
proxy_list = []
proxy_index = 0


def parse_proxy(proxies_url):
    proxies['http'] = proxies_url
    check = False
    global can_be_use
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


def get_proxy_ip(url):
    # page_num = url[34:]
    #
    # print '====================当前 %s 页======================' % page_num
    global proxy_list
    global proxy_index

    if len(proxy_list) == 0:
        proxy_list = model.query_proxy_item()
    item = proxy_list[proxy_index]

    if isinstance(item, model.Proxy_Item):
        try:
            r = requests.get(url=url, timeout=5)
            page = etree.HTML(r.text.lower())
            tb_list = page.xpath(item.xp_count)
            count = len(tb_list)
            for i in range(1, count + 1):
                ip_address = page.xpath(item.xp_tb1 % i)[0]
                ip_port = page.xpath(item.xp_tb2 % i)[0]

                if ip_address and ip_port is not None:
                    parse_proxy('http://%s:%s' % (ip_address, ip_port))
                    # print '=================================================='
        except Exception as e:
            print e
            pass


def get_list():
    global can_be_use
    return can_be_use


def pool_load():
    global proxy_index
    global proxy_list
    proxy_list = model.query_proxy_item()
    for item in proxy_list:
        if isinstance(item, model.Proxy_Item):
            pool = ThreadPool(4)
            print u'==============当前访问的是 Host %s==============' % item.host
            pool.map(get_proxy_ip, item.urls)
            pool.close()  # 这就结束了
            pool.join()
            proxy_index += 1
