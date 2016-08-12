# coding: utf-8
import time

import model
import proxy_chicken
import logging


def check_save_proxy():
    logging.getLogger(__name__)
    logging.info('========寻找代理启动==========')
    proxy_chicken.pool_load()
    logging.info('===========存储完毕===========')


def check_delete_proxy():
    logging.info('===========检查启动===========')
    for i in model.query_proxy():
        if proxy_chicken.parse_proxy(i) is False:
            model.delete_proxy(i)
    logging.info('===========再检完毕===========')


check_save_proxy()
