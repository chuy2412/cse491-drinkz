import app
import urllib
import dynamic_web
import db

#reference from:https://github.com/ctb/cse491-webz/blob/master/test_app.py
def test_index():
    environ = {}
    environ['PATH_INFO'] = '/'
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Drinkz') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_recipes():
    environ = {}
    environ['PATH_INFO'] = '/recipes.html'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    #Check for recipe: "scotch on the rocks"
    assert text.find('scotch on the rocks') != -1, text

    #Check for recipe: "vomit inducing martini"
    assert text.find('vomit inducing martini') != -1, text

    #Check for recipe: "whiskey bath"
    assert text.find('whiskey bath') != -1, text

    #Check for recipe: "vodka martini"
    assert text.find('vodka martini') != -1, text

    #Make sure that the test did not produce an error
    assert status == '200 OK'

def test_inventory():
    environ = {}
    environ['PATH_INFO'] = '/inventory.html'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    #Check for manufacturer: "Gray Goose"
    assert text.find('Gray Goose') != -1, text

    #Check for manufacturer: "Johnnie Walker"
    assert text.find('Johnnie Walker') != -1, text

    #Check for manufacturer: "Rossi"
    assert text.find('Rossi') != -1, text

    #Check for manufacturer: "Uncle Herman's"
    assert text.find('Uncle Herman\'s') != -1, text

    #Make sure that the test did not produce an error
    assert status == '200 OK'

def test_liquor_types():
    environ = {}
    environ['PATH_INFO'] = '/liquor_types.html'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    #Check for liquor type: "blended scotch"
    assert text.find('blended scotch') != -1, text

    #Check for liquor type: "unflavored vodka"
    assert text.find('unflavored vodka') != -1, text

    #Check for liquor type: "vermouth"
    assert text.find('vermouth') != -1, text

    #Make sure that the test did not produce an error
    assert status == '200 OK'

#Test conversion to ml
#Convert 1 gallon to ml
def test_conversion():
    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(amount='1',
                                                    type='gallon'))
    environ['PATH_INFO'] = '/recv'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)
    
    text = "".join(results)
    status = d['status']
    headers = d['headers']

    assert text.find("1 gallon = 3785.41 ml") != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
