# -*- coding: utf-8 -*-
from .app import Route
from .handler.response import response
from .handler.route_dict import tuple_dict
from .tools.cache import DoCache
from .tools.private_cache import PrivateCache
from .tools.json_loads import str_json
from .tools.requests import Requests
from .handler.db import LawSession
from .handler.url import set_route


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


def json(data):
    return str_json(data)


class Routes(object):
    def __init__(self, *args):
        tuple_dict(args)


class Url(object):
    def __init__(self, *args):
        set_route(args)


class Cache(DoCache):
    pass


class _Cache(PrivateCache):
    pass


class DBSession(LawSession):
    @classmethod
    def init_all(cls, db_session, exc):
        cls.init_session = db_session
        cls.init_exc = exc

requests = Requests()  # fake python_requests
