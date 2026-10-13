#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 3. 27/05/2018.
#Programmed & tested in Python 2.76 only
#This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
#import math
#import csv
#import os.path

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version 3. 27/05/2018.")
print("Programmed & tested in Python 2.76 only.")
print("This program checks if a number input by user is prime.")
print("It has been tested on Linux Mint v3.19 x64.")
print("Using Lists instead of sets for storage to minimise memory usage.")
print("---------------------------------------------------------------------")

def main():
	print("What is the number you want to test?")
	N_initial = input()
	if N_initial.isdigit() is False:
		print("You have not entered an integer. Please reenter.")
		sys.exit()

	#now convert type for N into a long:
	N = int(N_initial)
	
	#Simple Checks for N:
	if N==0:
		print("Number entered is 0. Please choose another number.")
		sys.exit()
	if N==1:
		print("1 is not a prime. Please choose another number.")
		sys.exit()
	if N<0:
		print("Number entered is negative. Please enter another number")
		sys.exit()

	#isprime_mem_usage_Kb = round(float(result[5]) / 1024, 1)
	
def isprime(p):		#this is O(sqrt(n))
	
	print("Running isprime(",p,")..")
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
	if p==2:
		return True
	
	i = 3
	while i*i <= p:
		if p % i == 0:
			return False
		i += 2

	return True

if __name__=='__main__':
	main()
