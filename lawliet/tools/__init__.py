# -*- coding: utf-8 -*-
from os import path
from hello_world import Hello


class SetPath(object):
    app_path = ''

    @classmethod
    def run(cls, __file__):
        cls.app_path = path.dirname(__file__) + '/'


def hello(content=None, url=None,
          host=None, port=None):
    Hello(content, url, host, port).run()
