#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 1. 19/03/2018.
#Programmed & tested in Python 2.76 only
#This program attemps to check the primality of a prime via the AKS primality test. 
#Results ...
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to check a prime of xxx in xxx seconds.

#*** Potentially confusing O() with number of operations - post question on Math.SE ?? ***

import sys
import math
try:
	from math import gcd as bltin_gcd
except ImportError:
	from fractions import gcd
import os
import itertools
import csv
import time

print "Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3."
print "Version 1. 19/03/2018."
print "Programmed & tested in python 2.76 only."
print "---------------------------------------------------------------------"
print "This program attemps to check the primality of a prime via the AKS primality test."
print "Results printed are three arrays ..."
print "Prime list file should be a .CSV file with each prime separated by commas."
print "Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
print "It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds"
print "---------------------------------------------------------------------"
	
def main():
	prime_list_path="/home/mint/Desktop/"			#O(1)
	prime_list_filename="primes_upto_100000.csv"		#O(1)
	primefile=prime_list_path + prime_list_filename		#O(1)
	print 'primefile currently is: '+str(primefile)

	#print(sys.version_info)

	print 'Enter prime to be tested'			#O(1)
	p_initial = raw_input()					#O(1)
	if p_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for p. p is: '+str(p_initial)+'. Please reenter.')
		sys.exit()						#O(1)

	#now convert h into a long:
	p = long(p_initial)					#O(1)

	print "---------------------"
	print "prime: "+str(prime)

	#define counts for different types of results
	count_nosolns=0						#O(1)
	count_normal_soln=0					#O(1)
	count_needlargerprimelist=0				#O(1)
	count_a_notprime=0					#O(1)
 	count_order_not_prime=0					#O(1)

	#define lists for different types of results
	answers_to_be_checked=[]				#O(???)

	print("======================================")

	result = aks_primality_test()
	#return 

	#x=result[0]						#O(1)
	#M=result[1]						#O(1)
	prime_status=result[0]					#O(1)

	if prime_status == True:
		print "Result: "+str(prime)+" is Prime"		#O(1)
	elif prime_status == False:
		print "Result: "+str(prime)+" is NOT Prime" 	#O(1)
	else: 
		"prime_status is: "+str(prime_status)
		"prime is: "+str(prime)

def aks_primality_test():


	return

def ghp_checks(g,p,h,floor_sqrt_p, count_a_notprime):	
	
	print "Running ghp_checks().."

	#Assuming p is prime: 		Best case: O(sqrt(n)+5)		Worst case: O(sqrt(n)+8)
	#Assuming p is not prime: 	O(sqrt(n)+5)

	status=1
	
	#Simple Checks for g & h:
	if (g==0 or h==0):				#O(1)
		print('One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.')
		status=0												#O(1)
		sys.exit()												#O(1)
	elif g==1:					#O(1)
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
		status=0												#O(1)
		sys.exit()												#O(1)
	elif g<0:					#O(1)
		print('Number for g is negative. Please enter another number.')
		status=0												#O(1)
		sys.exit()												#O(1)
	
	#Check if g = p:
	elif g == p:
		print('g = p. x is any integer. Please enter other numbers for g and p.')
		status=0												#O(1)
		sys.exit()												#O(1)

	#Check if g = h:
	#elif g == h:
	#	print('g = h. x is 1. Please enter other numbers for g and p.')
	#	status=0												#O(1)
	#	sys.exit()	

	#Check if h < p:
	elif h >= p:
		print('h is >= p. Please enter other numbers for h and p.')
		status=0												#O(1)
		sys.exit()												#O(1)

	#Need to check if p is prime
	#print('Checking if p is prime ..')
	a = isprime(p)					#O(sqrt(n))	
	#True for Prime
	#False for not prime	
	if a == False:					#O(1)	#Best case: O(5)
		print('The number entered for p: '+str(p)+' is not prime. Please choose a number that is prime for p.')		
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

def exponent_g_n(g, h_value, p):
	print "Running exponent_g_n("+str(g)+","+str(h_value)+","+str(p)+").."

	#Worst: O(n + 7)	#Best: O(8)

	n=1						#O(1)
	x=0						#O(1)
	status=False					#O(1)
	while n < p:					#O(n)	#Worst: O(n + 7)
		#print "n is:"+str(n)
		if pow(g,n,p) == h_value:		#O(2)	#Worst: O(6)
		#if generator**n % p == h_value:		#O(n+2)	#Worst: O(n+6)
			x = n				#O(1)
			status=True			#O(1)
			break				#O(1)
		n = n + 1				#O(1)

	if x==0:					#O(1)
		x="No exponent found"			#O(1)
		status=False				#O(1)

	return x, status

def calc_modinverse(g, power, p):
	#print "----------------"
	print "Running calc_modinverse().."					#O(1)
	#print "g is: "+str(g)
	#print "power is: "+str(power)
	#raw_input("Waiting for user..")	

	#print "p is: "+str(p) #p = 1 ?????

	floor_sqrt_p = math.floor(math.sqrt(p))					#O(2)

	#this only works for p being prime!	
	if isprime(p) == True:							#O(1)	#Subtotal O(2n+4)
	#if isprime(p,floor_sqrt_p) == 0:	
		result=g**(p-2)% p						#O(n+2)	#Subtotal O(2n+3)
		#print str(g)+"**(-1) mod "+str(p)+" is: "+str(result)
		c = result**power % p						#O(n+1)
		#print "c is: "+str(c)	
		#print str(g)+"**(-"+str(power)+") mod "+str(p)+" is: "+str(c)
	else:
		#p is not prime!
		#print "p: "+str(p)+" is not prime!"
		c = modinv(g, p)						#O(n)
		#return x % m
		#print "inverse is: "+str(c)		

		#raw_input("Waiting for user..")	
	return c

def csvfile_store_primes(csv_filename_var):		### Assumming O(n+len(z1)+1) ### 
		
	print('Importing primes from csv file..')
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to getse) number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)			#O(n) - Potentially y rows and x items in each row, 
											# however only 1 row in csvfile being used. Hence x*y=x items to store
		primes=list(z1)								#O(len(z1))
		csvfile.close()								#O(1 ???)
	return primes

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	print "Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.clock()	
	factors = []					#O(1)
	#c_lists = time.clock() - s_before_lists

	#print "Calculating prime factors and powers"
	s_before_factorisations = time.clock()	
	#N=5 - gets listed as remainder instead of factor!!!	
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]			#O(1)
	length, cycle = 11,3				#O(1)
	f, factors, next = 2, [], 0			#O(1)
	while f*f <= N:					#O(n)
		while N % f == 0:				#O(n)
			#f is a factor. Add factor f to fs
			factors.append(f)				#O(1)
			N /= f						#O(1)
		f += gaps[next]				#O(1)
		next += 1				#O(1)
		if next == length:			#O(1)
			next = cycle				#O(1)
	if N > 1: factors.append(N)
		
	c_factorisations = time.clock() - s_before_factorisations	#O(1)

	#print "factors are: "+str(factors)
	#print "c_factorisations are: "+str(c_factorisations)

	#raw_input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors, c_factorisations		#O(1)
	
def calc_powers(factors):
	#Worst: O(n+13)	#Best: O(18)

	print "Running calc_powers.."
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	powers = []						#O(1)
	fac_list = []						#O(1)
	count = 0						#O(1)
	c_primefactors_powers = 0				#O(1)
	s_before_calc_powers = time.clock()			#O(1)
	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
		#print "------------------"	
		#print "factor is: "+str(factor)		
		if fac_list:						#O(1)	#Worst: O(n+2)	#Best: O(4)
			#temp factor list for comparisons has values
			if factor in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
				#print str(factor)+" is in fac_list"
				count += 1						#O(1)
				#print "count is: "+str(count)
				#temp_factor, temp_count = factor, count
				#print temp_factor, temp_count
			else:							#O(1)
				#factor is not in fac_list
				#add factor to prime_factors
				prime_factors.append(factor)				#O(1)
				#print "Added "+str(factor)+" to prime_factors"
				#print "prime_factors is: "+str(prime_factors)
				#add current count to powers for previous factor
				#print "count is: "+str(count)
				powers.append(count)					#O(1)
				#print "Added "+str(count)+" to powers for previous factor"
				#count = 0
				#print str(factor)+" is NOT in fac_list"
				#append it				
				fac_list.append(factor)					#O(1)
				#count += 1
				count = 1						#O(1)
				#print "count is: "+str(count)
				#print "fac_list is: "+str(fac_list)
				
		else:								#O(1)	#Subtotal: O(4)
			#temp factor list for comparisons is empty
			#store 1st factor
			#print "fac_list is empty"
			fac_list.append(factor)						#O(1)
			#print str(factor)+" added to fac_list"
			prime_factors.append(factor)					#O(1)
			#print "Added "+str(factor)+" to prime_factors"
			#print "prime_factors is: "+str(prime_factors)			
			count += 1							#O(1)
			#print "count is: "+str(count)	

	#add count to powers for the last factor and the last factor
	powers.append(count)
	#print "Added "+str(count)+" to powers for previous factor"
	
	#print "prime_factors are: "+str(prime_factors)
	#print "powers are: "+str(powers)

	#c_pps=result2[3]
	#c_nrem=result2[4]

	c_calc_powers = time.clock() - s_before_calc_powers

	return prime_factors, powers, c_calc_powers

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()

def egcd(a, b):							#O(n)
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:						#O(1)	#Subtotal: O(2)
		return (b, 0, a)				#O(1)
	g, y, x = egcd(b % a, a)				
	#print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
	return (g, x - (b//a) * y, y)

def modinv(a, m):						#### O(n+5) ###
	print("Running modinv("+str(a)+","+str(m)+")")		
	#print "a is: "+str(a)
	#print "m is: "+str(m)	
	#egcd(a, m)
	g, x, y = egcd(a, m)					#O(n)
	if g != 1:							#O(1)	#Subtotal: O(2)
		raise Exception('No Modular Inverse') 			#O(1)
	print(str(a)+"**(-1) mod "+str(m)+" is: "+str(x % m))	
	return x % m						#O(1)
