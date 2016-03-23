# -*- coding: utf-8 -*-
import json
from .request import Request


class Route(object):
    """这是url调度功能"""
    debug = False
    urls = tuple()

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']

        #print self.environ

        for r in self.urls:
            if path == r[0]:
                if len(r) == 2 or method in r[2] or 'AUTO' in r[2]:
                    try:
                        import_str = r[1].split('.')[-1]
                        from_str = r[1][:-(len(import_str)+1)]
                        if len(r) == 2 or method in r[2]:
                            exec 'from {} import {}'.format(from_str, import_str)
                            try:
                                request = Request(self.environ)
                                exec 'mydef={}(request)'.format(import_str)
                            except:

                                exec 'mydef={}()'.format(import_str)
                        elif 'AUTO' in r[2]:
                            if method == 'GET':
                                input_def = 'get'
                            elif method == 'POST':
                                input_def = 'post'
                            elif method == 'PUT':
                                input_def = 'put'
                            exec 'from {} import {}'.format(from_str, import_str)
                            try:
                                request = Request(self.environ)
                                exec 'mydef={}().{}(request)'.format(import_str, input_def)

                            except:

                                exec 'mydef={}().{}()'.format(import_str, input_def)
                        try:
                            if type(mydef) == type({}):
                                return self.res_text(json.dumps(mydef), headers=[('Content-type', 'application/json')])
                        except:
                            pass
                        try:
                            if type(mydef) == type([]):
                                try:
                                    res = mydef[0]['res']
                                except:
                                    res = None
                                try:
                                    status = mydef[0]['status']
                                except:
                                    status = None
                                try:
                                    headers = mydef[0]['headers']
                                except:
                                    headers = None
                                return self.res_text(res, status, headers)
                        except:
                            pass
                        return self.res_text(mydef)
                    except Exception as e:
                        if self.debug in [False, '', None]:
                            return self.error_code()
                        else:
                            return self.res_text(str(e))
                else:
                    return self.method_not_allowed()
        return self.not_found()

    def res_text(self, res=None, status=None, headers=None):
        if status is None:
            status='200 OK'
        if headers is None:
            if type(res) == type({}):
                res = json.dumps(res)
                headers=[('Content-type', 'application/json')]
            else:
                headers=[('Content-type', 'text/plain')]
        self.start(status, headers)
        if res is None:
            yield ''
        else:
            if type(unicode()) == type(res):
                res = res.encode('utf-8')
            yield res

    def error_code(self):
        status = '500 INTERNAL SERVER ERROR'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 500, "errmsg": "page error"}'

    def not_found(self):
        status = '404 NOT FOUND'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 404, "errmsg": "page not find"}'

    def method_not_allowed(self):
        status = '405 METHOD NOT ALLOWED'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 405, "errmsg": "Method Not Allowed"}'


def run(host=None, port=None):
    if host is None:
        host = '127.0.0.1'
    if port is None:
        port = 5000
    from wsgiref.simple_server import make_server
    httpd = make_server(host, port, Route)
    sa = httpd.socket.getsockname()
    print 'running ==> http://{0}:{1}/'.format(*sa)
    httpd.serve_forever()
