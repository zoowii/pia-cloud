# coding: utf8
from __future__ import print_function, unicode_literals
from .views import AccountHandler, LoginHandler, LogoutHandler, ProfileHandler, RegisterHandler
from core.urls import register_urls

register_urls(
    (r'/login$', LoginHandler, {}, 'login'),
    (r'/logout$', LogoutHandler, {}, 'logout'),
    (r'/account$', AccountHandler, {}, 'account'),
    (r'/register$', RegisterHandler, {}, 'register'),
)