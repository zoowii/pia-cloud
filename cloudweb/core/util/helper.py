# coding: UTF-8
from __future__ import print_function, unicode_literals
import random
import string
import hashlib
import os


def encrypt_password(password, salt):
    salt = salt.strip().encode('UTF-8')
    password = password.strip().encode('UTF-8')
    p1 = hashlib.sha256(password).hexdigest()
    p2 = p1.encode('UTF-8') + salt
    return hashlib.sha256(p2).hexdigest()


def random_str(length=20):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:length])


def split_path(path):
    """
    split path to list of items
    eg. /Users/abc/test.txt would be splited to ['Users', 'abc', 'test.txt']
    """
    items = []
    while True:
        path, folder = os.path.split(path)
        if folder != '':
            items.append(folder)
        else:
            if path != '':
                items.append(path)
            break
    items.reverse()
    return items


def get_server_address(request):
    from .. import settings

    if settings.SERVER_HOST is not None:
        return settings.SERVER_HOST
    host = request.host
    if host.find(':') > 0:
        host = host[:host.find(':')]
    return host


def list_strip(lst):
    return filter(lambda x: len(x) > 0, map(lambda x: x.strip(), lst))