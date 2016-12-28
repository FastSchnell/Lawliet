# -*- coding: utf-8 -*-


def _content_type_split(content_type):
    parts = content_type.split(';')
    if parts[0] == 'multipart/form-data':
        boundary = parts[1].lstrip()
        return boundary.split('=')[1]
    else:
        return False


def _get_input(file_input, end_boundary):
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
        file_list[-1] = file_list[-1].rstrip()
        self.data = file_list[4:]
        self.buf = '\r\n'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return True

    def read(self):
        all_data = ''
        for line in self.data:
            all_data += line
        return all_data

    def readline(self):
        # ['begin', {'type':'file','name':'test','file':'ss.txt'},
        # 'Content-Type: text/x-python-script\r\n', '\r\n']
        if len(self.data) == 0:
            return ''
        else:
            return self.data.pop(0)


def form_data(environ):
    boundary = _content_type_split(environ['CONTENT_TYPE'])
    _form = dict()
    _file = dict()
    if not boundary:
        return _form, _file
    real_boundary = '--' + boundary + '\r\n'
    end_boundary = '--' + boundary + '--\r\n'
    cache = []
    for line in _get_input(environ['wsgi.input'], end_boundary):
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
