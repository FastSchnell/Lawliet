# -*- coding: utf-8 -*-
import tempfile


def _boundary(content_type):
    parts = content_type.split(';')
    if parts[0] == 'multipart/form-data':
        boundary = parts[1].lstrip()
        return boundary.split('=')[1]
    else:
        return False


def _input(file_input, end_boundary):
    line = file_input.readline()
    while True:
        if line == end_boundary:
            yield line
            raise StopIteration()
        else:
            yield line
            line = file_input.readline()


class File(object):

    def __init__(self, file_list):
        self.file_name = file_list[1]["file_name"]
        file_list[-1] = file_list[-1].rstrip()
        self.data = file_list[4:]

    def __enter__(self):
        self.temp = tempfile.TemporaryFile()
        self.temp.write(self.read())
        self.temp.seek(0)
        return self.temp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp.close()

    def read(self):
        return ''.join(self.data)

    def readline(self):
        if len(self.data) == 0:
            return ''
        else:
            return self.data.pop(0)


class Temp(object):

    def __init__(self, temp_file):
        self.file_name = temp_file[1]
        self.temp = temp_file[0]

    def __enter__(self):
        return self.temp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp.close()


def form_data(environ):
    boundary = _boundary(environ['CONTENT_TYPE'])
    _form = dict()
    _file = dict()
    if not boundary:
        return _form, _file
    real_boundary = '--' + boundary + '\r\n'
    end_boundary = '--' + boundary + '--\r\n'
    cache = []
    output = environ.pop('wsgi.input')
    for line in _input(output, end_boundary):
        if line == real_boundary:
            if not cache:
                cache.append('begin')
            elif cache[1]["type"] == "file":
                _file[cache[1]["name"]] = cache
                cache = ['begin']
            else:
                raise
        elif line == end_boundary:
            if cache:
                _file[cache[1]["name"]] = cache
                cache = []

        elif len(cache) == 1:
            line_list = line.split(';')
            if len(line_list) == 3:
                cache.append({
                    "type": "file",
                    "name": line_list[1].split('=')[1].strip()[1:-1],
                    "file_name": line_list[2].split('=')[1].strip()[1:-1]
                })
            elif len(line_list) == 2:
                cache.append({
                    "type": "form",
                    "name": line_list[1].split('=')[1].strip()[1:-1]
                })
            else:
                raise

        elif len(cache) == 2:
            cache.append(line)

        elif len(cache) == 3:
            cache.append(line)
            if cache[1]["type"] == "form":
                _form[cache[1]["name"]] = line.rstrip()
                cache = []

        elif cache[1]["type"] == "file":
            cache.append(line)

        else:
            raise

    return _form, _file


class UseTemp(object):

    def __init__(self, environ):
        self.environ = environ
        self.boundary = _boundary(environ['CONTENT_TYPE'])
        self._form = dict()
        self._file = dict()
        self.temp = tempfile.TemporaryFile()

    def run(self):
        if not self.boundary:
            return self._form, self._file
        real_boundary = '--' + self.boundary + '\r\n'
        end_boundary = '--' + self.boundary + '--\r\n'
        cache = []
        output = self.environ.pop('wsgi.input')
        for line in _input(output, end_boundary):
            if line == real_boundary:
                if not cache:
                    cache.append('begin')
                elif cache[1]["type"] == "file":
                    self.temp.write(line.rstrip())
                    self.temp.seek(0)
                    self._file[cache[1]["name"]] = (self.temp, cache[1]["file_name"])
                    cache = ['begin']
                else:
                    raise
            elif line == end_boundary:
                if cache:
                    self._file[cache[1]["name"]] = (self.temp, cache[1]["file_name"])
                    self.temp.seek(0)
                    cache = []

            elif len(cache) == 1:
                line_list = line.split(';')
                if len(line_list) == 3:
                    self.temp = tempfile.TemporaryFile()
                    cache.append({
                        "type": "file",
                        "name": line_list[1].split('=')[1].strip()[1:-1],
                        "file_name": line_list[2].split('=')[1].strip()[1:-1]
                    })
                elif len(line_list) == 2:
                    cache.append({
                        "type": "form",
                        "name": line_list[1].split('=')[1].strip()[1:-1]
                    })
                else:
                    raise

            elif len(cache) == 2:
                cache.append(line)

            elif len(cache) == 3:
                cache.append(line)
                if cache[1]["type"] == "form":
                    self._form[cache[1]["name"]] = line.rstrip()
                    cache = []

            elif cache[1]["type"] == "file":
                self.temp.write(line)

            else:
                raise

        return self._form, self._file
