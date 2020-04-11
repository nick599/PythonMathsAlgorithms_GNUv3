# 24/04/2018
# Version 1
# Licenced under GNU GPL v3
# python3

#import sys
#import math
#import os
#import itertools
#import csv
#import time

def main():
	#print "What is a?"
	a_initial=input("What is a?\n")
	m_initial=input("What is m?\n")

	#Check if a is a digit
	if a_initial.isdigit() == False:
		print(a," is not a number! Exiting..")

	#Check if a is a digit
	if m_initial.isdigit() == False:
		print(m," is not a number! Exiting..")

	#convert a & m to integers
	a = int(a_initial)
	m = int(m_initial)

	modinv(a, m)
	#modinv(a_initial, m_initial)

def egcd(a, b):
	#print("Running egcd(",a,",",b,")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:
		#print("STOPPING since a is 0. Result: (",b,", 0, ",a,")")
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b//a) * y, y)

def modinv(a, m):
	print("Running modinv(",a,",",m,")")	
	#print("a is:",a)
	#print("m is:",m)	
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('No Modular Inverse') 
	print(a,"**(-1) mod ",m," is: ",x % m)	
	return x % m

if __name__=='__main__':
	main()



