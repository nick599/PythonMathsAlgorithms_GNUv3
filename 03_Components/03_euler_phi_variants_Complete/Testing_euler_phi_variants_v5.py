# Testing_euler_phi_variants.py
# Version: 5

import math
import sys
try:
	from math import gcd as bltin_gcd
except ImportError:
	from fractions import gcd
import time
import csv

def main():

	#prime_list_path="/home/mint/Desktop/"
	#prime_list_filename="primes_upto_100000.csv"
	#primefile=prime_list_path + prime_list_filename
	#print('primefile currently is: '+str(primefile))

	#define prime list
	#print('Importing primes from csv file')
	#primes = csvfile_store_primes(primefile)
	#print('First ten primes are: '+str(primes[0:10]))
	
	test_range = xrange(1,1001)

	incorrect_result_checks(test_range)
	timing_loops(test_range)

def incorrect_result_checks(test_range):

	count_k = 0
	ep = 0
	for n in test_range:
		result1 = euler_phi_noprimesused(n)
		#return count_k, status	
		count_k = result1[0]
		status = result1[1]

		ep = euler_phi_primesused(n)
		#result2 = euler_phi_primesused(n)
		#return ep
		#ep = result2[0]
		#status = result2[1]

		if count_k <> ep:
			print "n is: "+str(n)+", euler_phi_noprimesused(n) is: "+str(count_k)+", euler_phi_primesused(n) is: "+str(ep)
			sys.exit()		 	
			break

def timing_loops(test_range):

	#print 'Enter number to be tested: '			#O(1)
	#n_initial = raw_input()					#O(1)
	#if n_initial.isdigit() is False:			#O(1)
	#	print('You have not entered a positive integer for n. n is: '+str(n_initial)+'. Please reenter.')
	#	sys.exit()						#O(1)

	#now convert n_initial into a long:
	#n = long(n_initial)					#O(1)
	
	#now want to time 50 runs of 1000 loops of euler_phi_primesused & euler_phi_noprimesused for the same xrange

	timing_test_range = xrange(1,51)
	len_timing_test_range = len(timing_test_range)

	total_time_primes_used = 0
	for y in timing_test_range:
		print "Primes used - Run "+str(y)		
		s_euler_phi_primesused = time.clock()	
		for n in test_range:
			result1 = euler_phi_primesused(n)
			#return ep, status
			#ep = result1[0]
			#status = result1[1]
		c_euler_phi_primesused = time.clock() - s_euler_phi_primesused
		total_time_primes_used = total_time_primes_used + c_euler_phi_primesused

	mean_time_primes_used = total_time_primes_used / float(len_timing_test_range)

	total_time_noprimes_used = 0
	for y in timing_test_range:
		print "Primes used - Run "+str(y)
		s_euler_phi_noprimesused = time.clock()
		for n in test_range:
			result2 = euler_phi_noprimesused(n)
			#return count_k, status	
			#count_k = result2[0]
			#status = result2[1]
		c_euler_phi_noprimesused = time.clock() - s_euler_phi_noprimesused
		total_time_noprimes_used = total_time_noprimes_used + c_euler_phi_noprimesused

	mean_time_noprimes_used = total_time_noprimes_used / float(len_timing_test_range)
	
	#if status == True:
	#	print "euler_phi_primesused("+str(n)+") is: "+str(ep)

	print "mean_time_primes_used is: "+str(mean_time_primes_used)+", mean_time_noprimes_used is: "+str(mean_time_noprimes_used)

	#print "T[euler_phi_primesused] is: "+str(c_euler_phi_primesused)+", T[euler_phi_noprimesused] is: "+str(c_euler_phi_noprimesused)


def euler_phi_noprimesused(n):	

	#euler_phi_noprimesused(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	
	#print "Running euler_phi_noprimesused("+str(n)+").."
	status = False					#O(1)
	count_k = 0	

	#gcd(n,k) --> b=min(n,k) 
	#==> h=#base 10 digits of b
	# now h = int(math.floor(math.log(b,10))) + 1
	# Hence h = int(math.floor(math.log(min(n,k),10))) + 1

	for k in xrange(1, n + 1):		#O(n)	#Subtotal: O(n*pow(h,2))			
		#print "-----------------"
		#print "k is: "+str(k)		
		g, x, y = egcd(n, k) 

		if g == 1:			#1 op for if. #O(pow(h,2)) for gcd
			#print "egcd("+str(n)+", "+str(k)+") is 1"
			status = True
			count_k = count_k + 1			#1 op
			#print "k is "+str(k)+", count_k is now: "+str(count_k)	
			

	#print "count_k is: "+str(count_k)
	if count_k <> 0:
		status=True
	else:
		status=False

	return count_k, status

def euler_phi_primesused(n):				
	
	#when n is not prime
	# Worst: O(sqrt(n)+8)  
	# Best:	O(4) when n=1

	#when n is prime
	#O(sqrt(n)+5) 
	
	#print "Running euler_phi_primesused("+str(n)+", primes).."
	
	#print "isprime_result is: "+str(isprime_result)

	#left_isprime_result=left()

	#status = True 					#O(1)
	#floor_sqrt_n = math.floor(math.sqrt(n))

	#print "isprime(n) is: "+str(isprime(n)
	#print "isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#status=1 for not prime
	#status=0 for prime

	if n==1:					#O(1)	#subtotal O(3)
		a = 1					#O(1)
		#status = False		
		return a				#O(1)
	else:							#subtotal O(???)
		#euler_phi(p**k) = (p-1)*p**(k-1) for prime p 
		#euler_phi(m*n) = euler_phi(m)*euler_phi(n) for coprime m & n

		#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.
		#n = p_1**(k_1)*p_2**(k_2)*p_3**(k_3)... , where p_i are prime factors of n, and k_i are corresponding powers.
		#n, and P_i are known 
		#need primes from factorise()!
				
		factors = factorise(n)					#O(sqrt(size(n)))
		#print "factors are: "+str(factors)
		
		prime_factors = calc_prime_factors(factors)		#O(???)			#Best operations: ??? 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		
		#print "prime factors are: "+str(prime_factors)
		
		len_prime_factors = len(prime_factors)

		#initialise ep
		ep=n
		#print "ep initialised as: "+str(ep)

		for prime in prime_factors:			#O(prime_factors)
			#now calculate first (1-1/p) for p|n
			#print "prime is: "+str(prime)
			term = 1 - 1 / float(prime)
			#print "term is: "+str(term)
		
			#recalculate ep
			ep = ep * term
			#print "ep is now: "+str(ep)

		ep = int(ep)
		#print "final ep is: "+str(ep)

		#raw_input("Waiting for user...")		

		#status = True				#O(1)
		return ep				#O(1)	

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print "Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.clock()	
	factors = []					#O(1)
	#c_lists = time.clock() - s_before_lists

	#print "Calculating prime factors and powers"
	#s_before_factorisations = time.clock()	
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
		
	#c_factorisations = time.clock() - s_before_factorisations	#O(1)

	#print "factors are: "+str(factors)
	#print "c_factorisations are: "+str(c_factorisations)

	#raw_input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors
	#return factors, c_factorisations		#O(1)

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

def calc_powers(factors):
	#Worst: O(n+13)	#Best: O(18)

	#print "Running calc_powers.."
	#print "factors is: "+str(factors)

	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	#powers = []						#O(1)
	fac_list = []						#O(1)
	count = 0						#O(1)
	#c_primefactors_powers = 0				#O(1)
	#s_before_calc_powers = time.clock()			#O(1)
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
				#powers.append(count)					#O(1)
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
	#powers.append(count)
	#print "Added "+str(count)+" to powers for previous factor"
	
	#print "prime_factors are: "+str(prime_factors)
	#print "powers are: "+str(powers)

	#c_pps=result2[3]
	#c_nrem=result2[4]

	#c_calc_powers = time.clock() - s_before_calc_powers

	return prime_factors
	#return prime_factors, powers
	#return prime_factors, powers, c_calc_powers

def csvfile_store_primes(csv_filename_var):		### Assumming O(n+len(z1)+1) ### 
		
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)			#O(n) - Potentially y rows and x items in each row, 
											# however only 1 row in csvfile being used. Hence x*y=x items to store
		primes=list(z1)								#O(len(z1))
		csvfile.close()								#O(1 ???)
	return primes

def egcd(a, b):							#O(n)
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:						#O(1)	#Subtotal: O(2)
		return (b, 0, a)				#O(1)
	g, y, x = egcd(b % a, a)				
	#print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
	return (g, x - (b//a) * y, y)

if __name__=='__main__':
	main()
