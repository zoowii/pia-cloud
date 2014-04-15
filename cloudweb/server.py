# coding: utf8
from __future__ import print_function, unicode_literals
from app.application import app
import os


if __name__ == "__main__":
    import tornado.ioloop

    port = int(os.environ.get('PORT', '8888'))
    app.listen(port)
    print('server started at http://localhost:%d' % port)
    tornado.ioloop.IOLoop.instance().start()
