# -*- coding: utf-8 -*-
from os import path


class SetPath(object):
    app_path = ''

    @classmethod
    def run(cls, __file__):
        cls.app_path = path.dirname(__file__) + '/'

