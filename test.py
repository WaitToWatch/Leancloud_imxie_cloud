# coding: utf-8
import model
import proxy_chicken
import cloud


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

