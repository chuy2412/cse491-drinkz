"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package
from . import recipes

def data_reader(fp):
    reader = csv.reader(fp)

    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue

        yield line
        

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)
    x = []
    n = 0
    for line in new_reader:
        try:
            (mfg, name, typ) = line
        except ValueError:
	    print 'Badly formatted line: %s' % line
	    continue

        n += 1
        db.add_bottle_type(mfg, name, typ)

    print n
    return n



def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0

    while (1):
        try:
            for mfg, liquor, amount in new_reader:
                if amount.endswith('ml') or amount.endswith('oz') or amount.endswith('gallon') or amount.endswith('liter'):
                    n += 1
                    db.add_to_inventory(mfg, liquor, amount)
            new_reader.next()
        except StopIteration:
            return n
    return n


#5.1b: Implement bulk loading of recipes from the command line.
def load_recipes(fp):
    """
    Loads in data of the form recipe_Name, recipe_Ingredient from a CSV file.
    Note: recipe_Ingredient is a list of ingredients. Every ingredient
          contains (ingredient_name, amount)

    Takes a file pointer.

    Adds data to database.

    Returns number of valid recipes loaded correctly
    """
    new_reader = data_reader(fp)
    x = []
    n = 0
    for line in new_reader:
        try:
	    #get recipe name
            name = line[0]
	
	    #initialize an empty list ingredients
	    ingredients = []

	    #initialize counter
	    count =1

	    #ingredients to read
	    ingredients_to_read = len(line) -1

	    #While there are ingredients to read
	    while count < ingredients_to_read:
		#Get ingredient name
	    	ingredient_name = line[count]

		#Get ingredient amount
		ingredient_amount = line[count+1]

		#Append ingredients
		ingredients.append((ingredient_name,ingredient_amount))

		#update counter
		count = count +2

            #Create a recipe
            r = recipes.Recipe(name, ingredients)

            #Try to add recipe to database
 	    db.add_recipe(r)

        except ValueError:
	    print 'Badly formatted line: %s' % line
	    continue

        #increment the counter for recipes added
        n = n+1 
    
    return n


