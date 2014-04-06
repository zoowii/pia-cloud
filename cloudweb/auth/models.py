# coding: UTF-8
from __future__ import print_function, unicode_literals
from core.db import Base, Column, Integer, String, Boolean, DateTime
from datetime import datetime
from core.util import helper
from core import settings


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, default=1, nullable=False)
    created_time = Column(DateTime(), default=datetime.now, nullable=False)
    user_name = Column(String(50), nullable=False, unique=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    salt = Column(String(50), nullable=False)
    is_admin = Column(Boolean(), nullable=False, default=False)
    url = Column(String(50))
    updated_time = Column(DateTime(), nullable=True, default=None)
    last_login_time = Column(DateTime(), nullable=False, default=datetime.now)
    last_login_ip = Column(String(50), nullable=True)
    image = Column(String(200))
    is_group_account = Column(Boolean(), default=False)
    removed = Column(Boolean(), default=False)

    def __unicode__(self):
        return u'<Account %s>' % self.user_name

    def __repr__(self):
        return self.__unicode__().encode('utf8')

    def get_image_url(self):
        if self.image is not None:
            return self.image  # the image should store in third party service
        else:
            return settings.DEFAULT_USER_AVATAR

    @staticmethod
    def find_by_user_name(db, user_name):
        return db.query(Account).filter_by(user_name=user_name, is_group_account=False, removed=False).first()

    @staticmethod
    def find_by_email(db, email):
        return db.query(Account).filter_by(email=email, is_group_account=False, removed=False).first()

    @staticmethod
    def find_by_user_or_email(db, username):
        return Account.find_by_user_name(db, username) or Account.find_by_email(db, username)

    @staticmethod
    def create_root_if_empty(db):
        """
        create root user if there are no accounts
        """
        account = db.query(Account).first()
        if account is not None:
            return
        username = 'root'
        password = 'root'
        account = Account(user_name=username, full_name=username, email='root@localhost', is_admin=True)
        account.salt = helper.random_str(10)
        account.password = helper.encrypt_password(password, account.salt)
        db.add(account)
        db.commit()


account_table = Account.__table__
