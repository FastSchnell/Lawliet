class auto_method(object):

    def get(self):
        return 'qqq'

    def post(self, request):
        return request.get('okok')

    def put(self):
        return {'method': 'PUT'}
