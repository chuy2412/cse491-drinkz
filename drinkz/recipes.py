###################################################################
#Class Recipe
##################################################################
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
