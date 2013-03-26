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
	db._reset_db() #Reset database

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
#Index
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_index():
        add_items()
	#data = open('html/index.html', 'w')
	data = ""
	data="Drinkz <p><a href='recipes.html'>Recipes</a>"
	data= data +  """
	<p>
	<a href='inventory.html'>Inventory</a>
	</p>

	<p>
	<a href='liquor_types.html'>Liquor Types</a>
	</p>

	"""
	return data

###############################################################
#Recipes
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_Recipes():
	#fp = open('html/recipes.html', 'w')

	data =  "<b>Recipes</b><p></p>"
	data = data + """ 
	<table border="1">
	<tr>
	<th>Recipe Name</th>
	<th>Ingredients</th>"
	<th>Enough ingredients?</th>
	"""
	#For every recipe in the database
	for r in db._recipe_db:
	    possible = 'No'
	    if len(db.need_ingredients(r)) == 0:
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
	"""
        return data

#############################################################
#Inventory
##############################################################
def generate_Inventory():
	#fp = open('html/inventory.html', 'w')

	data =  "<b>Inventory</b><p></p>"
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
	"""
	return data

#############################################################
#liquor_types
#Reference: github.com/ctb/cse491-linkz
#############################################################
def generate_Liquor_Types():
	#fp = open('html/liquor_types.html', 'w')

	data = "<b>Liquor Types</b><p></p>"
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
	"""
	return data

