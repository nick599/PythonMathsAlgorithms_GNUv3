# 02/01/2018
# Version 2
# Licenced under GNU GPL v3

import sys
import math
import os
import itertools
import csv
import time

def main():
	#print "What is a?"
	a_initial=raw_input("What is a?\n")
	m_initial=raw_input("What is m?\n")

	#convert a & m to integers
	a = long(a_initial)
	m = long(m_initial)

	modinv(a, m)

def egcd(a, b):
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:
		#print "STOPPING since a is 0. Result: ("+str(b)+", 0, "+str(a)+")"
		return (b, 0, 1)
	
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b//a) * y, y)

def modinv(a, m):
	print("Running modinv("+str(a)+","+str(m)+")")	
	#print "a is: "+str(a)
	#print "m is: "+str(m)	
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('No Modular Inverse') 
	print str(a)+"**(-1) mod "+str(m)+" is: "+str(x % m)	
	return x % m

if __name__=='__main__':
	main()



