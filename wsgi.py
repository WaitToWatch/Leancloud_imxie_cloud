# -*- coding: utf-8 -*-


from gevent import monkey
import os

import leancloud
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import app
from cloud import Engine
from leancloud import HttpsRedirectMiddleware

monkey.patch_all()

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])

leancloud.init(APP_ID, master_key=MASTER_KEY)

# app 为您的 wsgi 函数
app = HttpsRedirectMiddleware(app)
engine = Engine(app)
application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = WSGIServer(('localhost', PORT), application, handler_class=WebSocketHandler)
    server.serve_forever()
