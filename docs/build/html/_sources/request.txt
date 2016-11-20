Request
=======

Get URL Params
______________
::

      def get_url_params(r):
          url_values = r.get('key')

Get Json
________
::

      def get_json_params(r):
          json_values = r.get_data('json')

Get Http Header Params
______________________
::

      def get_header_params(r):
          origin = r.headers('Origin')

Get All Params
______________
::

      def get_all(r):
          origin = r.environ
