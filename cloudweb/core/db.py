# coding: UTF-8
from __future__ import print_function, unicode_literals

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from . import settings

engine = create_engine(settings.DATABASE['default'], echo=settings.echo_sql)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def create_all():
    metadata = Base.metadata
    metadata.create_all(engine)