#Copyright Nick Prowse 2017. Code Licenced under GNU GPL3.
#Version 5. 25/05/2018.
#Programmed & tested in Python 3.4.3 only
#This program attempts to factorise a number N specified by user, via wheel-factorisation using a 2,3,5-wheel. 
#Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second.

import sys
import math
import csv
import os
import itertools
import time

version = 5

def main():
	#prime_list_path="/home/mint/Desktop/"
	#prime_list_filename="primes_upto_100000.csv"
	#primefile=prime_list_path + prime_list_filename

	print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.")
	print("Version:",version,". 25/05/2018.")
	print("Programmed & tested in Python 3.4.3 only.")
	print("This program attempts to factorise a number N specified by user, via wheel-factorisation using a 2,3,5-wheel.")
	print("Results printed are three arrays - first for prime factors, second for powers of those primes.")
	#print("Prime list file should be a .CSV file with each prime separated by commas."
	#print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
	#print("The larger the prime file is that is used, the longer the factorisation will take!"
	print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second.") 
	print("---------------------------------------------------------------------")
	
	#Check if primefile exists.
	#if os.path.exists(primefile) is False:
	#	#File doesn't exist in location. Exit process.
	#	print('Prime file doesn\'t exist in location specified. Exiting.')
	#	sys.exit()

	#print('Using primefile: '+str(primefile))
	
	print('Number to attempt to factorise?')
	N_initial = input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()	

	#now convert type for N into a long:
	N = int(N_initial)

	#call number_checks() for simple checks on input 
	number_checks(N)	
	
	#Call size_input_check() if want to stop program running for very large numbers 
	#size_input_check()

	result1 = factorise(N)
	#return factors, c_factorisations
	factors = result1[0]
	c_factorisations = result1[1]

	print("factors are:",factors)
	print("time for factorisation is:",round(c_factorisations,8))
	
	result2 = calc_primefactors(factors)
	#return prime_factors, c_calc_powers		
	prime_factors = result2[0]
	#powers = result2[1]
	
	c_calc_primefactors = result2[1]
	print("c_calc_primefactors:",round(c_calc_primefactors,8))
	total_calc_time = c_factorisations + c_calc_primefactors

	print("prime factors are:",prime_factors)
	#print("powers are: "+str(powers)
	#print("time for calc prime factors is: "+str(c_calc_primefactors)
	print("total calc time is:",round(total_calc_time,8))

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	print("Running factorise(",N,")..")	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.time()	
	factors = []
	#c_lists = time.time() - s_before_lists

	#print("Calculating prime factors and powers"
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]
	length, cycle = 11,3
	f, factors, next = 2, [], 0
	s_before_factorisations = time.time()
	while f*f <= N:
		while N % f == 0:		
			#f is a factor. Add factor f to fs
			factors.append(f)
			print("appended "+str(f)+" to factors..")
			N /= f
		f += gaps[next]		
		next += 1
		if next == length:
			next = cycle
	#print("N:",N)
	#print("int(N):",int(N))
	if N > 1: factors.append(int(N))
		
	c_factorisations = time.time() - s_before_factorisations

	#print("factors are: "+str(factors)
	#print("c_factorisations are: "+str(c_factorisations)

	#input("Waiting for user..")	

	return factors, c_factorisations

def calc_primefactors(factors):
	#print("------------------"
	print("Running calc_primefactors..")
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]
	#powers = []
	fac_list = []
	#count = 0
	c_primefactors_powers = 0
	s_before_calc_powers = time.time()	
	for factor in factors:		
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if factor not in fac_list:
			#factor is not in fac_list
			#print(str(factor)+" is NOT in fac_list"
			#add factor to prime_factors
			prime_factors.append(factor)
			#print("Added "+str(factor)+" to prime_factors"
			#print("prime_factors is: "+str(prime_factors)
			#append it				
			fac_list.append(factor)	
			#print("fac_list is: "+str(fac_list)
		else:
			#temp factor list for comparisons is empty
			fac_list.append(factor)
			#print(str(factor)+" added to fac_list"
			#prime_factors.append(factor)
			#print("Added "+str(factor)+" to prime_factors"
			#print("prime_factors is: "+str(prime_factors)			
			
	#prime_factors.append(factor)
	#print("Added "+str(factor)+" to prime_factors"
	#print("prime_factors are: "+str(prime_factors)
	
	#print("prime_factors are: "+str(prime_factors)

	c_calc_powers = time.time() - s_before_calc_powers

	return prime_factors, c_calc_powers
	#return prime_factors, powers, c_calc_powers

def number_checks(number):

	#Simple Checks for N:
	#print('Running simple checks for number...')
	if number==0:
		print('Number entered is 0. Please choose another value for N')
		sys.exit()
	if number==1:
		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
		sys.exit()
	if number<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()

	

