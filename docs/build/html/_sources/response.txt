Response
========

Response Json
_____________
::

      def hello_world():
          return {'msg': 'Hello, World!'}

Response XML
____________
::

      from lawliet import Response
      xml_str = '<xml>..</xml>'
      def hello_world():
          return Response(xml_str, headers={'Content-type': 'application/xml'})

Response HTML
_____________
::

      from lawliet import Response
      def hello_world():
          return Response('Hello, World!', headers={'Content-type': 'application/html'})
