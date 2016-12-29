# -*- coding: utf-8 -*-
import re
from lawliet import Route
from lawliet.tools import SetPath


def tuple_dict(args):
    for i in args:
        set_route(i)


def set_route(r):
    if re.search(r'/', r[1]):
        if SetPath.app_path is None:
            return
        with open(SetPath.app_path+r[1], 'rb') as f:
            output = f.read()
        Route.get_route[r[0]] = ['cache', output]
        return
    if len(r[1].split('.')) == 1:
        r[1] = '__main__.' + r[1]
    import_str = r[1].split('.')[-1]
    from_str = r[1][:-(len(import_str)+1)]
    exec 'from {} import {}'.format(from_str, import_str)
    if len(r) == 2:
        try:
            exec 'mydef={}()'.format(import_str)
            exec "Route.get_route[r[0]] = ['func', {}]".format(import_str)
            exec "Route.post_route[r[0]] = ['func', {}]".format(import_str)
            exec "Route.put_route[r[0]] = ['func', {}]".format(import_str)
        except:
            exec "Route.get_route[r[0]] = ['func_request', {}]".format(import_str)
            exec "Route.post_route[r[0]] = ['func_request', {}]".format(import_str)
            exec "Route.put_route[r[0]] = ['func_request', {}]".format(import_str)
    elif 'AUTO' in r[2]:
        try:
            exec 'mydef={}().get()'.format(import_str)
            exec "Route.get_route[r[0]] = ['func', {}().get]".format(import_str)
        except:
            try:
                exec "Route.get_route[r[0]] = ['func_request', {}().get]".format(import_str)
            except:
                pass
        try:
            exec 'mydef={}().post()'.format(import_str)
            exec "Route.post_route[r[0]] = ['func', {}().post]".format(import_str)
        except:
            try:
                exec "Route.post_route[r[0]] = ['func_request', {}().post]".format(import_str)
            except:
                pass
        try:
            exec 'mydef={}().put()'.format(import_str)
            exec "Route.put_route[r[0]] = ['func', {}().put]".format(import_str)
        except:
            try:
                exec "Route.put_route[r[0]] = ['func_request', {}().put]".format(import_str)
            except:
                pass
    elif len(r) == 3:
        for i in r[2]:
            if i == 'GET':
                try:
                    exec 'mydef={}()'.format(import_str)
                    exec "Route.get_route[r[0]] = ['func', {}]".format(import_str)
                except:
                    exec "Route.get_route[r[0]] = ['func_request', {}]".format(import_str)
            elif i == 'POST':
                try:
                    exec 'mydef={}()'.format(import_str)
                    exec "Route.post_route[r[0]] = ['func', {}]".format(import_str)
                except:
                    exec "Route.post_route[r[0]] = ['func_request', {}]".format(import_str)
            elif i == 'PUT':
                try:
                    exec 'mydef={}()'.format(import_str)
                    exec "Route.put_route[r[0]] = ['func', {}]".format(import_str)
                except:
                    exec "Route.put_route[r[0]] = ['func_request', {}]".format(import_str)

