#Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.
#Version 2. 06/09/2019.
#Programmed & tested in Python 3.4.3 only
#This program tests a number provided by user for primality
#It has been tested on Linux Mint v3.19 x64.
#Using lists instead of sets for storage to minimise memory usage

import sys
#import math
#import csv
#import os.path

version = 2

print("Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.")
print("Version",version,"06/09/2019.")
print("Programmed & tested in Python 3.5.2 only.")
print("This program checks if a number input by user is prime.")
print("It has been tested on Linux Mint Ubuntu v4.40-Generic x64.")
print("Using Lists instead of sets for storage to minimise memory usage.")
print("---------------------------------------------------------------------")

primes_under_100 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,97]

def main():
	print("What is the number you want to test?")
	N_initial = input()
	if N_initial.isdigit() is False:
		print("You have not entered an integer. Please reenter.")
		sys.exit()

	#now convert type for N into a long:
	#N = long(N_initial)
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
	
	result=isprime(N)

	if result==False:
		print(N,"is NOT prime")
	else:
		print(N,"is prime!")

def isprime(p):		#this is O(sqrt(n))
	
	#print("Running isprime(",p,")..")
	# http://stackoverflow.com/questions/4545114/quickly-determine-if-a-number-is-prime-in-python-for-numbers-1-billion
	
	if p<=100:
		return p in primes_under_100

	if p % 2 ==0 or p % 3 == 0:
		if p % 2 ==0:
			print(p,"mod 2 = 0")
		if p % 3 ==0:
			print(p,"mod 3 = 0")		
		return False	
	
	for f in range(5, int(p ** .5),6):
		if p % f == 0 or p % (f+2) == 0:
			if p % f == 0:			
				print(p,"mod",f,"= 0")	
				return False
			if p % (f+2) == 0:			
				print(p,"mod",f+2,"= 0")	
				return False
	return True

if __name__=='__main__':
	main()
	#isprime(396836483) - Prime
