# coding: utf-8
import time

import model
import proxy_chicken


def check_save_proxy():
    print time.strftime('%Y-%m-%d (%H:%M)', time.localtime(time.time()))
    # # 保持我的池子活着 5 个代理
    # if len(model.query_proxy()) < 5:
    print '========寻找代理启动=========='
    proxy_chicken.pool_load()
    print '===========存储完毕==========='
    # check_delete_proxy()


def check_delete_proxy():
    print '===========检查启动==========='
    for i in model.query_proxy():
        if proxy_chicken.parse_proxy(i) is False:
            model.delete_proxy(i)
    print '===========再检完毕==========='


check_save_proxy()
