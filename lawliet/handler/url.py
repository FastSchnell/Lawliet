# -*- coding: utf-8 -*-
import inspect

from lawliet.app import Route

route_mapping = {
    'GET': Route.get_route,
    'POST': Route.post_route,
    'PUT': Route.put_route
}


class FuncArgsMaxError(Exception):
    pass


class UrlSetError(Exception):
    pass


def _set_path(url_path, func, method):
    func_args_len = len(inspect.getargspec(func).args)
    if func_args_len == 0:
        func_type = 'func'
    elif func_args_len == 1:
        func_type = 'func_request'
    else:
        raise FuncArgsMaxError()
    if isinstance(method, str):
        method = [method]
    elif not isinstance(method, (list, tuple)):
        raise Exception("method is not a list, like this:['GET']")
    for value in method:
        try:
            route_mapping[value.upper()][url_path] = [func_type, func]
        except KeyError:
            raise KeyError('method is not in [GET, POST, PUT]')


def set_route(args):
    try:
        for arg in args:
            if len(arg) != 3:
                raise Exception('len(arg) != 3')
            _set_path(*arg)
    except Exception as e:
        raise UrlSetError(repr(e))

