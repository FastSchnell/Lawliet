# -*- coding: utf-8 -*-
__author__ = 'monomer'
from .app import Route
status_dict = {400: '400 BAD REQUEST', 403: '403 FORBIDDEN', 404: '404 NOT FOUND', 405: '405 METHOD NOT ALLOWED', 500: '500 INTERNAL SERVER ERROR'}

def Response(res=None, status=None, headers=None):
    dict_res = dict()
    if res is not None:
        dict_res['res'] = res
    if status is not None:
        if type(status) == type(1):
            if status in status_dict:
                status = status_dict[status]
            else:
                status = '{} '.format(status)
        dict_res['status'] = status
    if headers is not None:
        for i in headers:
            new_headers = list()
            new_headers.append((i, headers[i]))
        dict_res['headers'] = new_headers
    return [dict_res]


def abort(code, res=None):
    if code == 404:
        res = {"errcode": 404, "errmsg": "page not find"}
    elif code == 500:
        res = {"errcode": 500, "errmsg": "page error"}
    return Response(res=res, status=code)

def redirect(url):
    return Response(status=301, headers={"Location": url})


class Routes(object):
    def __init__(self, *args):
        Route.urls = args