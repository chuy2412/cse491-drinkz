#! /usr/bin/env python
from drinkz import db      #Import database
from drinkz import recipes #Import recipe class
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
fp = open('html/index.html', 'w')
print >>fp, "Drinkz <p><a href='recipes.html'>Recipes</a>"
print >>fp, """
<p>
<a href='inventory.html'>Inventory</a>
</p>

<p>
<a href='liquor_types.html'>Liquor Types</a>
</p>

<p>
<a href='Add_bottle_type.html'>Add Bottle Type</a>
</p>

"""
fp.close()

###############################################################
#Recipes
#Reference: github.com/ctb/cse491-linkz
###############################################################
fp = open('html/recipes.html', 'w')

print >>fp, "<b>Recipes</b><p></p>"
print >>fp, """ 
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
    print >> fp, "<tr> <td>%s </td> <td>%s </td> <td>%s </td> </tr>" % (r.Name, r.Ingredient, possible)

print >>fp, """
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
fp.close()

#############################################################
#Inventory
##############################################################
fp = open('html/inventory.html', 'w')

print >>fp, "<b>Inventory</b><p></p>"
print >>fp, """ 
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
    print >> fp, "<tr> <td>%s </td> <td>%s </td> <td>%s </td> </tr>" % (mfg, liquor, amount)

print >>fp, """
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
fp.close()

#############################################################
#liquor_types
#Reference: github.com/ctb/cse491-linkz
#############################################################
fp = open('html/liquor_types.html', 'w')

print >>fp, "<b>Liquor Types</b><p></p>"
print >>fp, """
<table border="1">
<tr>
<th>Manufacturer</th>
<th>Liquor</th>"
<th>Type</th>
"""
for (mfg, liquor, type) in db._bottle_types_db:
    print >> fp, "<tr> <td>%s </td> <td>%s </td> <td>%s </td> </tr>" % (mfg, liquor, type)

print >>fp, """
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
fp.close()


#############################################################
#Add_bottle_type
#############################################################
fp = open('html/Add_bottle_type.html', 'w')

print >>fp, "<b>Add Bottle  Type</b><p></p>"
print >>fp, """
"""
fp.close()



