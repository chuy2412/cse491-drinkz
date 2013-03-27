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
    The function 'need_ingredients' is now in db instead or recipes
    because otherwise, every recipe object would have access to the inventory
    database. Instead, the database has a function need_ingredients and 
    receives a recipe as an input. Tests cases were changed accordingly

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

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set() #Changed to Set
_inventory_db = {}       #Changed to dictionary
_recipe_db = set()       #Added a recipe database as set


#Input: a recipe
#This function adds a recipe to the dictionary
#If the recipe was already there, no ingredients are included
def add_recipe(r):
    #Check if the recipe name already exists
    for rec in _recipe_db:
	if rec.Name ==r.Name:  #Recipe already exists
		err = 'Duplicate Recipe'
		raise DuplicateRecipeName(err)
    #New recipe
    #Add recipe in the recipe database
    _recipe_db.add(r)

#Input: a recipe name
#If recipe found, it returns the recipe
def get_recipe(name):
    for temp in _recipe_db:
        if name in temp.Name: #Found the recipe name
            return temp       #Return the recipe

    #Recipe not found
    return

#Return all the recipes
def get_all_recipes():
    return _recipe_db  #Return all the recipes

def need_ingredients(r):
    ingredients = r.Ingredient #get the recipe ingredients
    missing = []
    for i in ingredients: #for each ingredient
	#get the type and the amount
	type = i[0]
	amount = i[1]
	need_amount = unit_conversion.convert_to_ml(amount)
	current_amount = get_liquor_amount_noMix(type)
        diff = need_amount - current_amount
	if diff >0:
		new_amount = diff #str(diff) + ' ml' #to show ml
		missing.append((type, new_amount))

    #print missing 
    return missing

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


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    # just add it to the inventory database as a tuple, for now.
    #_inventory_db.append((mfg, liquor, amount))
    if not ((mfg,liquor)) in _inventory_db:
        _inventory_db[((mfg,liquor))] = set()
        
    _inventory_db[((mfg,liquor))].add(amount)

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
        	if type == t:
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
	if key[1]==liquor:
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
    if((mfg,liquor)) in _inventory_db:
        for bottle_amount in _inventory_db[mfg,liquor]:
            amounts.append(bottle_amount) #add amount

    for bottle in amounts:
        totalVolume += unit_conversion.convert_to_ml(bottle)  #Now calls the function convert_to_ml
					     #to make sure the function works

    return totalVolume

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in sorted(_inventory_db):
        yield key
