# -*- coding: utf-8 -*-
__author__ = 'monomer'
from .app import Route
from .request import get_input

class Routes(object):
    def __init__(self, *args):
        Route.urls = args

class Request(object):

    def headers(self, param):
        pass

    def get(self, param):
        pass

    def data(self):
        pass




def response(res_str, types):
    return [res_str, types]
