# -*- coding: utf-8 -*-
from .app import Route
from .handler.response import response
from .handler.route_dict import tuple_dict
from .tools.cache import DoCache
from .tools._cache import _DoCache
from .tools.json_loads import str_json


def Response(res=None, status=None, headers=None):
    response(res, status, headers)


def abort(code, res=None):
    if code == 404:
        res = {"errcode": 404, "errmsg": "page not find"}
    elif code == 500:
        res = {"errcode": 500, "errmsg": "page error"}
    Response(res=res, status=code)


def redirect(url):
    Response(status=301, headers={"Location": url})


def jsons(str):
    return str_json(str)


class Routes(object):
    def __init__(self, *args):
        tuple_dict(args)


class Cache(DoCache):
    pass


class _Cache(_DoCache):
    pass
