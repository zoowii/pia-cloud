# coding: utf8
from __future__ import print_function, unicode_literals


class UrlPatterns(object):
    def __init__(self, url_patterns):
        self.urls = url_patterns


def include(sub_urls):
    return UrlPatterns(urls(sub_urls))


def urls(*sub_urls):
    res = []
    for item in sub_urls:
        if isinstance(item, UrlPatterns):
            res.extend(urls(*item.urls))
        else:
            res.append(item)
    return res


def make_urls(*sub_urls):
    return UrlPatterns(sub_urls)


def export(*sub_urls):
    register_urls(make_urls(sub_urls))


all_urls = []


def register_urls(*app_urls):
    global all_urls
    all_urls.append(make_urls(*app_urls))


_installed_apps_loaded = False


def load_installed_apps_urls():
    if _installed_apps_loaded:
        return
    from core.settings import INSTALLED_APPS

    for app_name in INSTALLED_APPS:
        __import__('%s.urls' % app_name)


def get_urls():
    load_installed_apps_urls()
    global all_urls
    return urls(*all_urls)