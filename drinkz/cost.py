##########################################################################
#Class: Cost
#Additional feature containing the cost of drinks
#Database of drinks downloaded from: Virginia Department of Alcoholic
#				     Beverage Control
##########################################################################
import csv
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def data_reader(fp):
    reader = csv.reader(fp)

    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue

        yield line
        
class Cost(object):
   ###############################################################
   #Constructor:
   #cost is a dictionary database.Where the key is the drink type
   # and the content is a list of tuples.
   #Each tuple contains: (code,brand,size,age,proof,price)
   ################################################################
   def __init__(self):
     #Dictionary database
     self.cost_db = {}

     filename = os.path.dirname(__file__) +"/drinks_cost.csv"
     n = self.load_from_file(filename)         
     #print "loaded " + str(n) + " items \n"

   ###############################################################
   #load_from_file
   #Given the name of the file containing the cost database
   #the function loads all the values in cost_db
   ##############################################################
   def load_from_file(self,filename):
	fp = open(filename)
	reader = data_reader(fp)
	n = 0
    	for line in reader:
        	try:
		    #print line
		    (type,code,brand,size,age,proof,price)= line
		    #If type is not in dictionary
		    if not (type in self.cost_db):
		    	#Create an empty set
			self.cost_db[type] = set()

	   	    #add value to cost database
	    	    self.cost_db[type].add((code,brand,size,age,proof,price))
		    n+=1

		except ValueError:
		   continue

	return n


   ####################################################################
   #search_type(typ)
   #Given the drink type, returns cost data with that type in database
   ####################################################################
   def search_type(self,type):
	search_result = set()
	
	typ = type.upper()
	for key in sorted(self.cost_db):
        	if typ in key:
        	        for item in self.cost_db[key]:
                	        type = key
				code = item[0]
				brand= item[1]
				size = item[2]
				age  = item[3]
				proof= item[4]
				price= item[5]
				search_result.add((type,code,brand,size,age,proof,price))
	return search_result

   ###############################################################################
   #get_all_drinks_cost()
   #Returns the entire cost database in tuples 
   #(type,code,brand,size,age,proof,price)
   ###############################################################################
   def get_all_drinks_cost(self):
        all_results = set()
        for key in (self.cost_db):
        	for item in (self.cost_db[key]):
                	type = key
                        code = item[0]
                        brand= item[1]
                        size = item[2]
                        age  = item[3]
                        proof= item[4]
                        price= item[5]
                        all_results.add((type,code,brand,size,age,proof,price))
	
	all_results = sorted(all_results,key=lambda tup: tup[0]) 
        return all_results


