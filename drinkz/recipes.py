###################################################################
#Class Recipe
##################################################################
import db
import unit_conversion

class Recipe(object):
   ###############################################################
   #Constructor:
   #  The constructor for Recipe should take
   #  a name (a string) and a list of ingredient 2-tuples,
   #  (liquor type, amount).
   #For example:
   #  Recipe('vodka martini', [('vodka', '6 oz'), ('vermouth', '1 oz')])
   ################################################################
   def __init__(self,name, ingredient):
      self.Name = name
      self.Ingredient = ingredient         

   ###############################################################
   #need_ingredients
   #Return the list of missing ingredients.
   #If the list is empty, the recipe can be done with current
   #inventory. Otherwise, return a list of missing ingredients
   ##############################################################
   def need_ingredients(self):
      ingredients = self.Ingredient #get the recipe ingredients
      missing = []
      for i in ingredients: #for each ingredient
	#get the type and the amount
	type = i[0]
	amount = i[1]
	need_amount = unit_conversion.convert_to_ml(amount)
	current_amount = db.get_liquor_amount_noMix(type)
        diff = need_amount - current_amount
	if diff >0:
		new_amount = diff #str(diff) + ' ml' #to show ml
		missing.append((type, new_amount))

      #print missing 
      return missing
