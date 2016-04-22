from lawliet import Response


class auto_method(object):

    def get(self):
        return 'qqq'

    def post(self, request):
        return request.get('okok')

    def put(self):
        headers = {'Access-Control-Allow-Origin': 'IJI',
                   'Access-Control-Allow-Methods': 'GET',
                   #'Connection': 'close',
                   'Content-type': 'application/json'
                   }
        return Response('{"ss":11}', headers=headers)
