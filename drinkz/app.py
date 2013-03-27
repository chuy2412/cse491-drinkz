#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import dynamic_web
import unit_conversion

dispatch = {
    '/' : 'index',
    '/index.html' : 'index',
    '/recipes.html' : 'recipes',
    '/inventory.html' : 'inventory',
    '/liquor_types.html' : 'liquor_types',
    '/convert_to_ml.html' : 'convert_to_ml',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

	#load from file
	dynamic_web.load_database('bin/sample_database')

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = dynamic_web.generate_index()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        data = dynamic_web.generate_Recipes()
        start_response('200 OK', list(html_headers))
        return [data]


    def inventory(self, environ, start_response):
        data = dynamic_web.generate_Inventory()
        start_response('200 OK', list(html_headers))
        return [data]

    def liquor_types(self, environ, start_response):
        data = dynamic_web.generate_Liquor_Types()
        start_response('200 OK', list(html_headers))
        return [data]

    def convert_to_ml(self, environ, start_response):
        data = dynamic_web.convert_to_ml()
        start_response('200 OK', list(html_headers))
        return [data]

    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        #Get the amount
        Amount = results['amount'][0]       
	#Get the type (oz, ml, liter, gallon)
        Type = results['type'][0]
        
  
        #Concatenate amount and type
        amount_given = Amount + " " + Type

        #Compute the conversion
        new_Amount = unit_conversion.convert_to_ml(amount_given)

        #Generate results in html format
        content_type = 'text/html'
        #data =  "<b>Conversion to ml</b><p></p>"
	data= """
        <html>
        <head>
        <title>Conversion Results</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        <h1>Result from conversion</h1>
	"""

        data = data + "<p>" + amount_given + " = "+ str(new_Amount)+" ml</p>"
        data = data + "<p><a href='./'>return to index</a></p>"
	data = data + """
	</body>
	<html>
	"""
        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)

    #HW4_5a JSON-RPC to convert unit to ml
    def rpc_convert_units_to_ml(self, amount):
        return unit_conversion.convert_to_ml(amount)

    #HW4_5a JSON-RPC get recipe names
    def rpc_get_recipe_names(self):
        return list(db.get_all_recipes())

    #HW4_5a JSON-RPC get liquor inventory
    def rpc_get_liquor_inventory(self):
        return dict(db.get_liquor_inventory())    
def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()

