# coding: utf8
from __future__ import print_function, unicode_literals

from core.urls import register_urls
from .views import FileServiceHandler, TestHandler

register_urls(
    (r'/api/v0/file$', FileServiceHandler, {}, 'file_service'),
    (r'/api/v0/file/test$', TestHandler, {}, 'file_service_test'),
)
