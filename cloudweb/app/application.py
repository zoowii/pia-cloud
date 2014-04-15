# coding: UTF-8
from __future__ import print_function, unicode_literals
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'site-packages'))
from core import web
from . import db

from core.urls import get_urls

app = web.Application(get_urls())
