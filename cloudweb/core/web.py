# coding: UTF-8
from __future__ import print_function, unicode_literals
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from .db import engine
from auth.models import Account
import json


class Application(tornado.web.Application):
    def __init__(self, handlers):
        from .settings import app_settings

        tornado.web.Application.__init__(self, handlers, **app_settings)
        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie('user')
        if not user_id:
            return None
        return self.db.query(Account).get(int(user_id))

    def session(self, key, val=None):
        if val is None:
            return self.get_secure_cookie(key)
        else:
            self.set_secure_cookie(key, val)

    def remove_session(self, key):
        self.set_secure_cookie(key, None)

    def set_current_user(self, user):
        self.set_secure_cookie('user', u'%d' % user.id)

    def logout(self):
        self.clear_cookie('user')

    def get_login_url(self):
        return self.application.reverse_url('login')

    def get_referer_url(self):
        return self.request.headers.get('Referer')

    def flash(self, msg=None, clear=True):
        if msg is None:
            msg = self.get_secure_cookie('flash_message')
            if clear:
                self.clear_cookie('flash_message')
            return msg
        else:
            self.set_secure_cookie('flash_message', msg)
            return msg

    def has_flash_message(self):
        return self.get_secure_cookie('flash_message') is not None

    def get_request_base_url(self):
        """
        get the base url user's browser send, eg. http://abc.com:3456  or https://abc.com
        """
        return '%s://%s' % (self.request.protocol, self.request.host)

    def ajax_response(self, success, data=None, code=0):
        """
        send ajax response with format {success: true/false, data: content, code: error code of type int
        code:
        0: success:
        1: common error code which might be any kind of error
        2: login required or permission denied
        3: login required
        4: permission denied
        [5, ...): other fail error code
        """
        res = {
            'success': success,
            'data': data  # JSON.to_json(data)
        }
        self.write(json.dumps(res))

    def ajax_success(self, data=None, code=0):
        self.ajax_response(True, data, code)

    def ajax_fail(self, data=None, code=1):
        self.ajax_response(False, data, code)


def require_login(func):
    def new_func(self, *args, **kwargs):
        if not self.get_current_user():
            self.redirect(self.get_login_url())
        else:
            func(self, *args, **kwargs)

    return new_func


def ajax_require_login(func):
    """
    check logined, if check failed, send ajax fail response back and stop the request
    """

    def new_func(self, *args, **kwargs):
        if not self.get_current_user():
            self.ajax_fail('Login required!', code=1)
        else:
            func(self, *args, **kwargs)

    return new_func


def basic_authenticated(func):
    """
    TOOD: basic authenticated filter
    """
    return func