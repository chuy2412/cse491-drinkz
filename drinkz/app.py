#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import dynamic_web
import unit_conversion
import db
import recipes

from Cookie import SimpleCookie
import jinja2
import uuid

import os
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

usernames = {}
# this sets up jinja2 to load templates from the 'templates' directory
loader = jinja2.FileSystemLoader('./jinja2/templates')
env = jinja2.Environment(loader=loader)

dispatch = {
    '/' : 'index',
    '/index.html' : 'index',
    '/recipes.html' : 'recipes',
    '/recipes_we_can_make.html' : 'recipes_we_can_make',
    '/inventory.html' : 'inventory',
    '/liquor_types.html' : 'liquor_types',
    '/add_liquor_types.html' : 'add_liquor_types',
    '/add_liquor_inventory.html' : 'add_liquor_inventory',
    '/add_recipe.html' : 'add_recipe',
    '/convert_to_ml.html' : 'convert_to_ml',
    '/generate_drink_cost.html' : 'generate_drink_cost',
    '/error' : 'error',
    '/recv_add_liquor_types' : 'recv_add_liquor_types',
    '/recv_add_liquor_inventory' : 'recv_add_liquor_inventory',
    '/recv_add_recipe' : 'recv_add_recipe',
    '/recv_search_drink_price' : 'recv_search_drink_price', 
    '/recv_convert' : 'recv_convert',
    '/rpc'  : 'dispatch_rpc',
    '/search_drink_price.html' : 'search_drink_price',
    '/view_image.html' : 'view_image',
    '/login_1' : 'login1',
    '/login1_process' : 'login1_process',
    '/logout' : 'logout',
    '/status' : 'status'

}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

	#load from file
        dynamic_web.load_database('/../bin/drinkz_database')

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
        
    #Add login process
    def login1(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        title = 'login'
        template = env.get_template('login1.html')
        return str(template.render(locals()))

    def login1_process(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        content_type = 'text/html'

        # authentication would go here -- is this a valid username/password,
        # for example?

        k = str(uuid.uuid4())
        usernames[k] = name

        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(('Set-Cookie', 'name1=%s' % k))

        start_response('302 Found', headers)
        return ["Redirect to /status..."]

    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key

                if key in usernames:
                    del usernames[key]
                    print 'DELETING'

        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /status..."]

    def status(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
                
        title = 'login status'
        template = env.get_template('status.html')
        return str(template.render(locals()))

    def recipes(self, environ, start_response):
        data = dynamic_web.generate_Recipes()
        start_response('200 OK', list(html_headers))
        return [data]

    def recipes_we_can_make(self, environ, start_response):
        data = dynamic_web.generate_Recipes_we_can_make()
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

    def add_liquor_types(self, environ, start_response):
        data = dynamic_web.add_Liquor_Types()
        start_response('200 OK', list(html_headers))
        return [data]

    def add_liquor_inventory(self, environ, start_response):
        data = dynamic_web.add_Liquor_Inventory()
        start_response('200 OK', list(html_headers))
        return [data]

    def add_recipe(self, environ, start_response):
        data = dynamic_web.add_Recipe()
        start_response('200 OK', list(html_headers))
        return [data]

    def convert_to_ml(self, environ, start_response):
        #data = dynamic_web.convert_to_ml()
        data = open('drinkz/conversion_form.html').read()
        start_response('200 OK', list(html_headers))
        return [data]

    def	generate_drink_cost(self, environ, start_response):
	data = dynamic_web.generate_drink_cost()
        start_response('200 OK', list(html_headers))
        return [data]

    def search_drink_price(self, environ, start_response):
	data = dynamic_web.search_drink_price()
        start_response('200 OK', list(html_headers))
        return [data]
 
    def view_image(self, environ, start_response):
        content_type = 'image/jpg'
        pth = os.path.dirname(__file__)
        filename = pth + '/googly_eyes_drink_markers_2.jpg'
        data = open(filename, 'rb').read()
        #data += """ <p><a href='index.html'>Back to Index</a></p>"""
	start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv_add_liquor_types(self, environ, start_response):
	formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	msg = "No values were modified"
	#Check if values have data
	if ( ('mfg' in results) and ('liquor' in results) and ('typ' in results)):
        	#Get manufacturer
		mfg = results['mfg'][0]
        	#Get liquor name
        	liquor = results['liquor'][0]
		#Get type
		typ = results['typ'][0]
  
		if (db._check_bottle_type_exists(mfg,liquor)):
			message = "Ooops Manufacturer and Liquor information was already there"
		else:
			#Add bottle type
			db.add_bottle_type(mfg,liquor,typ)
			dynamic_web.save_database('/../bin/drinkz_database')
			message = "Liquor type has been added successfully"
			msg = "Liquor type has been added"

	#At least one of the fields is empty
	else:
		message = "Ooops at least one of the fields was empty"

        #Generate results in html format
        content_type = 'text/html'
        data= """
        <html>
        <head>
        <title>Updated Liquor Type</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
	</head>
        <body>
	"""
        data = data + "<h1>" + message + "</h1>"
	data = data + msg 
	tmp = dynamic_web.generate_liquor_type_table()
	data = data + tmp
	data = data + "<p><a href='./add_liquor_types.html'>add another liquor type</a></p>"
        data = data + "<p><a href='./'>return to index</a></p>"
        data = data + """
        </body>
        <html>
        """
        start_response('200 OK', list(html_headers))
        return [data]

    def recv_add_liquor_inventory(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	msg = ""
	status = "No values were modified\n"
	#Check if values have data
        if ( ('mfg' in results) and ('liquor' in results) and ('amt' in results)):
	        #Get manufacturer
        	mfg = results['mfg'][0]
        	#Get liquor name
        	liquor = results['liquor'][0]
        	#Get amount
        	amt = results['amt'][0]
 
		#Check if bottle type information is there
        	if not (db._check_bottle_type_exists(mfg,liquor)):
                	message = "Ooops Please add manufacturer and liquor information to bottle types first"
		
        	else:
			#check if amount unit is correct
			if not (amt.endswith('ml') or amt.endswith('oz') or amt.endswith('gallon') or amt.endswith('liter')):
				message = "Ooops unit amount is not correct. "
				msg = "Valid units: 'ml','oz','gallon','liter'"
			else:
                		#Add to inventory
                		db.add_to_inventory(mfg,liquor, amt)
		                dynamic_web.save_database('/../bin/drinkz_database')
                		message = "Added to inventory successfully"
				status = "Updated inventory\n"

	else:
		message = "Ooops at least one of the fields was empty"

        #Generate results in html format
        content_type = 'text/html'
        data= """
        <html>
        <head>
        <title>Updated inventory</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        """
        data = data + "<h1>" + message + "</h1>"
        tmp = dynamic_web.generate_inventory_table()
        data = data + msg + "<p>" + status + "</p>" + tmp
	
        data = data + "<p><a href='./add_liquor_inventory.html'>add another liquor to inventory</a></p>"
        data = data + "<p><a href='./'>return to index</a></p>"
        data = data + """
        </body>
        <html>
        """
        start_response('200 OK', list(html_headers))
        return [data]

    def recv_add_recipe(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        msg = "No values were modified"
        is_duplicate = False
        #Check if values have data
        if ( ('name' in results) and ('ingredients' in results) ):
                #Get recipe name
                name = results['name'][0]
                #Get ingredients
                ingredients = results['ingredients'][0]

                for r in db._recipe_db:
			if name.lower() ==r.Name.lower():  #Recipe already exists
                        	is_duplicate =True
                if (is_duplicate):
			message = "Ooops recipe name is already in in database"
		else:
			print "Ingredients: " + ingredients + " \n"
                        #Add recipe
                        ingredient_list = []
			#Separate ingredient name and ingredient amount
		        split_ingredients = ingredients.split(';')
			#For each ingredient
			for i in split_ingredients:
				#Add tuple to ingredient list
				ingredient_list.append(tuple(i.split(',')))

			#create a recipe object
			r = recipes.Recipe(name,ingredient_list)

			#add recipe
			db.add_recipe(r)
			dynamic_web.save_database('/../bin/drinkz_database')
                        message = "Recipe type has been added successfully"
                        msg = "Updated recipe list"

        #At least one of the fields is empty
        else:
                message = "Ooops at least one of the fields was empty"

        #Generate results in html format
        content_type = 'text/html'
        data= """
        <html>
        <head>
        <title>Updated Recipe</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        """
        data = data + "<h1>" + message + "</h1>"
        data = data + msg
        tmp  = dynamic_web.generate_recipe_table()
        data = data + tmp
        data = data + "<p><a href='./add_recipe.html'>add another recipe</a></p>"
        data = data + "<p><a href='./'>return to index</a></p>"
        data = data + """
        </body>
        <html>
        """
        start_response('200 OK', list(html_headers))
        return [data]

    def recv_search_drink_price(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        search_results = set()
        #Check if values have data
        if ('type' in results):
                #Get type
                type = results['type'][0]
 
                #Search for given type
                search_results = db.cost_search_drink_type(type)
                message = "Search results for: " + type

        #Empty field
        else:
                message = "Ooops no value was entered, please try again"

        #Generate results in html format
        content_type = 'text/html'
        data= """
        <html>
        <head>
        <title>Results of liquor prices</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        """
        data = data + "<h1>" + message + "</h1>"
        tmp = dynamic_web.generate_drink_cost_table(search_results)
        data = data + tmp
        data = data + "<p><a href='./search_drink_price.html'>Search for another drink</a></p>"
        data = data + "<p><a href='./'>return to index</a></p>"
        data = data + """
        </body>
        <html>
        """
        start_response('200 OK', list(html_headers))
        return [data]


    def recv_convert(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	Amount = "0"
	if ('amount' in results):
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
        return list(db.get_recipe_names())

    #HW4_5a JSON-RPC get liquor inventory
    def rpc_get_liquor_inventory(self):
        return dict(db.get_liquor_inventory())    

    #HW5_1d JSON-RPC add recipe
    def rpc_add_recipe(self, name, ingredients):
        r = recipes.Recipe(name,ingredients)
        return db.add_recipe(r)

    #HW5_1d JSON-RPC add liquor to inventory          
    def rpc_add_to_inventory(self, mfg,liquor,amt ):
        return db.add_to_inventory(mfg,liquor,amt)

    #HW5_1d JSON-RPC add liquor type      
    def rpc_add_bottle_type(self, mfg, liquor,typ):
        return db.add_bottle_type(mfg,liquor,typ)

    #HW5_1d JSON-RPC return the recipes that we can make
    def rpc_check_if_can_make_recipes(self, recipe_list):
        return list(db.check_if_can_make_recipes(recipe_list))

    #H5_2 JSON-RPC to search price of a drink type
    def rpc_search_drink_price(self, type):
        return db.cost_search_drink_type(type)

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    #load from file
    dynamic_web.load_database('/../bin/drinkz_database')
    #dynamic_web.save_database('/../bin/drinkz_database')
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()

