#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 2. 10/04/2018.
#Programmed & tested in Python 2.76 only
#This program ...
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to check a prime of xxx in xxx seconds.

import sys
import math
#try:
#	from math import gcd as bltin_gcd
#except ImportError:
#	from fractions import gcd
#import os
#import itertools
#import csv
#import time

print "Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3."
print "Version 2. 10/04/2018."
print "Programmed & tested in python 2.76 only."
print "This program ..."
print "It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to check a prime of xxx in xxx seconds."
print "---------------------------------------------------------------------"
	
def main():
	#print(sys.version_info)

	print 'Enter value of b to be tested: '			#O(1)
	b_initial = raw_input()					#O(1)
	if b_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for b. b is: '+str(b_initial)+'. Please reenter.')
		sys.exit()						#O(1)

	#now convert b_initial into a long:
	b = long(b_initial)					#O(1)

	b_fac = factorial(b)

	print str(b)+"! is: "+str(b_fac)

def factorial(z):

	#print "Running factorial("+str(z)+").."
	if z == 0 or z == 1:
		return 1
	elif z >= 2:	
		#initialise answer
		answer = 1
		#print "Initial answer is: "+str(answer)
		for b in xrange(z, 1, -1):
			#print "b is now: "+str(b)			
			answer = answer * b
			#print "answer is now: "+str(answer)
		#print str(z)+"! is: "+str(answer)

	return answer

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()


