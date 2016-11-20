Request
=======

Get URL Params
______________

  .. sourcecode::

      def get_url_params(r):
          url_values = r.get('key')

Get Json
________

  .. sourcecode::

      def get_json_params(r):
          json_values = r.get_data('json')

Get Http Header Params
______________________

  .. sourcecode::

      def get_header_params(r):
          origin = r.headers('Origin')

Get All Params
______________

  .. sourcecode::

      def get_all(r):
          origin = r.environ
