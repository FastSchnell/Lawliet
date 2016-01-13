#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server

routes = [
    ('/ping', 'ping.views.ping')
]


class app_1:
    "这是一个web框架"
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        for r in routes:
            if path == r[0]:
                if len(r) == 2 or method in r[2]:
                    try:
                        import_str = r[1].split('.')[-1]
                        from_str = r[1][:-(len(import_str)+1)]
                        print import_str
                        print from_str
                        exec 'from {} import {}'.format(from_str, import_str)
                        exec 'mydef={}()'.format(import_str)
                        return self.res_text(mydef)
                    except:
                        return self.error_code()
                else:
                    return self.method_not_allowed()
            else:
                return self.notfound()

    def res_text(self, res):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield res

    def error_code(self):
        status = '500 INTERNAL SERVER ERROR'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 500, "errmsg": "page error"}'

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 404, "errmsg": "page not find"}'

    def method_not_allowed(self):
        status = '405 METHOD NOT ALLOWED'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 405, "errmsg": "Method Not Allowed"}'

httpd = make_server('', 5001, app_1)
sa = httpd.socket.getsockname()
print u'跑起来了http://{0}:{1}/'.format(*sa)
httpd.serve_forever()
