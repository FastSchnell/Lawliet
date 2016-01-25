# -*- coding: utf-8 -*-
__author__ = 'monomer'
from .app import Route
from .handler.response import Res
from .tools.json_loads import str_json


def Response(res=None, status=None, headers=None):
    return Res(res, status, headers).response()


def abort(code, res=None):
    if code == 404:
        res = {"errcode": 404, "errmsg": "page not find"}
    elif code == 500:
        res = {"errcode": 500, "errmsg": "page error"}
    return Response(res=res, status=code)


def redirect(url):
    return Response(status=301, headers={"Location": url})


def jsons(str):
    return str_json(str)


class Routes(object):
    def __init__(self, *args):
        Route.urls = args