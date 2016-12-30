# -*- coding: utf-8 -*-
from .app import Route
from .handler.response import response
from .handler.route_dict import tuple_dict
from .tools.cache import DoCache
from .tools.private_cache import PrivateCache
from .tools.json_loads import str_json
from .handler.db import (
    InitSession,
    LawSession,
)


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


def jsons(data):
    return str_json(data)


class Routes(object):
    def __init__(self, *args):
        tuple_dict(args)


class Cache(DoCache):
    pass


class _Cache(PrivateCache):
    pass


class DBSession(LawSession):
    @classmethod
    def init_session(cls, db_session, exc):
        InitSession.db_session = db_session
        InitSession.exc = exc
