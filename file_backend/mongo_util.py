# coding: utf8
from __future__ import print_function
import settings
import pymongo


def get_mongo_db():
    client = pymongo.MongoClient('mongodb://%s:%s@%s:%d/%s' % (
        settings.MONGO['user'], settings.MONGO['pass'], settings.MONGO['host'], settings.MONGO['port'], settings.MONGO['database']))
    return client[settings.MONGO['database']]

