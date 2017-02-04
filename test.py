# -*- coding: utf-8 -*-

from lawliet import app, Url


def index():
    return {'msg': 'hello world'}

Url(['/', index, 'get'])

if __name__ == '__main__':
    app.run()
