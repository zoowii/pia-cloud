# coding: utf8
from __future__ import print_function, unicode_literals

from core.urls import register_urls
from .views import IndexHandler, SqlHandler

register_urls(
    (r'/datastore/v0$', IndexHandler, {}, 'datastore_index'),
    (r'/datastore/v0/sql$', SqlHandler, {}, 'datastore_sql'),
)
