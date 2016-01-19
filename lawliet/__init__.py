# -*- coding: utf-8 -*-
__author__ = 'monomer'
from .app import Route


def Response(res=None, status=None, headers=None):
    dict_res = dict()
    if res is not None:
        dict_res['res'] = res
    if status is not None:
        if type(status) == type(1):
            status = '{} '.format(status)
        dict_res['status'] = status
    if headers is not None:
        for i in headers:
            new_headers = list()
            new_headers.append((i, headers[i]))
        dict_res['headers'] = new_headers
    return [dict_res]


class Routes(object):
    def __init__(self, *args):
        Route.urls = args