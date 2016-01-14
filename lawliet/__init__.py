# -*- coding: utf-8 -*-
__author__ = 'monomer'
from .app import Route

class Routes(object):
    def __init__(self, *args):
        Route.urls = args

def response(res_str, types):
    return [res_str, types]
