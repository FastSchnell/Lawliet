# -*- coding: utf-8 -*-
import re
from urllib import unquote

from .handler import json_loads
from .handler.form import (
    form_data,
    File,
    UseTemp,
    Temp,
)


class MaxLengthError(Exception):
    pass


def _open(temp_file):
    if isinstance(temp_file, tuple):
        return Temp(temp_file)
    else:
        return None


class Request(object):

    """获取传递数据"""

    def __init__(self, environ):
        self.environ = environ
        self.content_type = self.environ.get('CONTENT_TYPE', None)
        self.content_length = int(self.environ.get('CONTENT_LENGTH', 0))
        self._form = dict()
        self._file = dict()
        self._json = dict()
        self._param = dict()
        self.is_temp = False

    def header(self, header):
        http_header = re.sub('-', '_', header).upper()
        if http_header == 'CONTENT_TYPE':
            return self.environ.get(http_header, None)

        else:
            http_header = 'HTTP_' + http_header
            return self.environ.get(http_header, None)

    def get(self, name, max_length=None):
        if not self._param:
            query_string = self.environ['QUERY_STRING'].split('&')
            for data in query_string:
                key_value = data.split('=')
                if len(key_value) == 2:
                    self._param[unquote(key_value[0])] = unquote(key_value[1])

            if self.content_type == 'application/x-www-form-urlencoded':
                if max_length is not None and max_length < self.content_length:
                    raise MaxLengthError()
                output = self.environ.pop('wsgi.input')
                wsgi_file = output.read(self.content_length)
                query_string = wsgi_file.split('&')
                for data in query_string:
                    key_value = data.split('=')
                    if len(key_value) == 2:
                        self._param[unquote(key_value[0])] = unquote(key_value[1])
        return self._param.get(name, None)

    def _init_form(self):
        _form, _file = form_data(self.environ)
        self._form = _form
        if _file:
            for name, file_list in _file.items():
                self._file[name] = File(file_list)

    def file(self, name, max_length=None, use_temp=False):
        if max_length is not None and max_length < self.content_length:
            raise MaxLengthError()

        if self._form or self._file:
            if self.is_temp:
                return _open(self._file.get(name, None))
            else:
                return self._file.get(name, None)
        else:
            if use_temp:
                self.is_temp = True
                self._form, self._file = UseTemp(self.environ).run()
                return _open(self._file.get(name, None))
            else:
                self._init_form()
                return self._file.get(name, None)

    def form(self, name, max_length=None, use_temp=False):
        if max_length is not None and max_length < self.content_length:
            raise MaxLengthError()

        if self._form or self._file:
            return self._form.get(name, None)
        else:
            if use_temp:
                self.is_temp = True
                self._form, self._file = UseTemp(self.environ).run()
            else:
                self._init_form()
            return self._form.get(name, None)

    def json(self, name=None, max_length=None):
        if max_length is not None and max_length < self.content_length:
            raise MaxLengthError()

        if self.content_type == 'application/json':
            if not self._json:
                output = self.environ.pop('wsgi.input')
                self._json = json_loads(output.read(self.content_length))
        if name is None:
            return self._json
        else:
            return self._json.get(name, None)

    def headers(self, header):
        return self.header(header)
