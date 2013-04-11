#! /usr/bin/env python
import sys
import simplejson
import urllib2
import db, recipes, app, dynamic_web
from StringIO import StringIO

#Reference: https://github.com/ctb/cse491-webz/blob/master/json-rpc-client.py
#############################################################################
#Input: jsonrpc method and parameters
#Output: the status, header and result of calling the jsonrpc function based
#	 on given method and parameters
#############################################################################
def call_remote(method, params):
    env = {}
    env['PATH_INFO'] = '/rpc'
    env['REQUEST_METHOD'] = 'POST'
    env['wsgi.input'] = StringIO(simplejson.dumps({
        'method': method,
        'params': params,
        'id': 1
    }))
    env['CONTENT_LENGTH'] = len(env['wsgi.input'].getvalue())

    response = {}
    def my_start_response(s, h, return_in=response):
        response['status'] = s
        response['headers'] = h

    #Create a new SimpleApp object
    app_obj = app.SimpleApp()

    #Get the content
    content = app_obj(env, my_start_response)

    #Get the status
    status = response['status']

    #Get the header
    header = response['headers']

    #Get result
    result =  simplejson.loads(''.join(content))

    #Return: status, header, and result 
    #of calling the jsonrpc function based on given method and parameter
    return (status, header, result)

#############################################################################
#Test function "rpc_convert_units_to_ml"
#Passes 1 galon
#Check if the amount returned is equal to 3785.41
#############################################################################
def test_convert_units_to_ml():
    s, h, result = call_remote('convert_units_to_ml', ['1 gallon'])

    #Check for valid status
    assert s == '200 OK'

    #Check for correct content
    assert ('Content-Type', 'application/json') in h, h

    #Check for correct conversion
    assert result['result'] == 3785.41, result['result']

#############################################################################
#Test function "rpc_get_recipe_names"
#Populatates the database
#Check for all recipe names from the sample database
#############################################################################
def test_get_recipe_names():
    #load from file
    dynamic_web.load_database('bin/sample_database')

    s, h, result = call_remote('get_recipe_names', [])

    #Check for valid status
    assert s == '200 OK'

    #Check for correct content
    assert ('Content-Type', 'application/json') in h, h

    #Check for whiskey bath
    assert 'whiskey bath' in result['result'], result['result']

    #Check for vomit inducing martini
    assert 'vomit inducing martini' in result['result'], result['result']

    #Check for scotch on the rocks
    assert 'scotch on the rocks' in result['result'], result['result']

    #Check for vodka martini
    assert 'vodka martini' in result['result'], result['result']

#############################################################################
#Test function "rpc_get_liquor_inventory"
#Populatates the database
#Check for correct content on the inventory
#############################################################################
def test_get_liquor_inventory():
    s, h, result = call_remote('get_liquor_inventory', [])

    #Check for valid status
    assert s == '200 OK'

    #Check for correct content
    assert ('Content-Type', 'application/json') in h, h

    #Check for Gray Goose
    assert 'Gray Goose' in result['result'], result['result']

    #Check for Johnnie Walker        
    assert 'Johnnie Walker' in result['result'], result['result']

    #Check for Rossi 
    assert 'Rossi' in result['result'], result['result']

    #Uncle Herman's
    assert 'Uncle Herman\'s' in result['result'], result['result']
