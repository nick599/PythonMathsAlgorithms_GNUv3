#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 11. 07/04/2018.
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
#import itertools
#import csv
import time

print "Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3."
print "Version 11. 07/04/2018."
print "Programmed & tested in python 2.76 only."
print "---------------------------------------------------------------------"
print "This program attemps to check the primality of a prime via the AKS primality test."
print "Results printed are three arrays ..."
print "Prime list file should be a .CSV file with each prime separated by commas."
print "Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
print "It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to check a prime of xxx in xxx seconds."
print "---------------------------------------------------------------------"
	
def main():
	#prime_list_path="/home/mint/Desktop/"			#O(1)
	#prime_list_filename="primes_upto_100000.csv"		#O(1)
	#primefile=prime_list_path + prime_list_filename		#O(1)
	#print 'primefile currently is: '+str(primefile)
	
	#primes = csvfile_store_primes(primefile)

	#print(sys.version_info)

	print 'Enter prime to be tested: '			#O(1)
	n_initial = raw_input()					#O(1)
	if n_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for n. n is: '+str(n_initial)+'. Please reenter.')
		sys.exit()						#O(1)

	#now convert n_initial into a long:
	n = long(n_initial)					#O(1)

	print "---------------------"
	print "n: "+str(n)

	#define lists for different types of results
	#answers_to_be_checked=[]				#O(???)

	print("======================================")
	
	#step 1 - check if n is a perfect power
	perfect_power_result = perfect_power_check_a_b(n)	#O(???)
	#return status - False for perfect power, True for not.

	if perfect_power_result == False:
		print "n is Composite"

	elif perfect_power_result == True:
		#print "perfect_power_result is True"
		#step 2 - find smallest r such that order_r(n) > [log_2(n)]**2
		log_2_n = math.log(n,2)
		log_2_n_squared = pow(log_2_n, 2)
		#print "log_2_n is: "+str(log_2_n)
		smallest_r_result = smallest_r(n , log_2_n_squared, log_2_n)
		#return r, r_status
		r = smallest_r_result[0]
		r_status = smallest_r_result[1]

		if r_status == False:
			#r not found!
			print "r is not found for n !"
			sys.exit()
		elif r_status == True:
			#step 3 - for all 2 <= a <= min(r,n-1) check that a does not divide n.
			min_r_n_minus_1 = min(r,n-1)
			#print "min_r_n_minus_1 is: "+str(min_r_n_minus_1)
			a_divide_n_check_result = a_divide_n_check(n , min_r_n_minus_1)
				#if a|n for some a s.t. 2 <= a <= min_r_n_minus_1 then output "n is composite"
 
			#return a_value, status
		 	a = a_divide_n_check_result[0]
			a_status = a_divide_n_check_result[1]
			#a_status = True for n is composite

			if a == 0:
				#print "2 <= a <= "+str(min_r_n_minus_1)+" not found for a|"+str(n)+" !"

				#step 4 - check if n <=r - if true output "prime"
				if n > r:
					#step 5 - check if (x+a)**n congruence holds. If it doesn't output "n is composite"
					print "n is: "+str(n)+", r is: "+str(r)
					euler_phi_r_result = euler_phi_noprimesused(r)
					#return count_k, status
					ep = euler_phi_r_result[0]
					ep_status = euler_phi_r_result[1]

					if ep_status == False:
						print "ep_status is False!"						
						raw_input("Waiting for user..")

					elif ep_status == True:
						#now want to calc floor[sqrt(eulerphi(r)) * log_2(n)]							
						#print "euler_phi_r is: "+str(ep)
						sqrt_euler_phi_r = math.sqrt(ep)
						floor_sqrt_eulerphi_r_times_log_2_n = math.floor(sqrt_euler_phi_r * log_2_n)
						#print "floor_sqrt_eulerphi_r_times_log_2_n is: "+str(floor_sqrt_eulerphi_r_times_log_2_n)
						int_floor_sqrt_eulerphi_r_times_log_2_n = int(floor_sqrt_eulerphi_r_times_log_2_n)
						print "int_floor_sqrt_eulerphi_r_times_log_2_n is: "+str(int_floor_sqrt_eulerphi_r_times_log_2_n)
							
						#raw_input("What is x??")

						x_plus_a_cong_check_result = x_plus_a_cong_check(n, r, int_floor_sqrt_eulerphi_r_times_log_2_n)
						#return n_status 
						n_status = x_plus_a_cong_check_result
						if n_status == True:
							return "n is Prime"
						elif n_status == False:
							return "n is Composite"
						else:
							print "n_status is: "+str(n_status)
							sys.exit()
					else:
						print "n is: "+str(n)+", r is: "+str(r)
						raw_input("Waiting for user..")
				elif n <= r:
					return "n is Prime"				
				else:
					print "n is: "+str(n)+", r is: "+str(r)
					raw_input("Waiting for user..")
			else:
				print "a_status is: "+str(a_status) 	#O(1)
				sys.exit()
		else:
			print "r_status is: "+str(r_status)	 	#O(1)
			sys.exit()
	else:
		print "perfect_power_result is: "+str(perfect_power_result)
		sys.exit()

def perfect_power_check_a_b(n):

	#False for perfect power, True for not.
	print "Running perfect_power_check_a_b(n).."	
	a = math.sqrt(n)
	if a - int(a):
		print "Not perfect power: sqrt("+str(n)+") - int(sqrt("+str(n)+")): True: "+str(a - int(a))		
		#print "a is: "+str(a)+", pow(a,2) is: "+str(pow(a,2))+", n is: "+str(n)		
		#if pow(a,2) == n:
		#	print "CHECK! pow(a,2) is: "+str(pow(a,2))+" == n, n is: "+str(n)+", a is: "+str(a)
		#	sys.exit()
		return True
	else:
		print "perfect power: a - int(a): False: "+str(a - int(a))
		if pow(a,2) <> n:
			print "CHECK! pow(a,2) is: "+str(pow(a,2))+" == n, n is: "+str(n)+", a is: "+str(a)
			sys.exit()

		return False	#n is composite

def perfect_power_check_a_b_old(n):
	print "Running perfect_power_check_a_b_old("+str(n)+").."

	print "n is:"+str(n)

	#Worst: O(n + 7)	#Best: O(8)

	a=1						#O(1)
	b=1						#O(1)
	status=False					#O(1)
	while a < n:					#O(n)	#Worst: O(n**2+5n) 	#Best: 6 operations
		print "a is:"+str(a)
		if status== True:
			print "Perfect square found!"			
			break
		elif status== False:
			if a==1:			
				log_na = 0
			elif a==n:			
				log_na = 1
			else:
				log_na = math.log(n,a)
			#print "log base "+str(a)+" of "+str(n)+" is: "+str(log_na) 
			#print "math.log("+str(n)+","+str(a)+") is: "+str(log_na) 
			int_flr_log_na = int(math.floor(log_na))
			#print "int(math.floor(math.log("+str(n)+","+str(a)+"))) is: "+str(int_flr_log_na)
			upper_bound = int_flr_log_na + 1
			print "upper_bound is: "+str(upper_bound) 
			for b in xrange(1, upper_bound):	#O(n)	
				if pow(a,b) == n:					#O(2)	#Worst: O(6)
					print "a: "+str(a)+", b: "+str(b)			#O(1)
					status=True						#O(1)
					break							#O(1)
			
		else:
			print "status: "+str(status)
		a = a + 1
	return status

def smallest_r(n , log_2_n_squared, log_2_n):
	#find smallest r such that order_r(n) > log_2_n_squared
	#if f and n are not coprime, then SKIP this r.
	print "Running smallest_r("+str(n)+" , log_2_n_squared, log_2_n).."
	print "log_2_n is: "+str(log_2_n)
	print "log_2_n_squared is: "+str(log_2_n_squared)

	#intialise r
	r = 1

	# G is the Multiplicative Group - (Z/rZ)*
	#Z_r - denotes set of integers modulo r
	#F_p denotes finite field with p elements

	#order_r(n) = order of n modulo r
	#integer n, positive integer r with gcd(n,r)=1,
	#multiplicative order of n modulo r is the smallest integer k with pow(n,k,r)=1
	#r is unknown & we want to find.

	#print "pow(log_2_n, 5) is: "+str(pow(log_2_n,5))
	#print "math.ceil(pow(log_2_n, 5)) is: "+str(math.ceil(pow(log_2_n,5)))
	#print "int(math.ceil(pow(log_2_n, 5))) is: "+str(int(math.ceil(pow(log_2_n,5))))
	while r <= int(math.ceil(pow(log_2_n,5))):
		
		#print "r is now: "+str(r)		
		order_result = calc_order(n,r) 
		#return status, order
		#status is False for "no exponent found"	
		#status is True for exponent found
		status = order_result[0]					#O(1)
		order_r_n = order_result[1]					#O(1)
		#status = result[1]					
		
		#print "status is: "+str(status)
		#raw_input("Waiting for user..")	

		if status == False:
			#print "order_r_n is not found!"
			r = r + 1
		elif status == True:
			if order_r_n <= log_2_n_squared:
				r = r + 1
			elif order_r_n > log_2_n_squared:
				#check if r and n are coprime
				if gcd(r,n) <> 1:
					r = r + 1
				else:
					print "r found: "+str(r)
					status = True				
					return r, status		
			else:
				print "order_r_n: "+str(order_r_n)+", log_2_n_squared: "+str(log_2_n_squared)
				raw_input("Waiting for user..")
		else:
			print "order_r_n is: "+str(order_r_n)
			raw_input("Waiting for user..")

	if r == 1:
		status = False				
		return r, status
		print "r not found!"

def a_divide_n_check(n , min_r_n_minus_1):
	#if a|n for some a s.t. 2 <= a <= min_r_n_minus_1 then output "n is composite"
	#True for n is composite
	a_value = 0
	status = False
	for a in xrange(2, min_r_n_minus_1 + 1):
		if n % a == 0:
			print "n is composite!"
			status=True
			a_value = a			
			break

	return a_value, status

def x_plus_a_cong_check(n, r, int_floor_sqrt_eulerphi_r_times_log_2_n):
	
	#calc difference between n and r
	diff_n_minus_r = n - r 	
	print "n minus r is: "+str(diff_n_minus_r)

	#Step 1 - expand binomial (x+a)**n for n, and store result (result1), and print it.
	#need formula for nCr coefficients! -> n! / r!*(n-r)! ???
	#need formula for n!
	bin_coeffs=[]	
	print "Evaluating Bin_Coeffs for "+str(n)+".."
	#for b in xrange(0, n + 1):	
	result = Bin_Coeffs(n)
	print "len of Bin_Coeffs("+str(n)+") is: "+str(len(result))
	#print "Bin_Coeffs("+str(n)+") is: "+str(result)
	#bin_coeffs.append(result)
	print "bin_coeffs for "+str(n)+" are: "+str(result)
	#raw_input("Waiting for user..")


	#Step 2 - Compute polynomial remainder (x**r - 1) from result1 of expanded binomial and store result (result2), and print it.
	raw_input("Waiting for user..")



	#Step 3 - Compute polynomial remainder (x**r - 1) from result1 of expanded binomial and store result (result2), and print it.
	raw_input("Waiting for user..")


	#Step 4 - take away (x**n + a) from result2 of expanded binomial and store result (result3), and print it.
	



	#step 5 - take result3 mod(n), store it (result4), and print it.
	bin_coeffs=[]	
	print "Evaluating elements of bin_coeffs mod "+str(n)+".."
	bin_coeffs_mod_n=[]
	for number in bin_coeffs:	
		index = bin_coeffs.index(number)		
		number = number % n 
		print "bin_coeff["+str(index)+"] is: "+str(number)
		bin_coeffs_mod_n.append(number)
	print "bin_coeffs for "+str(n)+" are: "+str(bin_coeffs)
	raw_input("Waiting for user..")



	#step 4 - loop through values from a = 1 to int_floor_sqrt_eulerphi_r_times_log_2_n, testing if result3 = 0.
	# If result3 == 0 then prime, otherwise composite.




	return status

def Bin_Coeffs(n):
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
			coeffs.append((pow(n,2)-n)/2)
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
			coeffs.append(result)
			#return result

	return coeffs

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


def euler_phi_noprimesused(n):	

	#euler_phi_noprimesused(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	
	#print "Running euler_phi_noprimesused("+str(n)+").."
	status = False					#O(1)
	count_k = 0	

	for k in xrange(1, n + 1):		#O(n)	#Subtotal: O(n*pow(h,2))			#gcd(n,k) --> b=min(n,k) --> h=#base 10 digits of b
		if gcd(n,k) == 1:			#1 op for if. #O(pow(h,2)) for gcd
			count_k = count_k + 1			#1 op
	
	#print "count_k is: "+str(count_k)
	if count_k <> 0:
		status=True
	else:
		status=False

	return count_k, status

def exponent_g_p(g, p):
	#print "Running exponent_g_p("+str(g)+", "+str(p)+").."

	#Worst: O(n + 7)	#Best: O(8)

	n=1				#1 op
	x=0				#1 op
	status=False			#1 op
	while n < p:			#O(n)	#Worst: O(n + 1)
		#print "n is:"+str(n)
		if pow(g, n, p) == 1:		#O(2)	#Worst: O(1)
			x = n				#1 op
			status=True			#1 op
			break				#1 op
		elif pow(g, n, p) == -1:		#O(2)	#Worst: O(6)
			x = 2 * n			#O(1)
			status=True			#O(1)
			break				#O(1)
		n = n + 1			#1 op. O(0)

	if x==0:			#1 op
		x="No exponent found"			#1 op
		status=False				#1 op

	return x, status

def calc_order(n, r):

	#print "Running calc_order("+str(n)+", "+str(r)+").."
	#print "Need to calculate & check order for: "+str(n)+" mod "+str(r)
	
	#use exponent function to get order of n mod r
	result = exponent_g_p(n, r)				#Worst: O(n + 7)	#Best: O(8)
	#return x, status
	#status is False for "no exponent found"	
	#status is True for exponent found
	order = result[0]					#O(1)
	status = result[1]					#O(1)
	#status = result[1]					

	#print "order is: "+str(order)+", status is: "+str(status)

	return status, order

def check_prime(n):
	#Need to check if n is prime
	#print 'Checking if n is prime ..'
	a = isprime(p)					#O(sqrt(n))	
	#True for Prime
	#False for not prime	
	if a == False:					#O(1)	#Best case: O(5)
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
		result=pow(g,p-2,p)
		#result=g**(p-2)% p						#O(n+2)	#Subtotal O(2n+3)
		#print str(g)+"**(-1) mod "+str(p)+" is: "+str(result)
		c = pow(result,power,p)
		#c = result**power % p						#O(n+1)
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
		csvfile.close()								#1 operation
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

if __name__=='__main__':
	main()


