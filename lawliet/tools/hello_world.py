# -*- coding: utf-8 -*-
from lawliet import app
from lawliet.app import Route


class Hello(object):

    def __init__(self, content=None, url_path=None,
                 host=None, port=None):
        self.content = content or 'Hello World !'
        self.url_path = url_path or '/'
        self.host = host or '127.0.0.1'
        self.port = port or 5000

    def index(self):
        return self.content

    def run(self):
        Route.get_route[self.url_path] = ['func', self.index]
        app.run(self.host, self.port)
