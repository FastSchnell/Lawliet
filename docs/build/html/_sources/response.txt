Response
========

Response Json
_____________

  .. sourcecode::

      def hello_world():
          return {'msg': 'Hello, World!'}

Response XML
____________

  .. sourcecode::

      from lawliet import Response
      xml_str = '<xml>..</xml>'
      def hello_world():
          return Response(xml_str, headers={'Content-type': 'application/xml'})

Response HTML
_____________

  .. sourcecode::

      from lawliet import Response
      def hello_world():
          return Response('Hello, World!', headers={'Content-type': 'application/html'})
