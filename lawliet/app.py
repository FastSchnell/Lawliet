# -*- coding: utf-8 -*-
import json
import logging
from .request import Request
from .handler.response import Response

logger = logging.getLogger(__name__)


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
            except KeyError:
                return self.not_found()
            func_type = route_list[0]
            if func_type == 'func_request':
                request = Request(self.environ)
                func = route_list[1](request)
            elif func_type == 'func':
                func = route_list[1]()
            elif func_type == 'cache':
                static_type = path.split('.')[-1]
                if static_type == 'css':
                    header = [('Content-type', 'text/css')]
                elif static_type == 'html':
                    header = [('Content-type', 'text/html')]
                elif static_type == 'js':
                    header = [('Content-type', 'text/javascript')]
                else:
                    header = [('Content-type', 'text/plain')]
                return self.response(str(self.get_route[path][1]), headers=header)
            else:
                raise

            if type(func) is type(dict):
                return self.response(
                    json.dumps(func),
                    headers=[('Content-type', 'application/json')]
                )
            else:
                return self.response(func)

        except Response as e:
            func = e.response()
            res = func.get('res', None)
            status = func.get('status', None)
            headers = func.get('headers', None)
            return self.response(res, status, headers)

        except Exception as e:
            logger.exception(repr(e))
            if not self.debug:
                return self.server_error()
            else:
                return self.response(repr(e))

    def response(self, res=None, status=None, headers=None):
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
            elif isinstance(res, (int, float, long)):
                res = str(res)
            yield res

    def server_error(self):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 500, "errmsg": "page error"}'

    def not_found(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'application/json')]
        self.start(status, response_headers)
        yield '{"errcode": 404, "errmsg": "page not find"}'

    def method_not_allowed(self):
        status = '405 Method Not Allowed'
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
