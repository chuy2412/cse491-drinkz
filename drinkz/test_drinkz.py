"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert db.check_inventory('Johnnie Walker', 'Black Label')

def test_add_to_inventory_3():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')

def test_bulk_load_inventory_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    data = """ """
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)
    assert n == 0, n
    
def test_bulk_load_inventory_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    data = """#happy comment, sad comment 


"""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)
    assert n == 0, n


def test_bulk_load_inventory_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    data = """#happy comment, sad comment 
Johnnie Walker,Black Label,1000 ml

"""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)
    assert n == 1, n

def test_bulk_load_inventory_4():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    data = """#happy comment, sad comment
Johnnie Walker,Black Label,1000 ml
Johnnie Walker,Black Label,1400 ml
"""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)
    assert n == 2, n

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '100 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 3957.35, amount

def test_get_liquor_amount_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount    
    assert n == 1, n

def test_get_liquor_amount_4():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '25 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 739.3375, amount


def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_bottle_types_2():
    db._reset_db()
    data = """#happy comment, sad comment 


"""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)
    assert n == 0, n

def test_bulk_load_bottle_types_3():
    db._reset_db()
    data = ''
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)
    assert n == 0, n


def test_bulk_load_bottle_types_4():
    db._reset_db()
    data = """#happy comment, sad comment 
Johnnie Walker,Black Label,blended scotch

"""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_bottle_types_5():
    db._reset_db()
    data = """#happy comment, sad comment 
Johnnie Walker,Black Label,blended scotch
Jose Cuervo,Silver,tequila

"""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 2, n

#HW5 1 Test functionality of bulk_load_recipes
#Test a single recipe with a single ingredient
def test_bulk_load_recipes_1():
    #Reset database
    db._reset_db()

    data = "scotch on the rocks,blended scotch,4 oz"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_recipes(fp)

    #Check if recipe name has been added to recipe list
    assert db.check_recipeName('scotch on the rocks')
    #Check for correct number of recipes
    assert n == 1, n

#Test a single recipe with 2 ingredients
def test_bulk_load_recipes_2():
    #Reset database
    db._reset_db()

    data = "vomit inducing martini,orange juice,6 oz,vermouth,1.5 oz"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_recipes(fp)
    #Check if recipe name has been added to recipe list
    assert db.check_recipeName('vomit inducing martini')
    #Check for correct number of recipes
    assert n == 1, n

#Test for including 3 recipes, added comments and an extra line
def test_bulk_load_recipes_3():
    #Reset database
    db._reset_db()

    data = """#happy comment, sad comment 
scotch on the rocks,blended scotch,4 oz
vodka martini,unflavored vodka,6 oz,vermouth,1.5 oz
whiskey bath,blended scotch,2 liter

"""

    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_recipes(fp)
    #Check if recipe name has been added to recipe list
    assert db.check_recipeName('scotch on the rocks')
    assert db.check_recipeName('vodka martini')
    assert db.check_recipeName('whiskey bath')
    
    #Check for correct number of recipes
    assert n == 3, n

#Test for recipe bad format: ingredient amount 
def test_bulk_load_recipes_bad_format_amount():
    #Reset database
    db._reset_db()

    data = """#happy comment, sad comment 
scotch on the rocks,rocks blended,4
vodka martini,unflavored vodka,6 oz,vermouth,1.5 oz
whiskey bath,blended scotch,2 liter

"""

    fp = StringIO(data)                 # make this look like a file handle
    try:
    	n = load_bulk_data.load_recipes(fp)
    	assert 0, "Improper ingredient amount, test should fail"

    except db.ImproperRecipeIngredientAmount:
    	pass
Ã


def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])
    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_bottle_types_2():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-2.txt'])
    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_bottle_types_3():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-3.txt'])
    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_bottle_types_4():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-4.txt'])
    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_script_load_bottle_types_5():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-5.txt'])
    assert exit_code == 0, 'non zero exit code %s' % exit_code
        
def test_get_liquor_inventory():
    db._reset_db()
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x



    



