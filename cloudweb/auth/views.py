# coding: UTF-8
from __future__ import print_function, unicode_literals
from .models import Account
from core import web
from core.util import helper


class AccountHandler(web.BaseHandler):
    def get(self):
        Account.create_root_if_empty(self.db)
        accounts_count = self.db.query(Account).count()
        self.write('hi, account %d' % accounts_count)


class ProfileHandler(web.BaseHandler):
    def get(self, username):
        user = Account.find_by_user_name(self.db, username)
        if user is None:
            self.flash("Can't find the user %s" % username)
            self.redirect('index')
            return
        data = {
            'user': user,
            'current_user': self.get_current_user(),
        }
        self.render('account/profile.html', **data)


class RegisterHandler(web.BaseHandler):
    def get(self):
        data = {
            'message': self.flash(),
        }
        self.render('site/register.html', **data)

    def post(self):
        username = self.get_body_argument('username')
        email = self.get_body_argument('email')
        password = self.get_body_argument('password')
        if Account.find_by_user_name(self.db, username) is not None:
            self.flash('The user name exists!')
            self.redirect(self.reverse_url('register'))
            return
        if Account.find_by_email(self.db, email) is not None:
            self.flash('The email exists!')
            self.redirect(self.reverse_url('register'))
            return
        account = Account(user_name=username, email=email, full_name=username)
        account.salt = helper.random_str(10)
        account.password = helper.encrypt_password(password, account.salt)
        try:
            self.db.add(account)
            self.db.commit()
            self.flash('Register successfully!')
            self.redirect(self.reverse_url('login'))
        except (Exception,) as e:
            self.flash(str(e))
            self.redirect(self.reverse_url('register'))


class LoginHandler(web.BaseHandler):
    def get(self):
        data = {
            'message': self.flash()
        }
        self.render('site/login.html', **data)

    def post(self):
        Account.create_root_if_empty(self.db)
        email = self.get_body_argument('email')
        password = self.get_body_argument('password')
        account = Account.find_by_user_or_email(self.db, email)
        if account is None:
            self.write("Can't find the user with username/email %s" % email)
            return  # TODO: redirect to login page with flash message
        encrypted_password = helper.encrypt_password(password, account.salt)
        if encrypted_password != account.password:
            self.write("Wrong email or password")
            return
        self.set_current_user(account)
        self.flash('登录成功')
        self.redirect(self.reverse_url('index'))


class LogoutHandler(web.BaseHandler):
    def get(self):
        self.logout()
        self.redirect(self.get_login_url())
