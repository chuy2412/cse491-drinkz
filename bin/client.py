import socket, sys
import os
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

######################################################################
#This script takes 2 command line arguments (host and port)
#  Test a straight up GET
#  Test a form submission GET (unit_conversion)
#  Image retrieval
#
#Reference:
#    http://effbot.org/zone/socket-intro.htm
#    "Example: read a document via HTTP (File:httpget1.py)"
#How to run:
#   python client.py arctic.cse.msu.edu  portNumber
#####################################################################
def test_main(args):
    #Check for right number of inputs
    if len(args) < 3:
	#Show error message
        print "Incorrect number of inputs"
	print "Try: client.py url port"
	#Terminate the program
        return -1

    host = args[1]
    port = int(args[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("GET / HTTP/1.0\r\n\r\n")

    result = "" 
    while 1:
        buf = s.recv(1000)
        if not buf:
            break
        result +=buf

    s.close()

    found = False
    if "Drinkz" in result:
	found = True


    assert found
    print "Test main page: passed"

##########################################
#Test unit_conversion form
#pass 4 oz
#check for 118.294 ml
#########################################
def test_form_unit_conversion(args):
    #Check for right number of inputs
    if len(args) < 3:
        #Show error message
        print "Incorrect number of inputs"
        print "Try: client.py url port"
        #Terminate the program
        return -1

    host = args[1]
    port = int(args[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("GET /recv_convert?amount=4&type=oz HTTP/1.0\r\n\r\n")

    result = ""
    while 1:
        buf = s.recv(1000)
        if not buf:
            break
        result +=buf

    s.close()

    found = False
    if "118.294 ml" in result:
        found = True

    assert found
    print "Test form page unit conversion: passed"



##########################################
#Test image_retrieval
#########################################
def test_image_retrieval(args):
    #Check for right number of inputs
    if len(args) < 3:
        #Show error message
        print "Incorrect number of inputs"
        print "Try: client.py url port"
        #Terminate the program
        return -1

    host = args[1]
    port = int(args[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("GET /view_image.html HTTP/1.0\r\n\r\n")
    
    fp = s.makefile("request_image")
    #search for the length of the image
    for line in fp:
	if "Content-Length: " in line:
		length = int(line.strip("Content-Length: "))
		break

     
    #manually get the image length
    pth = os.path.dirname(__file__)
    filename = pth +"/../drinkz/googly_eyes_drink_markers_2.jpg"
    manual = open(filename,"r")
    value = ""
    for line in manual:
	value+=line

    s.close()

    #Check if image has the same length
    assert length == len(value)
    print "Test image retrieval: passed"

if __name__ == '__main__':
    #Test a straight up GET
    test_main(sys.argv)
    #test form unit_conversion
    test_form_unit_conversion(sys.argv)
    #test image retrieval
    test_image_retrieval(sys.argv)



