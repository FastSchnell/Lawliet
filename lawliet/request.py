# -*- coding: utf-8 -*-
import re
from urllib import unquote

from .handler import json_loads
from .handler.form import (
    form_data,
    File,
)


class MaxLengthError(Exception):
    pass


class Request(object):

    """获取传递数据"""

    def __init__(self, environ):
        self.environ = environ
        self.content_type = self.environ['CONTENT_TYPE']
        self.content_length = 0
        if self.environ['CONTENT_LENGTH']:
            self.content_length = int(self.environ['CONTENT_LENGTH'])
        self._form = dict()
        self._file = dict()
        self._json = dict()
        self._param = dict()

    def header(self, header):
        http_header = re.sub('-', '_', header).upper()
        if http_header == 'CONTENT_TYPE':
            return self.environ.get(http_header, None)

        else:
            http_header = 'HTTP_' + http_header
            return self.environ.get(http_header, None)

    def get(self, param, max_length=None):
        if self._param:
            return self._param.get(param, None)

        query_string = self.environ['QUERY_STRING'].split('&')
        for data in query_string:
            key_value = data.split('=')
            if len(key_value) == 2:
                self._param[unquote(key_value[0])] = unquote(key_value[1])
        if self.content_type == 'application/x-www-form-urlencoded':
            if max_length is not None and max_length < self.content_length:
                raise MaxLengthError()
            wsgi_file = self.environ['wsgi.input'].read(self.content_length)
            query_string = wsgi_file.split('&')
            for data in query_string:
                key_value = data.split('=')
                if len(key_value) == 2:
                    self._param[unquote(key_value[0])] = unquote(key_value[1])
        return self._param.get(param, None)

    def environ(self):
        return self.environ

    def _format_form_data(self, _form, _file):
        self._form = _form
        if _file:
            for name in _file:
                self._file[name] = File(_file[name])

    def _get_file(self):
        _form, _file = form_data(self.environ)
        self._format_form_data(_form, _file)

    def _get_form(self):
        _form, _file = form_data(self.environ)
        self._format_form_data(_form, _file)

    def file(self, name, max_length=None):
        if max_length is not None and max_length < self.content_length:
            raise MaxLengthError()

        if self._form or self._file:
            return self._file.get(name, None)
        else:
            self._get_file()
            return self._file.get(name, None)

    def form(self, name, max_length=None):
        if max_length is not None and max_length < self.content_length:
            raise MaxLengthError()

        if self._form or self._file:
            return self._form.get(name, None)
        else:
            self._get_form()
            return self._file.get(name, None)

    def json(self, max_length=None):
        if max_length is not None and max_length < self.content_length:
            raise MaxLengthError()

        if self.content_type == 'application/json':
            self._json = json_loads(self.environ['wsgi.input'].read(self.content_length))
        return self._json

    def data(self):
        return self.json()

    def headers(self, header):
        return self.header(header)
