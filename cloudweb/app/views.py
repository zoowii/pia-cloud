# coding: UTF-8
from __future__ import print_function, unicode_literals
from core import web


class IndexHandler(web.BaseHandler):
    @web.require_login
    def get(self):
        user = self.get_current_user()
        data = {
            'user': user,
            'message': self.flash(),
        }
        self.render('site/index.html', **data)