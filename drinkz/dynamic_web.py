#! /usr/bin/env python
import unit_conversion
import db      #Import database
import recipes #Import recipe class
import os

#Reference: github.com/ctb/cse491-linkz
try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

try:
    os.mkdir('html/subdir')
except OSError:
    # already exists
    pass

########################################################################
#Add items to the inventory
#Copied the drinks from drinkz/test_recipes.py
########################################################################
def add_items():
        #Reset database
        db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
	db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

	db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
	db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
	db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
	db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

	db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
	db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

	#Add recipes
	r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
	db.add_recipe(r)
	r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
	db.add_recipe(r)
	r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
	db.add_recipe(r)
	r = recipes.Recipe('whiskey bath', [('blended scotch', '2 liter')])
	db.add_recipe(r)


###############################################################
#load database
###############################################################
def load_database(filename):
	try:
		#Try to load from database
	   	db.load_db(filename)

	except Exception:
		#If the file was not found add items
		add_items()

###############################################################
#Index
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_index():
	data= """
        <html>
        <head>
        <title>Drinkz Home page</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
	<script>
	function myFunction()
	{
		alert("Hello! I am an alert box!");
	}
	</script>
	</script>
        </head>
        <body>
        <h1>Drinkz</h1>
        <p><a href='recipes.html'>Recipes</a>
        <p>
        <a href='inventory.html'>Inventory</a>
        </p>

        <p>
        <a href='liquor_types.html'>Liquor Types</a>
        </p>

	<p>
        <a href='add_liquor_types.html'>Add Liquor Types</a>
        </p>

        <p>
        <a href='convert_to_ml.html'>Convert to ml</a>
        </p>

	<p>
	<input type="button" onclick="myFunction()" value="Show alert box" />
	</p>

        </body>
        </html>
        """
        return data

###############################################################
#Recipes
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_Recipes():
	data= """
        <html>
        <head>
        <title>View Recipes</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        <h1>Recipes</h1>
	"""
	data = data + """ 
	<table border="1">
	<tr>
	<th>Recipe Name</th>
	<th>Ingredients</th>"
	<th>Enough ingredients?</th>
	"""
	#For every recipe in the database
	for r in sorted(db._recipe_db):
	    possible = 'No'
	    if len(r.need_ingredients()) == 0:
	        possible = 'Yes'
	    #Display result
	    data = data +  "<tr> <td>" + r.Name + " </td> <td>" + str(r.Ingredient) + " </td> <td>" +possible +  " </td> </tr>"

	data = data +  """
	</table>
	</tr>
	</table>

	Link to the other three files:
	<p><a href='index.html'>Back to Index</a>
	</p>
	<p><a href='inventory.html'>Inventory</a>
	</p>
	<p><a href='liquor_types.html'>Liquor Types</a>
	</p>
	</body>
	</html>
	"""
        return data

#############################################################
#Inventory
##############################################################
def generate_Inventory():
	data= """
        <html>
        <head>
        <title>My Inventory</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        <h1>Inventory</h1>
	"""
	data = data +  """ 
	<table border="1">
	<tr>
	<th>Manufacturer</th>
	<th>Liquor Type</th>"
	<th>Amount</th>
	"""
	for mfg, liquor in db.get_liquor_inventory():
    		#Get the amount in ml 
    		amt = db.get_liquor_amount(mfg,liquor)
    		amount = str(amt) + ' ml'
    		data = data +  "<tr> <td>" + mfg + "</td> <td>"+ liquor + "</td> <td>"+ amount+ " </td> </tr>"

	data = data + """
	</table>
	</tr>
	</table>

	Link to the other three files:
	<p><a href='index.html'>Back to Index</a>
	</p>
	<p><a href='recipes.html'>Recipes</a>
	</p>
	<p><a href='liquor_types.html'>Liquor Types</a>
	</p>
	</body>
	</html>
	"""
	return data

#############################################################
#liquor_types
#Reference: github.com/ctb/cse491-linkz
#############################################################
def generate_Liquor_Types():
	data= """
        <html>
        <head>
        <title>View Liquor Types</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        <h1>Liquor Types</h1>
	"""
	data = data + """
	<table border="1">
	<tr>
	<th>Manufacturer</th>
	<th>Liquor</th>"
	<th>Type</th>
	"""
	for (mfg, liquor, type) in db._bottle_types_db:
    		data = data + "<tr> <td>" + mfg+ "</td> <td>" +liquor+" </td> <td>"+type+" </td> </tr>"

	data = data +  """
	</table>
	</tr>
	</table>

	Link to the other three files:
	<p><a href='index.html'>Back to Index</a>
	</p>
	<p><a href='recipes.html'>Recipes</a>
	</p>
	<p><a href='inventory.html'>Inventory</a>
	</p>
	</body>
	</html>
	"""
	return data

#############################################################
#Add liquor_types
#Reference: github.com/ctb/cse491-linkz
#############################################################
def add_Liquor_Types():
        data= """
        <html>
        <head>
        <title>Add Liquor Types</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        <h1>Enter Liquor Types</h1>
        """
        data = data + """
        
        <form action='recv_add_liquor_types'>
        Manufacturer: <input type='text' name='mfg' size'20'>
        Liquor: <input type='text' name='liquor' size'20'>
	Type: <input type='text' name='typ' size'20'>
        <p><input type='submit'></p>
	</form>

	Link to to home:
	<p><a href='index.html'>Back to Index</a>
        </body>
        </html>
        """
        return data




###############################################################
#convert_to ml
###############################################################
def convert_to_ml():
	data= """
        <html>
        <head>
        <title>Conversion</title>
        <style type='text/css'>
        h1 {color:red;}
        body{
        font-size:14px;
        }
        </style>
        </head>
        <body>
        <h1>Convert to ml</h1>
	"""

        data = data +  """
        <form action='recv_convert'>
        Amount? <input type='text' name='amount' size'20'>
        <p><input type="radio" name="type" value="ml" checked> ml</p>
        <p><input type="radio" name="type" value="oz">oz<br></p>
        <p><input type="radio" name="type" value="gallon">gallon</p>
        <p><input type="radio" name="type" value="liter">liter</p>
        <p><input type='submit'></p>
        </form>
	</body>
	</html>
        """
        return data
