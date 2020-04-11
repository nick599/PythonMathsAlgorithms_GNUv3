#Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.
#Version 2. 27/08/2019.
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

print("Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.")
print("Version 2. 27/08/2019.")
print("Programmed & tested in Python 3.52 only")
print("This program works out the chinese remainder of two lists specified by user in ranges.")
print("It has been tested on Linux Mint v3.19 x64")
print("Testing results .... of xxx in xxx seconds.")
print("---------------------------------------------------------------------")
	
def main():
	
	result = leg_s_g_p_new(g, p)

	print("legendre_symbol_g_p is:",str(result))
	
def leg_s_g_p_new(g,p):

	print('Running leg_s_g_p_new(',g,',',p,')...')

	#outputs the legendre symbol (g over p) for inputs g and p 
	#legendre_g_p(g over p) == -1 when g is a quadratic residue mod p and g % p !=0 
	#legendre_g_p(g over p) == 1 when g is a non-quadratic residue mod p
	#legendre_g_p(g over p) == 0 when g % p = 0

	#power=int((p-1)/2)
	#print('power:',power)

	#legendre_symbol_g_p=pow(g,power,p)

	if g==-1:
		if p % 4 == 1:
			print("g=-1 and p mod 4 = 1")			
			legendre_symbol_g_p=1
		elif p % 4 == 3:
			print("g=-1 and p mod 4 = 3")
			legendre_symbol_g_p=-1			
	elif g==2:
		if p % 8 == 1 or p % 8 == -1:
			print("g=2 and p mod 8 = +-1")
			legendre_symbol_g_p=1
		elif p % 8 == 3 or p % 8 == -3:
			print("g=2 and p mod 8 = +-3")
			legendre_symbol_g_p=-1
	else:
		#print("running factorise(",g,")")
		result=factorise_powers(g)
		#return prime_factors, powers, round(c_calc_primefactors,8), round(c_calc_powers,8), round(total_calc_time,8)
		prime_factors=result[0]
		powers=result[1]
		print(result)

		powers_new=[]
		for power in powers:
			if power >=2:
				powers_new.append(power % 2)
			else:
				powers_new.append(power)

		print("powers mod 2:",powers_new)

		leg_new=[]
		c=0
		for power in powers_new:
			leg_temp=[]
			if power==1:
				#print("c:",c)
				#print("power:",power)
				factor_temp=prime_factors[c]
				#print("factor_temp:",factor_temp)		
				leg_temp.append(factor_temp)
				leg_temp.append(p)
				leg_new.append(leg_temp)
			c=c+1

		print("legendre_symbols to calculate:",leg_new)

		legendre_symbol_g_p=0

	if legendre_symbol_g_p > 1:
		legendre_symbol_g_p = legendre_symbol_g_p - p
	
	return legendre_symbol_g_p

def factorise_powers(N):

	#call number_checks() for simple checks on input 
	#number_checks(N)	
	
	#Call size_input_check() if want to stop program running for very large numbers 
	#size_input_check()

	result1 = factorise(N)
	#return factors, c_factorisations
	factors = result1[0]
	c_factorisations = result1[1]

	#print("factors are:",factors)
	#print("time for factorisation is:",round(c_factorisations,8))
	
	result2 = calc_primefactors_powers(N, factors)
	#return prime_factors, powers, c_calc_primefactors, c_calc_powers		
	prime_factors = result2[0]
	powers = result2[1]
	c_calc_primefactors = result2[2]
	c_calc_powers = result2[3]
	total_calc_time = c_factorisations + c_calc_powers + c_calc_primefactors

	#print("prime factors are:",prime_factors)
	#print("powers are:",powers)
	#print("time for calc prime factors & powers is:",round(c_calc_powers + c_calc_primefactors,8))
	#print("total calc time is: ",round(total_calc_time,8))

	return prime_factors, powers, round(c_calc_primefactors,8), round(c_calc_powers,8), round(total_calc_time,8)

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print("Running factorise()..")	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.time()	
	factors = []
	#c_lists = time.time() - s_before_lists

	#print("Calculating prime factors and powers"
	s_before_factorisations = time.time()	
	#N=5 - gets listed as remainder instead of factor!!!	
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]
	length, cycle = 11,3
	f, factors, next = 2, [], 0
	while f*f <= N:
		while N % f == 0:		
			#f is a factor. Add factor f to fs
			factors.append(f)
			N /= f
		f += gaps[next]		
		next += 1
		if next == length:
			next = cycle
	if N > 1: factors.append(int(N))
		
	c_factorisations = time.time() - s_before_factorisations

	#print("factors are: "+str(factors)
	#print("c_factorisations are: "+str(c_factorisations)

	#input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem

def calc_primefactors_powers(N, factors):
	#print("------------------"
	#print("Running calc_primefactors_powers(",factors,")..")
	
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]
	fac_list = []
	c_calc_primefactors = 0
	s_before_primefactors = time.time()	
	for factor in factors:		
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if factor not in fac_list:
			#factor is not in fac_list
			#add factor to prime_factors
			prime_factors.append(factor)
			#print("Added "+str(factor)+" to prime_factors"
			#print("prime_factors is: "+str(prime_factors)
			#print str(factor)+" is NOT in fac_list"
			#append it				
			fac_list.append(factor)				
			
			#print("count is: "+str(count)
			#print("fac_list is: "+str(fac_list)
				
		else:
			#factor is in fac_list
			fac_list.append(factor)
			#print str(factor)+" added to fac_list"
	
	#prime_factors = fs
	#print("prime_factors are: "+str(prime_factors)
	#prime_factors.append(factor)
	#print("Added "+str(factor)+" to prime_factors"
	
	#print("prime_factors are: "+str(prime_factors)
	c_calc_primefactors = time.time() - s_before_primefactors

	powers = []
	s_before_calc_powers = time.time()
	for prime_factor in prime_factors:
		count = 0
		while N % prime_factor == 0:
			count = count + 1
			N = N / prime_factor		
		else:
			powers.append(count)
				
	#print("powers are: "+str(powers)
	c_calc_powers = time.time() - s_before_calc_powers

	#input("Waiting for user..")	

	return prime_factors, powers, c_calc_primefactors, c_calc_powers

if __name__=='__main__':
	#main()
	#result = leg_s_g_p_new(2, 1009)
    #result = leg_s_g_p_new(51, 1009)
	result = leg_s_g_p_new(513, 100907)

	print("legendre_symbol_g_p is:",str(result))

#def legendre_symbol_g_p(g,p):
#
#	#print('Running legendre_symbol_g_p(',g,',',p,')...')
#
#	#outputs the legendre symbol (g over p) for inputs g and p 
#	#legendre_g_p(g over p) == -1 when g is a quadratic residue mod p and g % p !=0 
#	#legendre_g_p(g over p) == 1 when g is a non-quadratic residue mod p
#	#legendre_g_p(g over p) == 0 when g % p = 0
#
#	power=int((p-1)/2)
#	#print('power:',power)
#
#	legendre_symbol_g_p=pow(g,power,p)
#
#	if legendre_symbol_g_p > 1:
#		legendre_symbol_g_p = legendre_symbol_g_p - p
#	
#	return legendre_symbol_g_p
