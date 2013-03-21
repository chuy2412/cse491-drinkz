#Convert to ml
#Input: the amount
#Output: the corresponding amount in ml (as float)
def convert_to_ml(amount):
    amt = amount.split()
    volume = 0.0
    if amt[1] == "oz":
    	volume += float(amt[0]) * 29.5735
    elif amt[1]=="ml":
        volume += float(amt[0])
    elif amt[1] == "gallon":  #Added galon
        volume += float(amt[0]) * 3785.41
    elif amt[1] == "liter":   #Added liter
	volume += float(amt[0]) * 1000.0

    return volume
