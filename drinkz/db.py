"""
Database functionality for drinkz information.
"""
import recipes

# private singleton variables at module level
_bottle_types_db = set() #Changed to Set
_inventory_db = {}       #Changed to dictionary
_recipe_db = set()          #Added a recipe database as set
_recipe_name_db = set()    #Added a recipe name as a set

#Input: a recipe
#This function adds a recipe to the dictionary
#If the recipe was already there, no ingredients are included
def add_recipe(r):
    #Check if the recipe name already exists
    if r.Name in _recipe_name_db:
        assert False, 'Recipe name already exists'

    else:
        #New recipe
        #Include recipe in the recipe name database
        _recipe_name_db.add(r.Name)

        #Add recipe in the recipe database
        _recipe_db.add(r)

#Input: a recipe name
#If recipe found, it returns the recipe
def get_recipe(name):
    if not name in _recipe_name_db:
        return #No recipe found
    for temp in _recipe_db:
        if name in temp.Name: #Found the recipe name
            return temp       #Return the recipe

#Return all the recipes
def get_all_recipes():
    return _recipe_db  #Return all the recipes

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db, _recipe_name_db
    _bottle_types_db = set()   #Changed to Set
    _inventory_db = {}         #Changed to Dictionary
    _recipe_db = set()      #reset recipe database
    _recipe_name_db = set()
# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    totalVolume = 0.0
    if((mfg,liquor)) in _inventory_db:
        for bottle_amount in _inventory_db[mfg,liquor]:
            amounts.append(bottle_amount) #add amount

    for bottle in amounts:
        amt = bottle.split()
        if amt[1] == "oz":
            totalVolume += float(amt[0]) * 29.5735
        elif amt[1]=="ml":
            totalVolume += float(amt[0])
        elif amt[1] == "gallon":
            totalVolume += float(amt[0]) * 3785.41


    return totalVolume

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in sorted(_inventory_db):
        yield key
