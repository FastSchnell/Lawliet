status_dict = {400: '400 BAD REQUEST', 403: '403 FORBIDDEN',
               404: '404 NOT FOUND', 405: '405 METHOD NOT ALLOWED',
               500: '500 INTERNAL SERVER ERROR'}


class LawDict(dict):
    pass


class Res(object):

    def __init__(self, res=None, status=None, headers=None):
        self.res = res
        self.status = status
        self.headers = headers

    def response(self):
        dict_res = LawDict()
        if self.res is not None:
            dict_res['res'] = self.res
        if self.status is not None:
            if isinstance(self.status, int):
                if self.status in status_dict:
                    self.status = status_dict[self.status]
                else:
                    self.status = '{} '.format(self.status)
            dict_res['status'] = self.status
        if self.headers is not None:
            new_headers = list()
            for i in self.headers:
                new_headers.append((i, self.headers[i]))
            dict_res['headers'] = new_headers
        return dict_res
