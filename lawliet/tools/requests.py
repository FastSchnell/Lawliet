# -*- coding: utf-8 -*-

import json as python_json
import httplib
import gzip
import StringIO


from lawliet.exc import (
    RequestsUrlError,
)


def _unicode2str(uni):
    if isinstance(uni, unicode):
        return uni.encode('utf-8')
    else:
        return uni


def urlencode(kwargs):
    return '&'.join([
        _unicode2str(k) + '=' + _unicode2str(v)
        for k, v in kwargs.items()
    ])


def _split_url(url):
    """

    :param url:
    :return:
     host
     port
     path
     secure
    """
    if url:
        protocol_l = url.split('//')
        protocol = protocol_l.pop(0)

        if protocol == 'http:':
            secure = False
        elif protocol == 'https:':
            secure = True
        else:
            raise RequestsUrlError('Invalid URL %s' % url)

        enpoint_l = ''.join(protocol_l).split('/')
        host_port = enpoint_l.pop(0)
        path = '/' + '/'.join(enpoint_l)

        if ':' in host_port:
            host, port = host_port.split(':')
        else:
            host = host_port
            port = None
        return host, port, path, secure

    else:
        raise RequestsUrlError()


class RequestsResponse(object):

    def __init__(self, response):
        self.response = response

    def json(self):
        if self.headers.get('content-encoding') == 'gzip':
            return python_json.loads(gzip.GzipFile(fileobj=StringIO.StringIO(self.response.read())).read())
        else:
            return python_json.loads(self.response.read())

    @property
    def content(self):
        if self.headers.get('content-encoding') == 'gzip':
            return gzip.GzipFile(fileobj=StringIO.StringIO(self.response.read())).read()
        else:
            return self.response.read()

    @property
    def status_code(self):
        return self.response.status

    @property
    def headers(self):
        return {k: v for k, v in self.response.getheaders()}


class Requests(object):

    @staticmethod
    def get(url, params=None, headers=None, timeout=None):
        host, port, path, secure = _split_url(url)
        if secure:
            http = httplib.HTTPSConnection(host=host, port=port, timeout=timeout)
        else:
            http = httplib.HTTPConnection(host=host, port=port, timeout=timeout)
        if params:
            path += '?%s' % urlencode(params)

        if headers:
            headers['accept'] = '*/*'
            headers.update({
                'accept': '*/*',
                'connection': 'keep-alive',
            })
        else:
            headers = {
                'accept': '*/*',
                'connection': 'keep-alive',
            }

        http.request(method='GET', url=path, body=None, headers=headers)
        return RequestsResponse(http.getresponse())

    @staticmethod
    def post(url, params=None, json=None, data=None, headers=None, timeout=None):
        host, port, path, secure = _split_url(url)
        if secure:
            http = httplib.HTTPSConnection(host=host, port=port, timeout=timeout)
        else:
            http = httplib.HTTPConnection(host=host, port=port, timeout=timeout)

        if json:
            body = python_json.dumps(json)
            headers = {'content-type': 'application/json'}
        elif data:
            body = data
        else:
            body = None

        if params:
            path += '?%s' % urlencode(params)

        http.request(method='POST', url=path, body=body, headers=headers or {})
        return RequestsResponse(http.getresponse())

    @staticmethod
    def delete(url, params=None, json=None, data=None, headers=None, timeout=None):
        host, port, path, secure = _split_url(url)
        if secure:
            http = httplib.HTTPSConnection(host=host, port=port, timeout=timeout)
        else:
            http = httplib.HTTPConnection(host=host, port=port, timeout=timeout)
        if json:
            body = python_json.dumps(json)
            headers = {'content-type': 'application/json'}
        elif data:
            body = data
        else:
            body = None

        if params:
            path += '?%s' % urlencode(params)

        http.request(method='DELETE', url=path, body=body, headers=headers or {})
        return RequestsResponse(http.getresponse())

    @staticmethod
    def put(url, params=None, json=None, data=None, headers=None, timeout=None):
        host, port, path, secure = _split_url(url)
        if secure:
            http = httplib.HTTPSConnection(host=host, port=port, timeout=timeout)
        else:
            http = httplib.HTTPConnection(host=host, port=port, timeout=timeout)
        if json:
            body = python_json.dumps(json)
            headers = {'content-type': 'application/json'}
        elif data:
            body = data
        else:
            body = None

        if params:
            path += '?%s' % urlencode(params)

        http.request(method='PUT', url=path, body=body, headers=headers or {})
        return RequestsResponse(http.getresponse())
