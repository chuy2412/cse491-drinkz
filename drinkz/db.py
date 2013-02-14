"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set() #Changed to Set
_inventory_db = {}       #Changed to dictionary

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()   #Changed to Set
    _inventory_db = {}         #Changed to Dictionary

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
    #for (m, l, _) in _inventory_db:
    #    yield m, l

    for key in sorted(_inventory_db):
        yield key
