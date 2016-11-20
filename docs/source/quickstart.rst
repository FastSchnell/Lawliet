Quickstart
==========

A Lawliet Application
_____________________

  .. sourcecode::

      from lawliet import Routes, app

      def index():
          return 'Hello, World!'

      Routes(['/', 'index'])
      if __name__ == '__main__':
          app.run()