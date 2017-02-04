<h1>引言</h1>
<h3>一个quickstart不能够暴露所有功能的框架他就不算是微框架</h3>

<h3>特别是某些同步框架写的文档比python文档还复杂，有意义吗。我觉得没有意义，所以我不会去看，那么我就自己写。</h3>

<h3>下面是Lawliet的Quickstart</h3>

<h2>安装</h2>

`pip install lawliet`


<h2>Hello World</h2>

      >>>from lawliet.tools import hello
      >>>hello('Hello World!')
      running ==> http://127.0.0.1:5000/


<h2>url映射</h2>

   Url(['url路径', func, [method方法]]),  多个url映射如下

      from lawliet import Url, app
      from lawliet.test import hello
      
      def index():
          return 'Hello, World!'

      Url(
          ['/', index, ['GET']], 
          ['/hello', hello, ['GET', 'POST']]
      )
      if __name__ == '__main__':
          app.run()

<h2>应答方式</h2>

<h3>返回json</h3>

`return {'msg': 'success'}`

<h3>返回str</h3>

`return 'hello world'`

<h3>其他数据结构</h3>

	from lawliet import Response
	Response(xml, headers={'Content-type': 'application/xml'})
	
<h3>返回http code</h3>

	from lawliet import abort
	abort(401)

<h3>url跳转</h3>

	from lawliet import redirect
	redirect('https://www.python.com/')

<h4>注: Response, abort, redirect方法放在try模块，需要把异常Response raise出来<h4>

<h2>请求参数获取</h2>

<h3>json参数</h3>

	def index(request):
	    get_json = request.json()
	    
<h3>form_data参数</h3>
	
	def index(request):
	   get_file = request.file('test_file', use_temp=True)
	   get_code = request.form('code')

<h4>注: use_temp是非必传参数，True缓存到磁盘，False缓存到内存，默认是缓存到内存<h4>

<h4>注: form跟file操作的同一个二进制流，所以设use_temp为True必须放到第一个使用form方法或者file方法里<h4>
   
   
<h3>url参数</h3>

	def index(request):
	    get_name = request.get('name')

<h3>header参数</h3>
    
	def index(request):
	    get_origin = request.header('origin')

<h3>通用获取方式 or 其他content_type类型的获取方式</h3>

	def index(request):
	    content_length = request.environ.get('CONTENT_LENGTH')
	    content_type = request.environ.get('CONTENT_TYPE')
	    if content_type == 'application/xml':
		    output = request.environ.pop('wsgi.input')
		    data = output.read(self.content_length)
		    
	 
<h2>附录</h2>

<h3>gunicorn启动lawliet</h3>
	 
	#hello.py  
	
	from lawliet import Url, Route
	
	def index():
	  return 'Hello, World!'
	  
	Url(['/', index, ['GET']])

` gunicron -w4 -b127.0.0.1:5000 hello:Route` or `gunicorn -c gun.conf hello:Route`

<h3>lawliet支持python2.7版本</h3>
	
	    
	    
<h1>这就是所有功能，可以吐槽了。<h1>
    

    
    

