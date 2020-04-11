#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 3. 27/05/2018.
#Programmed & tested in Python 2.76 only
#This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
import time
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

primes_under_100 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,97]

def main():
	N = input_user_checks()	
	print("Checking if",N," is prime..")
	result_v3 = isprime_v3(N)
	result_SO = isprime_SO(N)

	if result_v3[0]== True or result_SO[0]==True: 
		print(N," is prime!")
		diff = abs(result_v3[1] - result_SO[1])
		print("abs(time_v3 - time_SO):",round(diff,6),", time_SO:",round(result_SO[1],6),", time_v3:",round(result_v3[1],6))
	else:
		print(N," is not prime!")

def input_user_checks():
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

	return N
	
def isprime_v3(p):		#this is O(sqrt(n))
	
	#print("Running isprime(",p,")..")
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	
	s_before_isprime_v3 = time.time()
	if p==1:
		c_after_isprime_v3 = time.time() - s_before_isprime_v3
		return False, c_after_isprime_v3
	if p==2:
		c_after_isprime_v3 = time.time() - s_before_isprime_v3
		return True, c_after_isprime_v3
	
	i = 3
	while i*i <= p:
		if p % i == 0:
			c_after_isprime_v3 = time.time() - s_before_isprime_v3
			return False, c_after_isprime_v3
		i += 2

	c_after_isprime_v3 = time.time() - s_before_isprime_v3
	return True, c_after_isprime_v3

def isprime_SO(p):		#this is O(sqrt(n))
	
	#print("Running isprime(",p,")..")
	# http://stackoverflow.com/questions/4545114/quickly-determine-if-a-number-is-prime-in-python-for-numbers-1-billion
	
	s_before_isprime_SO = time.time()
	if p<=100:
		return (p in primes_under_100), c_after_isprime_SO

	if p % 2 ==0 or p % 3 == 0:
		c_after_isprime_SO = time.time() - s_before_isprime_SO
		return False, c_after_isprime_SO
	
	for f in range(5, int(p ** .5),6):
		if p % f == 0 or p % (f+2) == 0:
			c_after_isprime_SO = time.time() - s_before_isprime_SO
			return False, c_after_isprime_SO
	c_after_isprime_SO = time.time() - s_before_isprime_SO
	return True, c_after_isprime_SO

if __name__=='__main__':
	main()
