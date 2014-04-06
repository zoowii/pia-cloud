# coding: utf8
# 从下载队列中读取要下载的内容，下载后触发hook
# 存储到本地，也可以存储到mongodb fs中
from __future__ import print_function, unicode_literals
import time
import os
import sys
from file_backend import settings
from file_backend import mongo_util
import requests
import random
import string


def random_str(n=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, n))


def worker_process():
    col = mongo_util.get_mongo_db()['file_request']
    record = col.find_one({'state': 'not_processed'})
    if record is None:
        return
    url = record['url']
    res = requests.get(url)
    filepath = os.path.join(settings.DATA_DIR, str(record['_id']))
    f = open(filepath, 'wb')
    f.write(res.content)
    f.close()
    record['state'] = 'downloaded'
    col.save(record)
    callback = record['callback']
    requests.get(callback, params={
        'file_id': str(record['_id']),
        'request_id': str(record['_id']),
    })


def loop():
    while True:
        try:
            worker_process()
            print('downloader process once')
        except (Exception, ) as e:
            print(e)
        time.sleep(2)


if __name__ == '__main__':
    print('start download loop')
    loop()