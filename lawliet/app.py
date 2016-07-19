# -*- coding: utf-8 -*-
import json
from .request import Request
from .handler.response import LawDict


class Route(object):
    """这是url调度功能"""
    debug = False
    get_route = dict()
    post_route = dict()
    put_route = dict()

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        try:
            try:
                if method == 'GET':
                    route_list = self.get_route[path]
                elif method == 'POST':
                    route_list = self.post_route[path]
                elif method == 'PUT':
                    route_list = self.put_route[path]
                else:
                    return self.method_not_allowed()
            except:
                return self.not_found()
            request = Request(self.environ)
            func_name = route_list[0]
            if func_name == 'func_request':
                mydef = route_list[1](request)
            elif func_name == 'func':
                mydef = route_list[1]()
            elif func_name == 'cache':
                static_type = path.split('.')[-1]
                if static_type == 'css':
                    header = [('Content-type', 'text/css')]
                elif static_type == 'html':
                    header = [('Content-type', 'text/html')]
                elif static_type == 'js':
                    header = [('Content-type', 'text/javascript')]
                else:
                    header = [('Content-type', 'text/plain')]
                return self.res_text(str(self.get_route[path][1]), headers=header)
            else:
                raise

            if type(mydef) is type(dict):
                return self.res_text(json.dumps(mydef),
                                     headers=[('Content-type', 'application/json')])

            elif type(mydef) is type(LawDict()):
                try:
                    res = mydef['res']
                except:
                    res = None
                try:
                    status = mydef['status']
                except:
                    status = None
                try:
                    headers = mydef['headers']
                except:
                    headers = None
                return self.res_text(res, status, headers)
            else:
                return self.res_text(mydef)
        except Exception as e:
            if self.debug in [False, '', None]:
                return self.error_code()
            else:
                return self.res_text(repr(e))

    def res_text(self, res=None, status=None, headers=None):
        if status is None:
            status = '200 OK'
        if headers is None:
            if isinstance(res, dict):
                res = json.dumps(res)
                headers = [('Content-type', 'application/json')]
            else:
                headers = [('Content-type', 'text/plain')]
        self.start(status, headers)
        if res is None:
            yield ''
        else:
            if isinstance(res, unicode):
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
