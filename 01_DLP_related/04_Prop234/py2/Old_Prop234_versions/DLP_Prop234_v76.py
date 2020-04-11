#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 76. 04/03/2018.
#Programmed & tested in Python 2.76 only
#This program attemps to solve a Discrete Log Problem (DLP) specified by user, via Proposition 2.34 (in J Hoffstein, J Pipher & J Silverman), via factorisation of (p-1) where p is a prime number. 
#Results printed are three arrays ...
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

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

print("Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.")
print("Version 76. 04/03/2018.")
print("Programmed & tested in python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via Proposition 2.34 (in J Hoffstein, J Pipher & J Silverman), via factorisation of (p-1) where p is a prime number.")
print("Results printed are three arrays ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")
	
def main():
	prime_list_path="/home/mint/Desktop/"			#O(1)
	prime_list_filename="primes_upto_100000.csv"		#O(1)
	primefile=prime_list_path + prime_list_filename		#O(1)
	print('primefile currently is: '+str(primefile))

	#print(sys.version_info)

	print('What is g?')					#O(1)
	g_initial = raw_input()					#O(1)
	if g_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for g. g is: '+str(g_initial)+'. Please reenter.')	
		sys.exit()						#O(1)

	#now convert g into a long:
	g = long(g_initial)					#O(1)

	print('What is h?')					#O(1)
	h_initial = raw_input()					#O(1)
	if h_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for h. h is: '+str(h_initial)+'. Please reenter.')
		sys.exit()						#O(1)

	#now convert h into a long:
	h = long(h_initial)					#O(1)

	print('What is p?')					#O(1)
	p_initial = raw_input()					#O(1)
	if p_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for p. p is: '+str(p_initial)+'. Please reenter.')
		sys.exit()						#O(1)

	#now convert p into a long:
	p = long(p_initial)					#O(1)

	print("---------------------")
	print("g: "+str(g)+", h: "+str(h)+", p: "+str(p))

	#define counts for different types of results
	count_nosolns=0						#O(1)
	count_x_equals_0=0					#O(1)
	count_normal_soln=0					#O(1)
	count_needlargerprimelist=0				#O(1)
	#count_brute_force_soln=0
	count_q_e_found=0					#O(1)
	count_q_e_not_found=0					#O(1)
	count_a_notprime=0					#O(1)
 	count_calc_xi_no_solns=0				#O(1)
	count_order_not_prime=0					#O(1)

	#define lists for different types of results
	answers_to_be_checked=[]				#O(???)

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print("======================================")

	#result = dlp(g, h, p, primefile, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_q_e_found, count_q_e_not_found, count_order_not_prime, count_calc_xi_no_solns, count_a_notprime)	#O(1)

	result = dlp(g, h, p, primefile, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_q_e_found, count_q_e_not_found, count_order_not_prime, count_calc_xi_no_solns, count_a_notprime)	#O(1)

	#return x, count_nosolns, count_x_equals_0, count_normal_soln, x_moduli, count_diffeq0, count_order_not_prime, count_q_e_not_found, count_calc_xi_no_solns

	x=result[0]						#O(1)
	M=result[4]						#O(1)
	
	print "Final solution: x= "+str(x)+" mod "+str(M)	#O(1)

def ghp_checks(g,h,p,floor_sqrt_p, count_a_notprime):	
	
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

def prim_root(g, p, n_prime):
#def prim_root(g,p,primes):

	print "Running prim_root("+str(g)+", "+str(p)+").."

	#Assuming p is prime: 		Best case: O(46)	Worst case: O(???)
	#Assuming p is not prime: 	O()
	
	if p in n_prime:				#O(n)
		#we have already ran isprime(p) and it was prime
		#hence ep = p-1
		ep = p - 1					#O(1)	
		status_ep = True				#O(1)
	else:						#O(1)
		#Check if p is prime		
		if isprime(p)==True:			#O(sqrt(size(p)))
			ep = p - 1
			status_ep = True
		else:
			#p is not prime, hence need to factorise p first & get "primes" and "powers" first. 
			
			result = euler_phi(p)			#when n is not prime 	Worst: O(sqrt(n)+8) Best: O(4) when n=1
								#when n is prime	#O(sqrt(n)+5) 
			#result = euler_phi(p, primes)				
			#return a, status
			ep = result[0]					#O(1)
			#status_ep = result[1]				#O(1)
			#print "euler_phi("+str(p)+") is: "+str(ep)		
			
	if status_ep == False:				#O(1)
		#ie p=1 or p is not prime
		print "status_ep is: "+str(status_ep)+", ep is: "+str(ep)
		sys.exit()					#O(1)
	else:						#O(1)
		#p is prime, ep = p-1		
		result1 = factorise(ep)				#Worst: O(sqrt(n))
		#return factors, c_factorisations
		factors = result1[0]			#O(1)
		c_factorisations = result1[1]		#O(1)

		print "factors of "+str(ep)+" are: "+str(factors)
		print "time for factorisation of "+str(ep)+" is: "+str(c_factorisations)
	
		result2 = calc_powers(factors)				#Worst: O(n+13)	#Best: O(18) 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(n))
		#return prime_factors, powers, c_calc_powers		
		prime_factors = result2[0]				#O(1)
		powers = result2[1]					#O(1)
		c_calc_powers = result2[2]				#O(1)
		total_calc_time = c_factorisations + c_calc_powers	#O(1)

		print "prime factors are: "+str(prime_factors)
		print "powers are: "+str(powers)
		#print "time for calc prime factors & powers is: "+str(c_calc_powers)
		print "total calc time for prime_factors and powers is: "+str(total_calc_time)
		
		status = True						#O(1)	
		power=1							#O(1)

		print "Now testing if "+str(g)+" is a primitive root mod "+str(p)+".."
		#testing if g is a primitive root mod p
		# first compute euler_phi(n) = ep = p-1
		# then determine prime factors of ep, say p_1, p_2, ... p_k
		# Now for every element m of Z_n*, compute pow(m,ep/p_i,n), for i=1,..,k
		# eg p = 109 => ep = 108. 108=2**5 * 3**1
		# m = 2 
		# 1st loop compute pow(2,108/2,109) = pow(2,54,109) = 108 = -1
		# 2nd loop compute pow(2,108/3,109) = pow(2,36,109) = 108 = 1
		# break since RHS = 1
		
		for prime in prime_factors:				#O(n)	#Worst: O(5*len(prime_factors))	#Best: O(6)
			#if status==True:					
			#print "================="
			#print "prime is: "+str(prime)
			if pow(g,ep / prime,p)==1:				#O(3) 	#Worst: O(5) #Best: O(3)
				print "pow("+str(g)+","+str(ep)+" / "+str(prime)+","+str(p)+") is 1"	
				status=False						#O(1)
				break							#O(1)

		#print "Status is: "+str(status)

		#raw_input("Waiting for user..")

		return status, prime_factors, powers
		#return status, prime_factors, powers, remainder

def euler_phi(n):
#def euler_phi(n, primes):				
	
	#when n is not prime
	# Worst: O(sqrt(n)+8)  
	# Best:	O(4) when n=1

	#when n is prime
	#O(sqrt(n)+5) 

	#euler_phi(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.	
	
	print "Running euler_phi("+str(n)+")..."
	
	#print "isprime_result is: "+str(isprime_result)

	#left_isprime_result=left()

	status = True 					#O(1)
	#floor_sqrt_n = math.floor(math.sqrt(n))

	#print "isprime(n) is: "+str(isprime(n)
	#print "isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#status=1 for not prime
	#status=0 for prime

	if n==1:					#O(1)	#subtotal O(3)
		a = 1					#O(1)
		status = False				#O(1)		
		return a, status			#O(1)

	elif isprime(n) == True:			#O(sqrt(n)+1) #subtotal O(sqrt(n)+3) 
	#elif isprime(n,floor_sqrt_n) == 0:
		a = n - 1				#O(1)
		return a, status			#O(1)
				
	else:							#subtotal O(???)
		#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.
		#euler_phi(p**k) = (p-1)*p**(k-1) for prime p 
		#euler_phi(m*n) = euler_phi(m)*euler_phi(n) for coprime m & n

		#euler_phi(n) = p_1**(k_1-1)*p_2**(k_2-1)*p_3**(k_3-1)... , where p_i are prime factors of n, and k_i are corresponding powers.
		#need primes & powers from factorise()!
				
		result1 = factorise(n)				#Worst: O(sqrt(size(n)))
		#return factors, c_factorisations
		factors = result1[0]			#O(1)
		c_factorisations = result1[1]		#O(1)

		print "factors of "+str(ep)+" are: "+str(factors)
		print "time for factorisation of "+str(ep)+" is: "+str(c_factorisations)
	
		result2 = calc_powers(factors)				#Worst: O(size(n)+13)	#Best: O(18) 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		#return prime_factors, powers, c_calc_powers		
		prime_factors = result2[0]				#O(1)
		powers = result2[1]					#O(1)
		c_calc_powers = result2[2]				#O(1)
		total_calc_time = c_factorisations + c_calc_powers	#O(1)

		print "prime factors are: "+str(prime_factors)
		print "powers are: "+str(powers)
		#print "time for calc prime factors & powers is: "+str(c_calc_powers)
		print "total calc time for prime_factors and powers is: "+str(total_calc_time)
		
		len_prime_factors = len(prime_factors)
		len_powers = len(powers)
		
		#check lengths of lists
		if len_prime_factors <> len_powers:
			print "length(prime_factors) <> length(powers)! Exiting.."			
			sys.exit() 

		#euler_phi(n) = p_1**(k_1-1)*p_2**(k_2-1)*p_3**(k_3-1)... , where p_i are prime factors of n, and k_i are corresponding powers.

		raw_input("Waiting for user...")		

		#for b in xrange(0,len_prime_factors):
		for prime in primes:
			print "============================"
			number = primes.index(prime)
			print "number is: "+str(prime)
			print "prime is: "+str(prime)
			if not a:			
				print "power is: "+str(power(number))
				a = prime **(power(number)-1)
				print "a is now: "+str(a)
			else:
				print "power is: "+str(power(number))
				a = a * prime **(power(number)-1)
				print "a is now: "+str(a)

		status = True						#O(1)	
		power=1							#O(1)

		#print str(n)+" is not prime!"		
		status = False				#O(1)
		return a, status			#O(1)				

def dlp(g, h, p, primefile, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_q_e_found, count_q_e_not_found, count_order_not_prime, count_calc_xi_no_solns, count_a_notprime):

	print "Running dlp().."

	floor_sqrt_p = int(math.floor(math.sqrt(p)))			#O(3)
	#print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	#count_a_notprime = 0						#O(1)
	result=ghp_checks(g, h, p, floor_sqrt_p, count_a_notprime) 	#Best case: O(sqrt(n)+5) 	Worst case: O(sqrt(n)+8)
	#return status, a
	#status=0 for problem and 1 for no problem
	#a=True for Prime, a=False for not prime
	
	status_ghp = result[0]
	status_isprime_a = result[1]
	#status_isprime_b = result[2]
	#q = result[3]
	n_prime=[]

	if status_isprime_a == False:					#O(1)
		count_a_notprime = count_a_notprime + 1				#O(1)
		sys.exit()							#O(1)
	elif status_ghp == 0:						#O(1)
		print "At least one of checks for g, h or p failed! Exiting.."		
		sys.exit()							#O(1)
	else:
		#store result of p and isprime(p) so later we do not need to run isprime(p) again				
		n_prime.append(p)
		#n_prime.append(q)
		#n_prime.append(True)

		#print "n_prime is: "+str(n_prime)
		
		#define prime list
		#print('Importing primes from csv file')
		primes=csvfile_store_primes(primefile)			#Assuming this is O(n+len(primes)+1)
		#print('First ten primes are: '+str(primes[0:10]))

		#check if sqrt_p > largest element in primes
		print('checking if square root of p > largest element in primes...')
		sqrt_p = math.sqrt(p)					#O(1)
		largest_prime = primes[-1]				#O(1 ???)
		count_needlargerprimelist=0				
		if sqrt_p > largest_prime:				#O(1)	#Subtotal: O(4)
			print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
			count_needlargerprimelist = count_needlargerprimelist + 1	#O(1)
			sys.exit()							#O(1)
		else:							#O(1)
			
			#define counts for different types of results	#O(7)
			count_nosolns=0
			count_x_equals_0=0
			count_normal_soln=0
			count_diffeq0=0
			#count_brute_force_soln=0
			count_q_e_found = 0
			count_q_e_not_found = 0
			count_calc_xi_no_solns = 0

			#define boolean values
			#brute_force_status = False

			#Check if g is a primitive root mod p
			count_primroot=0				#O(1)
			result=prim_root(g, p, n_prime)			#Worst case: O(???)		
			#return status, prime_factors, powers, remainder

			prim_root_status=result[0]			#O(1)
			prime_factors=result[1]				#O(1)
			powers=result[2]				#O(1)
			#remainder=result[3]				#O(1)

			if prim_root_status is False:
				print(str(g)+' is not a primitive root mod '+str(p)+'! Exiting ...') 		
				sys.exit()								#O(1)
			else:
				print(str(g)+' is a primitive root mod '+str(p))	
				count_primroot = count_primroot + 1			#O(1)

				#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

				#1st step: calculate p-1 from p
				p_minus_1 = p-1						#O(1)
				#print('p-1 is: '+str(p-1))	

				#2nd step: factorise p_minus_1 into product of prime powers
				#result=factorise_old(p_minus_1, primes)
				primes_list=prime_factors				#O(1)

				#print('primes for factorisation of p-1 are:'+str(prime_factors))
				#print('powers for factorisation of p-1 are:'+str(powers))

				print "primes_list is: "+str(primes_list)		
				print "powers are: "+str(powers)			

				#use exponent function to get order of g mod p
				result = exponent_g_n(g, 1, p)				#Worst: O(n + 7)	#Best: O(8)
				#return x, status
				order = result[0]					#O(1)
				status = result[1]					#O(1)

				#print "order is: "+str(order)
				#sqrt_order=math.floor(math.sqrt(order))

				# Now want order = q**e, where q is prime
				# obtain q and e 
				if order == 1:						#O(1)
					q = order						#O(1)
					e = 1							#O(1)
					#raw_input("Order is 1! Waiting for user..")
					print "order: "+str(order)
					count_order_not_prime = count_order_not_prime + 1	#O(1)
					count_q_e_found = count_q_e_found + 1			#O(1)
				elif order in n_prime:				
					print "order: "+str(order)+" is prime"
					q = order						#O(1)
					e = 1							#O(1)
					count_q_e_found = count_q_e_found + 1			#O(1)
					print "q: "+str(q)+", e: "+str(e)
				elif isprime(order) == True:				#O(sqrt(n))
				#elif isprime(order, sqrt_order)==0:
					#True for prime
					#False for not prime
					#order is prime
					print "order: "+str(order)+" is prime"
					q = order						#O(1)
					e = 1							#O(1)
					count_q_e_found = count_q_e_found + 1			#O(1)
					print "q: "+str(q)+", e: "+str(e)
				else:
					#order is not 1 nor prime		
					print "order: "+str(order)+" is not prime"		
					count_order_not_prime = count_order_not_prime + 1	#O(1)
					#now assume order = q**e, where q is prime, e>=1. Need to find q and e.
					result = calc_q_e(primes, order, p)			#Worst: O(n**2+7n+4)	#Best: O(12)
					#return q, e, result

					q=result[0]						#O(1)
					e=result[1]						#O(1)
					status=result[2]					#O(1)

					if status==False:						#O(1)
						print "q and e for order: "+str(order)+" not found!"
						count_q_e_not_found = count_q_e_not_found + 1			#O(1)
						sys.exit()							#O(1)
					else:
						print "q is: "+str(q)+", e is: "+str(e)
						#raw_input("Waiting for user")	

				#################################################
				# Prop_234 Algorithm
				
				result_prop_234 = prop_234(g, h, q, e, p)
				#return x, M, calc_xi_status

				#store results
				calc_xi_status = result_prop_234[2]					#O(1)
				x = result_prop_234[0]							#O(1)
				x_moduli = result_prop_234[1]						#O(1)
	
				if calc_xi_status == True:						#O(1)
					#Calc_xi method found solutions
					#x=[]									#O(1)
					#x_moduli=[]								#O(1)
					#x.append(result_prop_234[0])						#O(1)
					#print str(result_prop_234[0])+" appended to x"
					#x_moduli.append(result_prop_234[1])					#O(1)
					#print str(result_prop_234[1])+" appended to x_moduli"
					count_normal_soln = count_normal_soln + 1				#O(1)
				else:
					#Calc_xi method failed to find solutions - lhs=1 and rhs=1	
					print "Calc_xi method failed to find solutions - lhs=1 and rhs=1"
					count_calc_xi_no_solns = count_calc_xi_no_solns + 1
					sys.exit()

				#raw_input("Waiting for user..")

				print "============================"	
				print "x is: "+str(x)
				#print "type(x) is: "+str(type(x))
				print "x_moduli is: "+str(x_moduli)
				#print "type(x_moduli) is: "+str(type(x_moduli))
				#raw_input("Waiting for user..")
				
				if pow(g, x, p) <> h:			#O(2)
					print "CHECK FAILED - pow("+str(g)+", "+str(x)+", "+str(p)+") <> "+str(h) 
					print "g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x: "+str(x)+", x_moduli: "+str(x_moduli)
					answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))	#O(1)
					sys.exit()										#O(1)

			return x, count_nosolns, count_x_equals_0, count_normal_soln, x_moduli, count_diffeq0, count_order_not_prime, count_q_e_not_found, count_calc_xi_no_solns
			#return x, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, x_moduli, count_diffeq0

def calc_q_e(primes, k, p):
	print "Running calc_q_e(primes, "+str(k)+", "+str(p)+").."	

	#Worst: O(n**2+7n+4)	#Best: O(12)

	result=False			#O(1)
	q=0				#O(1)
	e=0				#O(1)
	n=1				#O(1)
	#print "p is: "+str(p)
	for prime in primes:		#O(n)	#Worst: O(n**2+7n)	#Best: O(8)
		#print "=================="
		n = 1					
		#print "n is: "+str(n)+", k is: "+str(k) 		
		#print "prime is: "+str(prime)+", p is: "+str(prime)
		while result is False and prime < p and n <= k and pow(prime,n) <= k:	#O(n)	#Worst: O(n+7)	#Best: O(7)
			#print "-----------------"
			#print "n is: "+str(n)+", k is: "+str(k) 
			#print "prime is: "+str(prime)+", p is: "+str(p)
			#a = pow(prime,n)
			#a = prime**n
			#print "prime ** n is: "+str(prime**n)
			#raw_input("Waiting for user..")
			if pow(prime,n) == k:							#O(2)
				q = prime						#O(1)
				e = n							#O(1)
				result = True						#O(1)
				#print "result is: "+str(result)				
				break							#O(1)
			else:
				n = n + 1						#O(1)
	return q, e, result

def exponent_g_n(generator,h_value, p):
	print "Running exponent_g_n("+str(generator)+","+str(h_value)+","+str(p)+").."

	#Worst: O(n + 7)	#Best: O(8)

	n=1						#O(1)
	x=0						#O(1)
	status=False					#O(1)
	while n < p:					#O(n)	#Worst: O(n + 7)
		#print "n is:"+str(n)
		if pow(generator,n,p) == h_value:		#O(2)	#Worst: O(6)
		#if generator**n % p == h_value:		#O(n+2)	#Worst: O(n+6)
			x = n				#O(1)
			status=True			#O(1)
			break				#O(1)
		n = n + 1				#O(1)

	if x==0:					#O(1)
		x="No exponent found"			#O(1)
		status=False				#O(1)

	return x, status

def prop_234(g, h, qi, ei, p):
	#print "-----------------------------------"
	print('Running prop_234 to solve for x...')

	#g[var], h[var], qi[var], ei[var], p
	#let x = x_0 +x_1*(q)+x_2*(q**2)+...+x_{e-1}q^(e-1), with 0 <= x_i < q, and determine successively x_0, x_1, x_2, ...

	print "qi is: "+str(qi)
	print "ei is: "+str(ei)

	# constuct list of q_powers from 0 to e-1
	q_powers=[]						#O(1)

	#when ei > 0: #worst: O(n+3)	#best: O(3)
	#when ei = 0: O(3)	
	#when ei not > 0 nor = 0: O(4)

	#first q_power will always be 1 (for k=0)
	if ei > 0:						#O(1)	#worst: O(n+3)	#best: O(1)
		for k in xrange(0,ei):					#O(n)
			q_powers.append(pow(qi,k))			#O(2)
	elif ei==0:						#O(1)	#worst: O(3)
		print "ei = 0!"					
		sys.exit()						#O(1)
	else:							#O(1)	#worst: O(4)
		print "ei is: "+str(ei)
		sys.exit()					#O(1)

	#print "q_powers are: "+str(q_powers)

	#now want to calculate xi using function	
	result = calc_xi(q_powers, g, h, qi, ei, p)
	#return xi, calc_xi_status	
	xi = result[0]
	calc_xi_status = result[1]

	#Subtotal - Worst: O(n**2 + 7n + 3), Best: O(3) when calc_xi_status == False
	if calc_xi_status == False:				#O(1)
		print "calc_xi_status is: False!"
		######Need another method for calculating the xi or x since calc_xi() method failed - lhs = rhs 
		######Try p-1/q method?? 
		######brute force search instead??
		x=0 						#O(1)
		M=0						#O(1)
		#raw_input("Calc_xi method failed (lhs=rhs=1). Waiting for user..")
	else:							#O(1)	#Subtotal - Worst: O(n**2 + 7n + 2), Best: O(n+5) when only 1 as q_power
		#print "xi are: "+str(xi)

		#print "---------------------------"
	
		#print "q_powers are: "+str(q_powers)	
		for q_power in q_powers: 			#O(n)	#Worst: O(n**2 + 7n)	#Best: O(n+4) - when only 1 as q_power
			#print "q_power is: "+str(q_power)
			#print "index of q_power is: "+str(q_powers.index(q_power))
			#print "xi[(q_powers.index(q_power))] is: "+str(xi[(q_powers.index(q_power))])		
			a=xi[q_powers.index(q_power)] 							#O(n+1)
			if q_power==1: 									#O(1)
				#print "Adding "+str(xi[q_powers.index(q_power)])+" to x"
				x = a										#O(1)
				#x = xi[q_powers.index(q_power)]
			
			else:										#O(1)
				#print "Adding "+str(xi[(q_powers.index(q_power))])+"*"+str(q_power)+" to x, and reducing mod "+str(qi**ei)
				x = (x + a * q_power) % pow(qi,ei)					#O(4)
				#x = (x + xi[q_powers.index(q_power)]*q_power) % (pow(qi,ei))	
			
		M = pow(qi,ei)					#O(1)
		#print("x is: "+str(x)+" mod "+str(M))		
	return x, M, calc_xi_status

def calc_xi(q_powers, g, h, qi, ei, p):
	print "---------------------------"			
	print "Running calc_xi()"				

	#initialise xi, cumul_q_powers, cumul_xi_q_powers
	xi = len(q_powers) * [0]				#O(len(q_powers))
	cumul_q_powers=[]					#O(1)
	cumul_xi_q_powers=[]					#O(1)
	calc_xi_status=True					#O(1)

	#Loop through each q_power until xi are calculated
	for q_power in q_powers:
		#print "q_power is: "+str(q_power)		
		if calc_xi_status == True:
			if q_power==1:							#total (incl top lev if) = 
				#solving for x_0		
				print("---------------------------")			
				print("Solving for xi[0] ..")				
				print("q_power is: "+str(q_power))					
					
				lhs= pow(g,pow(qi,ei-1),p)				#O(2)
				#lhs= (g**qi**(ei-1)) % p				
				print("lhs is: "+str(lhs)) 		# lhs=76	
					
				rhs= pow(h,pow(qi,ei-1),p)				#O(2)
				#rhs= (h**qi**(ei-1)) % p				
				print("rhs is: "+str(rhs)) 		# rhs=1		
			
				if lhs ==1 and rhs ==1:					#O(1)		#subtotal: O(2)	#section= O(2n+6)				
					#This method seems to fail for this instance. Try p-1/q method?? brute force search instead??				
					calc_xi_status=False				#O(1)

				else:							#O(1)		#Worst: O(4n+1)	#best: O(6)
					for t in xrange(0, qi):				#O(n)		#Worst: O(4n)	#best: O(5)
						if pow(lhs,t,p) == rhs:			#O(2)		#Worst: O(4)	#best: O(4)
						#if lhs**t % p ==rhs:					
							xi[0]=t  # xi[0]=		#O(1)
							print "xi[0] is: "+str(t)	
							break				

				if calc_xi_status == True:				#O(1)		#subtotal= O(3)
					cumul_xi_q_powers.append(xi[0])			#O(1)
					cumul_q_powers.append(1)			#O(1)
					#print "cumul_xi_q_powers after append: "+str(cumul_xi_q_powers)
					#print "cumul_q_powers after append: "+str(cumul_q_powers)
			else:								#O(1)		#total (incl top lev if) = 
				#solving for x_n (n!=0)
				print("---------------------------")			
				print "solving for x_n (n<>0).."			
				print("q_power is: "+str(q_power))			
				xi_number = q_powers.index(q_power)			#O(n)
				#print("Solving for xi["+str(xi_number)+"] ..")
				#print "cumul_xi_q_powers before append: "+str(cumul_xi_q_powers)
				#print "cumul_q_powers before append: "+str(cumul_q_powers)
			
				#print "g is: "+str(g) # g=
				#print "h is: "+str(h) # h=
				a = xi_number-1						#O(1)
				print("xi["+str(a)+"] is: "+str(xi[a])) # xi[0]=0	
			
				#print("qi is: "+str(qi))	#qi = 
				#print("ei is: "+str(ei))	#ei = 
			
				print "cumul_xi_q_powers is: "+str(cumul_xi_q_powers)	
				print "cumul_q_powers is: "+str(cumul_q_powers)		
			
				z=0
				for cumul_xi_q_power in cumul_xi_q_powers:		#O(n+1)
					z = z + cumul_xi_q_power
				
				print "sum_cumul_xi_q_power is now: "+str(z)		

				if xi[xi_number-1] >= 0:
					#need to work out what g**-[x_0+x_1*q_power+x_2*q_power**2 + ...], mod p is!!!
					#print("xi["+str(xi_number-1)+"] >= 0")
					print("Calculating modular inverse of "+str(g)+"**"+str(-z)+", mod "+str(p))			
					#print("Calculating modular inverse of "+str(g)+"**"+str(-xi[xi_number-1])+", mod "+str(p))				
					b = calc_modinverse(g, z, p)									#O(n+5)
					print("inverse is: "+str(b)) #b = 								
				
					#(ei - xi_number - 1)

					#print "(h * b)**qi**(ei - xi_number - 1) % p is: "+str((h * b)**qi**(ei - xi_number - 1) % p)
					rhs = pow(h * b,pow(qi,ei - xi_number - 1),p)
					#rhs = (h * b)**qi**(ei - xi_number - 1) % p						#O(2n+2)			

					print("rhs is: "+str(rhs))								

					if lhs == 1 and rhs == 1:									#O(1)	#Subtotal O(4)
						print "lhs == 1 and rhs == 1"								
						#print "xi["+str(xi_number-1)+"] >= 0, lhs=1, rhs=1, g: "+str(g)+" p: "+str(p)+" h: "+str(h)			
						#This method seems to fail for this instance. Brute force search instead??
						calc_xi_status=False									#O(1)
						raw_input("Waiting for user..")								#O(1)
					else:												#O(1)	#Subtotal O(n**2+5n+1)
						for t in xrange(0, qi):									#O(n)
							#print "t is now: "+str(t)					
							#print(str(lhs)+"**"+str(t)+" % "+str(p)+" is: "+str(lhs**t % p))
							if lhs**t % p == rhs:								#O(n+2)
								xi[xi_number]=t									#O(1)
								print "xi["+str(xi_number)+"] is: "+str(t)					
								break										#O(1)

					if calc_xi_status == True:									#O(1)	#Subtotal O(n**2+5n+1)
						cumul_xi_q_powers.append(q_power * xi[xi_number])						#O(3)
						#print("Appended "+str(q_power * xi_number)+" to cumul_xi_q_powers")
						cumul_q_powers.append(q_power)									#O(1)
						#print("Appended "+str(q_power)+" to cumul_q_powers")
						#print("xi["+str(xi_number)+"] is: "+str(xi[xi_number]))
						#print "xi are now:"+str(xi)
						#print "cumul_xi_q_powers after append: "+str(cumul_xi_q_powers)
						#print "cumul_q_powers after append: "+str(cumul_q_powers)
				else:													#O(1)
					print("xi["+str(xi_number-1)+"] is negative !!! CHECK")							
					raw_input("Waiting for user..")										#O(1)
					sys.exit()												#O(1)
		
				#print "lhs is: "+str(lhs)
				#print "rhs is: "+str(rhs)

				#print("rhs is: "+str(rhs))
				#print "qi is: "+str(qi)
	return xi, calc_xi_status

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

