# coding: UTF-8
from __future__ import print_function, unicode_literals
from core import web
import json
from core.util import mongo_util


class FileServiceHandler(web.BaseHandler):
    """
    demo 只提供离线下载功能
    demo不需要认证
    直接GET请求，读入一个下载链接（暂时不支持需要登录的下载地址），文件名，回调地址
    返回一个json，内容是请求ID
    回调的格式是传入成功信息，请求ID和文件ID
    """

    def get(self):
        """
        存入请求到mongodb中，格式是：
        url, filename, callback, state
        """
        url = self.get_argument('url', None)
        if url is None:
            self.render('file_service/form.html', message=self.flash())
            return
        filename = self.get_argument('filename')
        callback = self.get_argument('callback')
        db = mongo_util.get_mongo_db()
        col = db['file_request']
        data = {
            'url': url,
            'filename': filename,
            'callback': callback,
            'state': 'not_processed',
        }
        req_id = col.insert(data)
        self.ajax_success(str(req_id))


class TestHandler(web.BaseHandler):
    """
    测试file service的回调的
    暂时用get请求
    """

    def get(self):
        file_id = self.get_argument('file_id')
        req_id = self.get_argument('request_id')
        db = mongo_util.get_mongo_db()
        col = db['file_callback_test']
        data = {
            'file_id': file_id,
            'request_id': req_id,
        }
        col.insert(data)
        self.ajax_success(file_id)
