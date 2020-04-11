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

print "Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3."
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
	n_init = b + 1
	n_max = b * 20 + 1

	bin_coeffs=[]
	for number in xrange(n_init, n_max + 1, 2):	
		coeff = Bin_Coeffs_test(number, b, b_fac)
		bin_coeffs.append(coeff)

	print "Bin_coeffs mod n (for odd n from "+str(n_init)+" to "+str(n_max)+") for b: "+str(b)+" is: "+str(bin_coeffs)

def Bin_Coeffs_withmod(n):
	#nCr = (n r) = n! / r!*(n-r)!
	
	#print "Running Bin_Coeffs("+str(n)+").."	
	coeffs=[]
	for b in xrange(0, n + 1):	
		if (n == b) or (b == 0):
			#print "coeff("+str(n)+", "+str(b)+") is 1"
			coeffs.append(1)
			#return 1
		elif (b == 1) or b == n - 1:
			#print "coeff("+str(n)+", "+str(b)+") is "+str(0)
			coeffs.append(0)
			#return n
		elif (b == 2) or b == n - 2:
			#print "coeff("+str(n)+", "+str(b)+") is "+str(0)
			coeffs.append(0)
			#return n
		elif (b == 3) or b == n - 3:
			if n % 3 == 0:
				#print "coeff("+str(n)+", "+str(b)+") is "+str(n/3)
				coeffs.append(n/3)
				#return n
			else:
				#print "coeff("+str(n)+", "+str(b)+") is "+str(0)
				coeffs.append(0)
				#return n
		elif (b == 4) or b == n - 4:
			#print "coeff("+str(n)+", "+str(b)+") is "+str(0)
			coeffs.append(0)
			#return n
		elif (b == 5) or b == n - 5:
			if n % 5 == 0:
				#print "coeff("+str(n)+", "+str(b)+") is "+str(n/5)
				coeffs.append(n/5)
				#return n
			else:
				#print "coeff("+str(n)+", "+str(b)+") is "+str(0)
				coeffs.append(0)
				#return n
		else:
			n_fac = factorial(n)
			#print "n_fac is: "+str(n_fac)
			b_fac = factorial(b)
			#print "b_fac is: "+str(b_fac)
			n_minus_b_fac = factorial(n - b)
			#print "n_minus_b_fac is: "+str(n_minus_b_fac)
			result = n_fac / (b_fac * n_minus_b_fac)
			result_mod = int(result % n)
			#print "n_minus_b_fac is: "+str(n_minus_b_fac)
			#print "coeff("+str(n)+", "+str(b)+") is "+str(result)
			#raw_input("waiting for user..")
			coeffs.append(result_mod)
			#return result

	return coeffs

def Bin_Coeffs_withoutmod(n):
	#nCr = (n r) = n! / r!*(n-r)!
	
	#print "Running Bin_Coeffs("+str(n)+").."	
	coeffs=[]
	for b in xrange(0, n + 1):	
		if (n == b) or (b == 0):
			#print "coeff("+str(n)+", "+str(b)+") is 1"
			coeffs.append(1)
			#return 1
		elif (b == 1) or b == n - 1:
			#print "coeff("+str(n)+", "+str(b)+") is "+str(n)
			coeffs.append(n)
			#return n
		elif (b == 2) or b == n - 2:
			#print "coeff("+str(n)+", "+str(b)+") is "+str(n)
			coeffs.append(n*(n-1)/2)
			#return n
		elif (b == 3) or b == n - 3:
			#print "coeff("+str(n)+", "+str(b)+") is "+str(n)
			coeffs.append(n*(n-1)*(n-2)/6)
			#return n
		else:
			n_fac = factorial(n)
			#print "n_fac is: "+str(n_fac)
			b_fac = factorial(b)
			#print "b_fac is: "+str(b_fac)
			n_minus_b_fac = factorial(n - b)
			#print "n_minus_b_fac is: "+str(n_minus_b_fac)
			result = n_fac / (b_fac * n_minus_b_fac)
			#print "n_minus_b_fac is: "+str(n_minus_b_fac)
			#print "coeff("+str(n)+", "+str(b)+") is "+str(result)
			#raw_input("waiting for user..")
			print "result is: "+str(result)
			print "int(result) is: "+str(int(result))
			coeffs.append(int(result))
			#return result

	return coeffs

def Bin_Coeffs_test(n, b, b_fac):
	#nCr = (n r) = n! / r!*(n-r)!
	
	#print "Running Bin_Coeffs("+str(n)+","+str(b)+").."	
	#coeffs=[]
	
	n_fac = factorial(n)
	#print "n_fac is: "+str(n_fac)
	#b_fac = factorial(b)
	#print "b_fac is: "+str(b_fac)
	n_minus_b_fac = factorial(n - b)
	#print "n_minus_b_fac is: "+str(n_minus_b_fac)
	result = n_fac / (b_fac * n_minus_b_fac)
	#print "factorial is: "+str(result)
	#print "coeff("+str(n)+", "+str(b)+") is "+str(result)
	#raw_input("waiting for user..")
	result_mod = int(result % n) 
	#print "factorial mod "+str(n)+" is: "+str(result_mod)
	#print "result_mod is: "+str(result_mod)
	#print "int(result_mod) is: "+str(int(result_mod))
	#coeffs.append(result_mod)
	#return result

	return result_mod

def factorial(z):

	#print "Running factorial("+str(z)+").."
	if z == 1:
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

def check_prime(n):
	#Need to check if n is prime
	#print 'Checking if n is prime ..'
	a = isprime(p)					#O(sqrt(n))	
	#True for Prime
	#False for not prime	
	if a == False:					#1 op	#Best case: O(5)
		print('The number entered for n: '+str(n)+' is not prime.')		
		status=0													#O(1)
		count_a_notprime = count_a_notprime + 1										#O(1)
		sys.exit()													#O(1)

	#return status, a, b, q
	return status, a
	
def isprime(p):		#this is O(sqrt(n))
	
	print "Running isprime("+str(p)+").."
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	return True		

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	print "Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.clock()	
	factors = []					#1 op
	#c_lists = time.clock() - s_before_lists

	#print "Calculating prime factors and powers"
	#s_before_factorisations = time.clock()	
	#N=5 - gets listed as remainder instead of factor!!!	
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]			#1 op
	length, cycle = 11,3				#1 op
	f, factors, next = 2, [], 0			#1 op
	while f*f <= N:					#O(n)
		while N % f == 0:				#O(n)
			#f is a factor. Add factor f to fs
			factors.append(f)				#1 op
			N /= f						#1 op
		f += gaps[next]				#1 op
		next += 1				#1 op
		if next == length:			#1 op
			next = cycle				#1 op
	if N > 1: factors.append(N)
		
	#c_factorisations = time.clock() - s_before_factorisations	#O(1)

	#print "factors are: "+str(factors)
	#print "c_factorisations are: "+str(c_factorisations)

	#raw_input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors					#1 op
	#return factors, c_factorisations		
	
def calc_prime_factors(factors):
	#Worst: O(n+13)	#Best: O(18)

	#print "Running calc_powers.."
	#print "factors is: "+str(factors)

	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	fac_list = []						#O(1)
	
	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
		#print "------------------"	
		#print "factor is: "+str(factor)		
		if factor not in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
			#factor is not in fac_list - add factor to prime_factors
			prime_factors.append(factor)				#O(1)
			#print "Added "+str(factor)+" to prime_factors"
			fac_list.append(factor)					#O(1)
			#print str(factor)+" added to fac_list"
				
		else:								#O(1)	#Subtotal: O(4)
			##store factor
			fac_list.append(factor)						#O(1)
			#print str(factor)+" added to fac_list"

	return prime_factors


def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()


