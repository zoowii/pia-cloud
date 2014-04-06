# coding: UTF-8
from __future__ import print_function, unicode_literals
from core import web
import json
from core.util import mongo_util
from cloudsql import engine


class IndexHandler(web.BaseHandler):
    @web.require_login
    def get(self):
        self.render('datastore/index.html', message=self.flash())


class SqlHandler(web.BaseHandler):
    @web.ajax_require_login
    def post(self):
        sql = self.get_body_argument('sql')
        db_name = self.get_body_argument('database', None)
        datastore_session = engine.Session()
        datastore_session.change_db(db_name)
        res = engine.squeal(datastore_session, sql)
        self.ajax_success({
            'database': datastore_session.get_db_name(),
            'result': res,
        })