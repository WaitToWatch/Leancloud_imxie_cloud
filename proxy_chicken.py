# coding: utf-8
from multiprocessing import Pool as ThreadPool

import time

import requests
from lxml import etree
import model
import logging

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger_proxy.log', level=logging.INFO)
logger = logging.getLogger(__name__)

header_info = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Content-Type': 'text/html; charset=utf-8'
}

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
    try:
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=5, headers=header_info)
        if r and r.status_code == 200:
            logging.info('===========Successful===============')
            logging.info('|| 访问成功 ||----> 耗时: (%f)s  当前IP: (%s) ' % (r.elapsed.total_seconds(), proxies_url))
            logging.info('====================================')
            # can_be_use.append(proxies['http'])
            model.save_proxy(proxies_url)
            check = True
    except (requests.ConnectionError, requests.Timeout):
        logging.info(u'|| 超时 or 代理出错 抛弃 ||----> 当前IP: (%s) ' % proxies_url)
        pass
    except Exception as e:
        logging.warn(e)
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
            r = requests.get(url=url, timeout=5, headers=header_info)
            page = etree.HTML(r.text)
            tb_list = page.xpath(item.xp_count)
            count = len(tb_list)
            if count == 0:
                logging.warn('当前长度有问题,网址是: (%s)' % url)
                raise requests.HTTPError
            for i in range(1, count):
                if page.xpath(item.xp_tb1 % i) and page.xpath(item.xp_tb2 % i) != 0:
                    ip_address = page.xpath(item.xp_tb1 % i)[0]
                    ip_port = page.xpath(item.xp_tb2 % i)[0]
                    if ip_address and ip_port is not None:
                        parse_proxy('http://%s:%s' % (ip_address, ip_port))
                        # print '=================================================='
        except Exception as e:
            logging.warn("get_proxy_ip报错:")
            logging.warn(e)
            pass


def get_list():
    return can_be_use


def pool_load():
    logging.info(time.strftime('|| 运行时间: %Y-%m-%d (%H:%M)', time.localtime(time.time())))
    global proxy_index
    global proxy_list
    proxy_list = model.query_proxy_item()

    print "当前有 %d 实例" % len(proxy_list)

    for item in proxy_list:
        if isinstance(item, model.Proxy_Item):
            pool = ThreadPool(4)
            logging.info(u'==============当前访问的是 Host %s==============' % item.host)
            pool.map(get_proxy_ip, item.urls)
            pool.close()  # 这就结束了
            pool.join()
            # for url in item.urls:
            #     get_proxy_ip(url)
            proxy_index += 1
