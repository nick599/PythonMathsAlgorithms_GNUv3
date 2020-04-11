#Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.
#Version 1. 23/08/2019.
#Programmed & tested in Python 3.52 only
#This program works out the Legendre Symbol of two numbers g & p specified by user.
#It has been tested on Linux Mint v3.19 x64
#Testing results .... of xxx in xxx seconds.

import sys
import math
import os
import itertools
import csv
import time

print "Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3."
print "Version 1. 23/08/2019."
print "Programmed & tested in Python 3.52 only"
print "This program works out the chinese remainder of two lists specified by user in ranges."
print "It has been tested on Linux Mint v3.19 x64"
print "Testing results .... of xxx in xxx seconds."
print "---------------------------------------------------------------------"
	
def main():
	
	result = legendre_symbol_g_p(g, p)
	print "legendre_symbol_g_p is: "+str(result)
	
def legendre_symbol_g_p(g,p):

	#print('Running legendre_symbol_g_p(',g,',',p,')...')

	#outputs the legendre symbol (g over p) for inputs g and p 
	#legendre_g_p(g over p) == -1 when g is a quadratic residue mod p and g % p !=0 
	#legendre_g_p(g over p) == 1 when g is a non-quadratic residue mod p
	#legendre_g_p(g over p) == 0 when g % p = 0

	power=int((p-1)/2)
	#print('power:',power)

	legendre_symbol_g_p=pow(g,power,p)

	if legendre_symbol_g_p > 1:
		legendre_symbol_g_p = legendre_symbol_g_p - p
	
	return legendre_symbol_g_p

if __name__=='__main__':
	main()
