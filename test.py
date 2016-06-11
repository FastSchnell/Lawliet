# -*- coding: utf-8 -*-
import os
from lawliet import Routes, app, Route, Cache
from lawliet.tools import SetPath

Route.debug = True
SetPath.run(__file__)


def ok():
    a = Cache.get('ok')
    if a:
        return a
    else:
        return 'error'

Routes(
    ['/ping', 'ping.views.ping'],
    ['/字典', 'ping.views.res_json'],
    ['/json', 'ping.views.res_json'],
    ['/xml/', 'ping.views.test_response'],
    ['/ok', 'test.ok', ['GET', 'PUT']],
    ['/ok.css', 'ping/css/ok.css'],
    ['/auto_method', 'ping.auto_method.auto_method', ['AUTO']]
)

if __name__ == '__main__':
    app.run()
