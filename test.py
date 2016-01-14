# -*- coding: utf-8 -*-
from lawliet import Routes, app


Routes(
    ('/ping', 'ping.views.ping'),
    ('/字典', 'ping.views.res_json'),
    ('/json', 'ping.views.res_json'),
    ('/xml/', 'ping.views.test_response'),
    ('/ok', 'test.ok')
)

if __name__ == '__main__':
    app.run()


def ok():
    return 'okokok'