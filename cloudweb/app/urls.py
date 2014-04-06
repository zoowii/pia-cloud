# coding: utf8
from __future__ import print_function, unicode_literals

from core.urls import register_urls
from .views import IndexHandler

register_urls(
    (r'/', IndexHandler, {}, 'index'),
)
