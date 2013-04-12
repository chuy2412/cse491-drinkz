"""
Database functionality for drinkz information.
Information:
    There is a new recipe database named: _recipe_db
    The recipe database is implemented as a set of recipe objects
    I decided to use a set because I am more familiar with sets,
     but I might change it later as a dictionary to look for 
     recipes in a more efficient way by using the recipe name
     as the key and the recipe ingredients as the value

Additional methods (besides the ones needed for homework):
    Thefunction 'check_recipeName(recipe_Name)' has been included
    This method receives a recipe name and returns true if 
    the recipe exist, otherwise, return false

    The function 'convert_to_ml(amount)' has been included
    This method receives an amount and converts the amount as ml
    Currently, the valid amounts are: 'oz', 'ml', 'gallon' and 'liter'

    The function 'get_liquor_amount_noMix(type)' has been included
    This method receives a liquor type and returns the biggest amount
    in ml of that liquor type without mixing liquors (unique manufacturer)

    The function 'get_liquor_amount_withMix(liquor)' has been included
    This method receives a liquor type and return the biggest amount
    in ml, this method allows mixing liquors (just in case is needed later)

"""
import recipes
import unit_conversion     #HW4_1 to convert the amount to ml
import cost
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set() #Changed to Set
_inventory_db = {}       #Changed to dictionary
_recipe_db = set()       #Added a recipe database as set
_cost_db = cost.Cost()   #New dictionary list of drink costs

#Given a recipe name, check if the recipe is on the 
#recipe database. Returns true if it exists, false otherwise
def check_recipeName(recipe_Name):

    for r in sorted(_recipe_db):
	if r.Name.lower() ==recipe_Name.lower():
		return True

    return False

#Given an inventory and a list of recipes,
#Return the recipes we can make.
def check_if_can_make_recipes(recipe_list):
    can_make = []

    #For every recipe in the list
    for r in sorted(recipe_list):
	    #if enough ingredients
	    if len(r.need_ingredients()) == 0:
		#Add recipe to the list
	        can_make.append(r)

    #return the list of recipes that can be done
    return can_make


#Input: a recipe
#This function adds a recipe to the dictionary
#If the recipe was already there, no ingredients are included
def add_recipe(r):
    #Check if the recipe name already exists
    for rec in _recipe_db:
	if rec.Name.lower() ==r.Name.lower():  #Recipe already exists
		err = 'Duplicate Recipe'
		raise DuplicateRecipeName(err)
		return False

    #Check for proper format on each ingredient amount
    for ingredient in r.Ingredient:
	amt = ingredient[1]

	#Check for proper amount 
	if not (amt.endswith('ml') or amt.endswith('oz') or amt.endswith('gallon') or amt.endswith('liter')):
		err = 'Improper recipe ingredient amount'
		raise ImproperRecipeIngredientAmount(err)

    #New recipe
    #Add recipe in the recipe database
    _recipe_db.add(r)
    return True

#Input: a recipe name
#If recipe found, it returns the recipe
def get_recipe(name):
    for temp in _recipe_db:
        if name.lower() in temp.Name.lower(): #Found the recipe name
            return temp       #Return the recipe

    #Recipe not found
    return

#Get recipe names
#Return the name of all recipes in the database
def get_recipe_names():
    names = set()
    for r in _recipe_db:
	names.add(r.Name)
    return names

#Return all the recipes
def get_all_recipes():
    return _recipe_db  #Return all the recipes


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set()   #Changed to Set
    _inventory_db = {}         #Changed to Dictionary
    _recipe_db = set()      #reset recipe database


def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipe_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipe_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipe_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass


class DuplicateRecipeName(Exception):
    pass

class ImproperRecipeIngredientAmount(Exception):
    pass


def add_bottle_type(mfg, liquor, typ):
    if _check_bottle_type_exists(mfg,liquor):
    	#Duplicate
	return False

    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))
    return True

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg.lower() == m.lower() and liquor.lower() == l.lower():
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
	return False

    found = False
    for item in _inventory_db:
	#print "Result is: " + item[0] + " : " + item[1] + "\n"
	if(mfg.lower() ==item[0].lower() and liquor.lower()==item[1].lower()):
		found = True
		mfg = item[0]
		liquor = item[1]

    if not found: 	
	_inventory_db[((mfg,liquor))] = set()    
   	 #Add to inventory
    	_inventory_db[((mfg,liquor))].add(amount)

    else:
	#Add new amount to existing inventory
	_inventory_db[((mfg,liquor))].add(amount)

    return True

def check_inventory(mfg, liquor):
    if ((mfg,liquor)) in _inventory_db: #now checks in a dictionary
        return True   
        
    return False

#Input a type of liquor
#Return the liquor amount in ml with biggest amount in a unique manufacturer
# (No mixing allowed)
def get_liquor_amount_noMix(type):
	max_amount = 0.0
	for (m, l, t) in _bottle_types_db:
        	if type.lower() == t.lower():
			temp_amount = get_liquor_amount(m,l)
			if temp_amount > max_amount:
				max_amount= temp_amount	#Update max amount

	return max_amount

#Input a liquor
#Return the total amount in ml for that liquor in the inventory (Allows mixing drinkz)
def get_liquor_amount_withMix(liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    totalVolume = 0.0
    for key in _inventory_db:
	if key[1].lower()==liquor.lower():
        	amounts.append(_inventory_db[key]) #add amount

    for s in amounts:
	for bottle in s:
        	totalVolume += unit_conversion.convert_to_ml(bottle)  #Now calls the function convert_to_ml
                                                      #to make sure the function works

    return totalVolume;

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    totalVolume = 0.0
    #Previous
    if((mfg,liquor)) in _inventory_db:
        for bottle_amount in _inventory_db[mfg,liquor]:
           amounts.append(bottle_amount) #add amount

    #Current
    #for item in _inventory_db:
	#if is on inventory
#	print item[0] + "kuriboh" + item[1]
#	if((mfg.lower() ==item[0].lower()) and (liquor.lower()==item[1].lower())):
 #       	for bottle_amount in (_inventory_db[item[0],item[1]]):
#		    print bottle_amount
 #         	    amounts.append(bottle_amount) #add amount

    for bottle in amounts:
        totalVolume += unit_conversion.convert_to_ml(bottle)  #Now calls the function convert_to_ml
					     #to make sure the function works

    
    return totalVolume

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in sorted(_inventory_db):
        yield key

def cost_search_drink_type(typ):
    return _cost_db.search_type(typ)

def get_all_drinks_cost():
    return _cost_db.get_all_drinks_cost()

