#Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.
#Version 1. 25/05/2018.
#Programmed & tested in Python 3.4.3 only
#This program attempts to factorise a number N specified by user, via pollards rho. 
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in xxx seconds.

import sys
import math
import fractions
import csv
import os
import itertools
import time
	
version = 1

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

	result1 = pollards_rho_factorise(N)
	#return failure, c_factorisations OR d, c_factorisations
	status = result1[0]
	c_factorisations = result1[1]

	if status == "Failure":
		print("Algorithm failed! Time taken:",round(c_factorisations,8))
	else:
		print("factor:",status,"Time taken:",round(c_factorisations,8))

	#print("factors are:",factors)
	#print("time for factorisation is:",round(c_factorisations,8))
	
	#result2 = calc_primefactors_powers(N, factors)
	#return prime_factors, powers, c_calc_primefactors, c_calc_powers		
	#prime_factors = result2[0]
	#powers = result2[1]
	#c_calc_primefactors = result2[2]
	#c_calc_powers = result2[3]
	#total_calc_time = c_factorisations + c_calc_powers + c_calc_primefactors

	#print("prime factors are:",prime_factors)
	#print("powers are:",powers)
	#print("time for calc prime factors & powers is:",round(c_calc_powers + c_calc_primefactors,8))
	#print("total calc time is: ",round(total_calc_time,8))

def pollards_rho_factorise(n):		
	#based on code on https://en.m.wikipedia.org/wiki/Pollard%27s_rho_algorithm/
	#this is is O(???) and XXX times faster than trial division in practice
	
	print("Running pollards rho factorise(",n,")..")	

	s_before_factorisations = time.time()	
		
	x = 2
	y = 2
	d = 1

	while d == 1:
		x = g(x,n)	
		#print("g(x,n):",x)
		#print("g(y,n):",g(y,n))
		y = g(g(y,n),n)		
		#print("g(g(y,n)):",y)
		#print("abs(x-y):",abs(x-y))
		d = fractions.gcd(abs(x-y),n)

	c_factorisations = time.time() - s_before_factorisations

	if d == n:
		return "Failure", c_factorisations
	else:
		return d, c_factorisations
			
	#print("factors are: "+str(factors)
	#print("c_factorisations are: "+str(c_factorisations)

	#input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	#return factors, c_factorisations

def g(x,n):
	result = (x*x + 1) % n

	return result

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

	

