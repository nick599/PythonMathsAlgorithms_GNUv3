#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 73. 28/01/2018.
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
print("Version 73. 28/01/2018.")
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

	x=result[0]						#O(1)
	M=result[7]						#O(1)
	
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
	#else:						#O(1)	#Worst case: O(8)
	#	#now check if p = 2q+1 where q is prime 		
	#	q = (p-1)/2											#O(1)
	#	b = isprime(q)											#O(1)
	#	if b == False:											#O(sqrt(n)+1)
	#		print str(q)+" is not prime. Hence "+str(g)+" is not a primitive root mod "+str(p)
	#		status=0												#O(1)
	#		sys.exit()												#O(1)
	
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
		result = euler_phi(p)				#when n is not prime 	Worst: O(sqrt(n)+8) Best: O(4) when n=1
								#when n is prime	#O(sqrt(n)+5) 
		#result = euler_phi(p, primes)				
		#return a, status
		ep = result[0]					#O(1)
		status_ep = result[1]				#O(1)
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
				
	else:							#subtotal O(3)
		print str(n)+" is not prime!"		
		status = False				#O(1)
		return a, status			#O(1)
		#sys.exit()				

#def dlp(g, h, p, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_q_e_found, count_q_e_not_found, count_order_not_prime, count_calc_xi_no_solns, count_a_notprime):

#def dlp(g, h, p, primefile, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_q_e_found, count_q_e_not_found, count_order_not_prime, count_calc_xi_no_solns, count_a_notprime):

def dlp(g, h, p, primefile, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_q_e_found, count_q_e_not_found, count_order_not_prime, count_calc_xi_no_solns, count_a_notprime):

	#count_order_not_prime 

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

			status=result[0]				#O(1)
			prime_factors=result[1]				#O(1)
			powers=result[2]				#O(1)
			#remainder=result[3]				#O(1)

			if status is False:
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

#def number_checks(number):
#
#	#Simple Checks for N:
#	#print('Running simple checks for number...')
#	if number==0:
#		print('Number entered is 0. Please choose another value for N')
#		sys.exit()
#	if number==1:
#		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
#		sys.exit()
#	if number<0:
#		print('Number entered is negative. Please enter another number')
#		sys.exit()

#def largest_divisor(n, primes_new, powers_new, mult_primes_powers):

	#div_values=[]
	#print('i is:'+str(i))
	#for i in xrange(0,len(primes)+1):	
		#print('i is:'+str(i))		
		#div_values.append(mult_primes_powers[i])
		#div_values.append(primes[i],powers[i], primes[i]**powers[i])
	
#	print "mult_primes_powers are: "/+str(mult_primes_powers)
#	l_div=max(mult_primes_powers)
#	print "Largest divisor (q**e) is: "+str(l_div)	
#	l_div_index=mult_primes_powers.index(l_div)
#	prime=primes_new[l_div_index]
	#print "Prime of largest divisor is: "+str(prime)
#	power=powers_new[l_div_index]
	#print "Power of largest divisor is: "+str(power)

	#max_div_value = max(div_values[2])
	#min_div_value = min(div_values[2])

	#if max_div_value==min_div_value:
	#	l_div=max_div_value
	#else:
				
		#continue

	#a="" #value to check
	#b=""
	#for j in xrange(0, len(div_values)+1):
	#	a = div_value[0]
	#	

#	return prime, power, l_div

#def order_element_modulo(a, p):
#	#m=0
#	#while N_remainder > 1 and not N_remainder % i:	
#	#	m += 1		
#	#	N_remainder //= i
#	
#	n=0
#	while (a**n) % p <> 1: 
#		n = n + 1
#	return n

		#qi_list[i] = primes_list[i]
		#qi_list[i] = primes_list(i)
		#Wi_list.append(p_minus_1 % (qi_list[i]**ei_list[i]))
		#Wi_list[i] = p_minus_1 % (qi_list[i]**ei_list[i]) 	
		#gi_list[i] = g**Wi_list[i]
		#hi_list[i] = h**Wi_list[i]
		#zi_list[i] = hi_list[i] % p
		
		#print('qi is:'+str(qi_list[i]))
		#print('ei is:'+str(ei_list[i]))
		#print('Wi is:'+str(Wi_list[i]))
		#print('gi is:'+str(gi_list[i]))
		#print('hi is:'+str(hi_list[i]))
		#print('zi is:'+str(zi_list[i]))
		#print('Vi is:'+str(Vi_list[i]))

#Now zi_list[i] * yi_list[i] congruent to Vi mod p, where zi, Vi, p are known and yi are unknown

#8: Take first congruence; x = qi * t + yi for some t unknown.
	#k = 0
	#for C in C_tuples:
	#	print('congruence '+str(k)+' is: x = '+str(qi_list[k])+'* t + '+str(yi_list[k]))
		
	#9: Substitute first congruence in all other congruences.
	#Now 	q1 * t + y1 = y2 mod q2
	#...................................
	#	q1 * t + y1 = yC mod qC
	# where t are unknown.

	#q_to_e=result[2]
	#print "q_to_e is: "+str(q_to_e)

	# largest divisor = q**e
	# Does order = q**e? or does order = e ???


#Use Euclids algorithm forward & reverse to find inverses where required
	
	#euclid_f=[]
	#euclid_r=[]
	#yi=[]
	#j = 0
	#for C in C_tuples:	
	#	euclid_f=euclid_forward(zi_list[j],Vi_list[j],p)
	#	euclid_r=euclid_reverse(euclid_f[0],euclid_f[1],p)
	#	yi[j]=euclid_r[0]	
	#	j = j + 1

	#Now x = yi mod qi for each record

#=================================

#evaluate x_i for qi and ei:
	#for q_power in q_powers:
	#	#print("q_power is: "+str(q_power))
	#	if q_power==1:
	#		#solving for x_0
	#		print("---------------------------")
	#		print("q_power is: "+str(q_power))
	#		print("Solving for xi[0] ..")
	#		#need to solve (g**q**(e-1))*x_0 = h**q**(e-1), mod q**(e-1)
	#		#eg g=3, h=5, p=101. Hence (3**5**1)*x_0 = 101**5**1, mod 5**1 
	#		print("qi is: "+str(qi)) #qi = 5
	#		print("ei is: "+str(ei)) #ei = 2
	#		moduli = p		
	#		print("moduli is: "+str(moduli))
	#		lhs= (g**qi**(ei-1)) % p
	#		print "g is: "+str(g) 			# g=81
	#		print "h is: "+str(h) 			# h=9
	#		print("lhs is: "+str(lhs)) 		# lhs=1
	#		rhs= (h**qi**(ei-1)) % p
	#		print("rhs is: "+str(rhs)) 		# rhs=4
	#		for t in xrange(0, qi):
	#			if lhs**t % p ==rhs:
	#				xi[0]=t  # xi[0]=0
	#				break

	#		print "xi are:"+str(xi)
	#		if not xi[0]:
	#			print("xi[1] not found!!!")
	#			sys.exit()
	#		print("xi[0] is: "+str(xi[0]))
			#print("---------------------------")
	#	elif q_power==qi:
			#solving for x_1
	#		print("---------------------------")
	#		print("q_power is: "+str(q_power))
	#		print("Solving for xi[1] ..")
			#need to solve (g**q**(e-1))*x_1 = (h*(g**[-x_0]))**q**(e-2), mod q**(e-1)
			#eg g=3, h=5, p=101. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
	#		print "g is: "+str(g) # g=81
	#		print "h is: "+str(h) # h=19
	#		print("xi[0] is: "+str(xi[0])) # xi[0]=0
			
	#		print("qi is: "+str(qi))	#qi = 5
	#		print("ei is: "+str(ei))	#ei = 2
			#moduli = p			
	#		print("moduli is: "+str(p))
			
			#b=-x_0
	#		if xi[0] > 0:
				#need to work out what g**[-x_0], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
	#			print("xi[0] > 0")
	#			print("Calculating modular inverse of "+str(g)+"**"+str(-xi[0])+", mod "+str(p))				
	#			b = calc_modinverse(g, xi[0], p) #b = 5
				#print("inverse is: "+str(b)) #b = 5
	#			rhs = (h * b)**qi**(ei-2) % p #rhs = (19 * 5) % 101 = 95 % 101				
				#print("rhs is: "+str(rhs))
	#		elif xi[0]==0:
				#g**[x_0]=g**0=1, mod p
				#Hence h*(g**[-x_0]) = h, mod p
	#			print("xi[0] = 0")
				#rhs= (h*g**(-x_0))**qi**(e-2)% p
				#Thus rhs = (h)**qi**(e-2) % p
	#			print("h**qi**(ei-2) % p is: "+str(h**qi**(ei-2)))
	#			rhs = (h**qi**(ei-2)) % p
	#			print("rhs is: "+str(rhs))	
	#		else:
	#			print("xi[0] is negative !!! CHECK")				
	#			sys.exit()			
	#		print "lhs is: "+str(lhs)
	#		print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
	#		print "qi is: "+str(qi)
	#		for t in xrange(0, qi):
	#			print "t is now: "+str(t)					
	#			print(str(lhs)+"**"+str(t)+" % "+str(p)+" is: "+str(lhs**t % p))
	#			if lhs**t % p ==rhs:
	#				xi[1]=t
					#print "xi[1] is: "+str(t)					
	#				break
	#		if not xi[1]:
	#			print("xi[1] not found!!!")
	#			sys.exit()
	#		print("xi[1] is: "+str(xi[0]))
	#	elif q_power==qi**2:
			#solving for x_2 
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for xi[2] ..")
			#need to solve (g**q**(e-1))*x_2 = (h*(g**[-x_0-x_1*q]))**q**(e-3), mod p
			#eg g=3, h=5, p=113. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
	#		print "g is: "+str(g) # g=81
	#		print "h is: "+str(h) # h=19
	#		print("xi[0] is: "+str(xi[0])) # xi[0]=1		
	#		print("xi[1] is: "+str(xi[1])) # xi[1]=1			
	#		print("qi is: "+str(qi))	#qi = 2
	#		print("ei is: "+str(ei))	#ei = 4			
	#		print("moduli is: "+str(p))	#moduli = 113
			
			#b=-x_0
	#		if xi[0]+xi[1]*qi > 0:
				#need to work out what g**[-x_0], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
	#			print("xi[0]+xi[1]*qi > 0")
	#			print("Calculating modular inverse of "+str(g)+"**"+str(-(xi[0]+xi[1]*qi))+", mod "+str(p))				
	#			b = calc_modinverse(g, xi[0]+xi[1]*qi, p) #b = 35
				#print("b is: "+str(b)) #b = 65
	#			rhs = (h * b)**qi**(ei-3) % p #rhs = (40 * 35) % 113 = 18 % 113				
				#rhs = (h * b)**qi**(ei-3)
				#print("rhs is: "+str(rhs))

	#		elif xi[0]+xi[1]*qi ==0:
				#g**[x_0]=g**0=1, mod p
				#Hence h*(g**[-x_0]) = h, mod p
	#			print("xi[0]+xi[1]*qi = 0")
				#rhs= (h*g**(-x_0))**qi**(e-2)% p
				#Thus rhs = (h)**qi**(e-2) % p
	#			print("h**qi**(ei-3) % p is: "+str(h**qi**(ei-3)))
	#			rhs = (h**qi**(ei-3)) % p
	#			print("rhs is: "+str(rhs))	
	#		else:
	#			print("xi[0]+xi[1]*qi is negative !!! CHECK")				
	#			sys.exit()			
	#		print "lhs is: "+str(lhs)
	#		print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
	#		for t in xrange(0, qi):
				#print "t is now: "+str(t)					
	#			if lhs**t % p ==rhs:
	#				xi[2]=t
	#				print "xi[2] is: "+str(t)					
	#				break
	#	elif q_power==qi**3:
			#solving for x_3
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for x_3 ..")

			#need to solve (g**q**(e-1))*x_2 = (h*(g**[-x_0-x_1*q]))**q**(e-3), mod p
			#eg g=3, h=5, p=113. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
	#		print "g is: "+str(g) # g=81
	#		print "h is: "+str(h) # h=19
	#		print("xi[0] is: "+str(xi[0])) # xi[0]=1		
	#		print("xi[1] is: "+str(xi[1])) # xi[1]=1			
	#		print("xi[2] is: "+str(xi[1])) # xi[2]=1			
	#		print("qi is: "+str(qi))	#qi = 2
	#		print("ei is: "+str(ei))	#ei = 4			
	#		print("moduli is: "+str(p))	#moduli = 113
			
			#b=-x_0
	#		if xi[0]+xi[1]*qi+xi[2]*qi**2 > 0:
				#need to work out what g**[-x_0], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
	#			print("xi[0]+xi[1]*qi+xi[2]*qi**2 > 0")
	#			print("Calculating modular inverse of "+str(g)+"**"+str(-(xi[0]+xi[1]*qi+xi[2]*qi**2))+", mod "+str(p))				
	#			b = calc_modinverse(g, xi[0]+xi[1]*qi+xi[2]*qi**2, p) #b = 35
				#print("b is: "+str(b)) #b = 65
	#			rhs = (h * b)**qi**(ei-4) % p #rhs = (40 * 35) % 113 = 18 % 113				
				#rhs = (h * b)**qi**(ei-4)
				#print("rhs is: "+str(rhs))

	#		elif xi[0]+xi[1]*qi+xi[2]*qi**2 ==0:
				#g**[x_0]=g**0=1, mod p
				#Hence h*(g**[-x_0]) = h, mod p
				#rhs= (h*g**(-x_0))**qi**(e-2)% p
				#Thus rhs = (h)**qi**(e-2) % p
	#			print("h**qi**(ei-4) % p is: "+str(h**qi**(ei-4)))
	#			rhs = (h**qi**(ei-4)) % p
	#			print("rhs is: "+str(rhs))	
	#		else:
	#			print("xi[0]+xi[1]*qi+xi[2]*qi**2 is negative !!! CHECK")				
	#			sys.exit()			
	#		print "lhs is: "+str(lhs)
	#		print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
	#		for t in xrange(0, qi):
				#print "t is now: "+str(t)					
	#			if lhs**t % p ==rhs:
	#				xi[3]=t
	#				print "xi[3] is: "+str(t)					
	#				break
	#	elif q_power==qi**4:
	#		#solving for x_4
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for x_4 ..")
	#	else:
			#solving for x_n .. ??
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for x_n ??..")
	#raw_input('Waiting for user..')


# Now need to contruct formulae for x = x_{0} +x_{1}*(q)+x_{2}*(q**2)+...+x_{e-1}q^(e-1)
	#print "e - 1 is: "+str(e-1)
	#for  in xrange(0, e+1): 
		#1st loop: x= x_0
		#2nd loop: x= x_0 + x_1(q)
		#3rd loop: x= x_0 + x_1(q) + x_2(q**2)
	#	x = j

	#initialise x
	#x=0	

#def a_exp_x_eq_1(a,p):
#	x=1
#	x_values=[]
#	count=0
#	while count < 3:
#		#print "count is: "+str(count)		
#		if a**x % p ==1:
#			#print "a**x % p is: "+str(a)
#			x_values.append(x)
#			#print str(x)+" appended to x_values"
#			count=count+1
#			if count==2:
#				#x_values.append(x)
#				#print str(x)+" appended to x_values
#				diff = x_values[1] - x_values[0]				
#				#diff = answer2 - answer1
#				#print "diff is: "+str(diff)
#				break
#		x = x + 1
#	return diff

#def prim_root_old(g,p):
#
#	print('Checking if '+str(g)+' is a primitive root mod '+str(p)+' ..')
#	status=True
#	F_p_star=[]	
#	for j in xrange(0,p-1): #eg for p=9: 0,1,2,3, .. ,7  
#		#F_p_star[j]=(g**j)%p	
#		if ((g**j)%p in F_p_star) and j<>0:
#			status=False
#			break
#		else:
#			F_p_star.append((g**j)%p)
#	return status

#print("======================================")

	#floor_sqrt_p = int(math.floor(math.sqrt(p)))
	#print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	#result=ghp_checks(g,h,p,floor_sqrt_p)
	#count_notprime = 0
	#result=ghp_checks(g, h, p, floor_sqrt_p, count_notprime) 

	#if result == 0:
	#	sys.exit()

	#define prime list
	#print('Importing primes from csv file')
	#primes=csvfile_store_primes(primefile)
	#print('First ten primes are: '+str(primes[0:10]))

	#check if sqrt_p > largest element in primes
	#print('checking if square root of p > largest element in primes...')
	#sqrt_p = math.sqrt(p)
	#largest_prime = primes[-1]
	#count_needlargerprimelist=0
	#if sqrt_p > largest_prime:
	#	print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
	#	count_needlargerprimelist = count_needlargerprimelist + 1
	#	sys.exit()

	#Check if g is a primitive root mod p
	#count_primroot=0
	#result=prim_root(g,p,primes)
	#status=result[0]
	#prime_factors=result[1]
	#powers=result[2]
	#moduli=result[3]

	#if result is False:
	#	print(str(g)+' is not a primitive root mod '+str(p)+'! Exiting ...')		
	#	sys.exit()
	#else:
		#print(str(g)+' is a primitive root mod '+str(p))	
	#	count_primroot = count_primroot + 1

#def a_exp_x_eq_r_old(a,p,r):
#	x=1
#	x_values=[]
#	count=0
#	while count < 3:
#		#print "count is: "+str(count)		
#		if a**x % p == r:
#			#print "a**x % p is: "+str(r)
#			x_values.append(x)
#			#print str(x)+" appended to x_values"
#			count=count+1
#			if count==2:
#				#x_values.append(x)
#				#print str(x)+" appended to x_values
#				diff = x_values[1] - x_values[0]				
#				#diff = answer2 - answer1
#				#print "diff is: "+str(diff)
#				break
#		x = x + 1
#	return diff

#def polig_helman(primes_list, g, h, p, count_nosolns, count_zi_bi_equal_1, count_diffeq0, count_x_equals_0, count_bi_equal_1_zi_ntequal_0_1):
#
#	print "Running polig-helman alg.."	
#
#	#3: Calculate C - number of unique primes in factorisation (also is number of congruences to solve)
#	C=0
#	for prime in primes_list:
#		C = C + 1		
#	#print('Number of primes in primes_list = C = '+str(C))
#
#	#4: Need to create a list (with C elements) for each of: q_i, e_i, W, g_i, h_i, z_i, & V_i 
#	C_list=list(xrange(1,C+1))
#	#print('C_list is: '+str(C_list))
#
#	#5: initialise lists
#	qi=[]
#	ei=[]
#	Wi=[]
#	gi=[]
#	hi=[]
#	zi=[]
#	Bi=[]
#	#Vi=[]
#
#	#6: loop through each C calculating values & storing them
#	x=[] 
#	x_moduli=[]
#	i = 0
#	for C in C_list:
#		#print('========================')
#		#print('current C is:'+str(C))
#		#print('i is: '+str(i))
#		qi.append(primes_list[i])
#		#print('qi['+str(i)+'] is: '+str(qi[i]))
#		ei.append(powers[i])
#		#print('ei['+str(i)+'] is: '+str(ei[i]))
#		Wi.append(p_minus_1 / (qi[i]**ei[i]))		
#		
#		gi.append(g**Wi[i])
#		#print('gi['+str(i)+'] is: '+str(gi[i]))
#		Bi.append(gi[i] % p)
#		#print('Bi['+str(i)+'] = gi['+str(i)+'] % p is: '+str(Bi[i]))
#		
#		hi.append(h**Wi[i])
#		#print('hi['+str(i)+'] is: '+str(hi[i]))
#		zi.append(hi[i] % p)
#		#print('zi['+str(i)+'] = hi['+str(i)+'] % p is: '+str(zi[i]))
#	
#		#7: Now Bi[i]**x = zi[i] mod p for each i
#		# Need to solve for x for each.
#		#x=[] 
#		#x_moduli=[]
#		
#		#print('i is: '+str(i))
#		#print('qi['+str(i)+'] is: '+str(qi[i]))
#		#print('ei['+str(i)+'] is: '+str(ei[i]))
#			
#		#print('Solving for x...')
#		if Bi[i]==0 and zi[i]==1:
#			print 'No Solutions!!!'
#			count_nosolns = count_nosolns + 1
#			sys.exit()
#		elif Bi[i]==0 and zi[i]==0:
#			print 'No Solutions!!!'
#			count_nosolns = count_nosolns + 1
#			sys.exit()
#		elif Bi[i]==1 and zi[i]==0:
#			print 'No Solutions!!!'
#			count_nosolns = count_nosolns + 1
#			sys.exit()
#		elif Bi[i]==1 and zi[i]==1:
#			x.append(0)			
#			#print "0 appended to x"
#			x_moduli.append(1)
#			#print "1 appended to x_moduli"
#			count_zi_bi_equal_1 = count_zi_bi_equal_1 + 1
#		elif Bi[i]==1:
#			x.append(0)			
#			#print "0 appended to x"
#			diff = a_exp_x_eq_r(1,p,zi[i])			
#			if diff==0:
#				#print('i is: '+str(i))
#				#print('qi['+str(i)+'] is: '+str(qi[i]))
#				#print('ei['+str(i)+'] is: '+str(ei[i]))
#				#print "Bi[i] is: "+str(Bi[i])
#				#print "zi[i] is: "+str(zi[i])
#				print 'Diff = 0 - No Solutions!!!'
#				count_diffeq0 = count_diffeq0 + 1
#				count_nosolns = count_nosolns + 1
#				sys.exit()
#			else:			
#				x_moduli.append(diff)
#				#print str(diff)+" appended to x_moduli"
#				count_bi_equal_1_zi_ntequal_0_1 = count_bi_equal_1_zi_ntequal_0_1 + 1
#		elif Bi[i]<>0 and zi[i]==1:
#			#print "Bi[i] is: "+str(Bi[i])
#			#print "zi[i] is: "+str(zi[i])
#			x.append(0)			
#			#print "0 appended to x"
#			diff = a_exp_x_eq_r(Bi[i],p,1)			
#			if diff==0:
#				#print('i is: '+str(i))
#				#print('qi['+str(i)+'] is: '+str(qi[i]))
#				#print('ei['+str(i)+'] is: '+str(ei[i]))
#				#print "Bi[i] is: "+str(Bi[i])
#				#print "zi[i] is: "+str(zi[i])
#				print 'Diff = 0 - No Solutions!!!'
#				count_diffeq0 = count_diffeq0 + 1
#				count_nosolns = count_nosolns + 1
#				sys.exit()
#			else:		
#				x_moduli.append(diff)			
#				#print str(diff)+" appended to x_moduli"
#				count_x_equals_0=count_x_equals_0 + 1
#		elif Bi[i] == zi[i]:
#			#print "Bi[i] is: "+str(Bi[i])
#			#print "zi[i] is: "+str(zi[i])
#			x.append(1)
#			#print "1 appended to x"	
#			#print str(1)+" appended to x"		
#			diff = a_exp_x_eq_r(Bi[i],p, zi[i])
#			if diff==0:
#				#print('i is: '+str(i))
#				#print('qi['+str(i)+'] is: '+str(qi[i]))
#				#print('ei['+str(i)+'] is: '+str(ei[i]))
#				#print "Bi[i] is: "+str(Bi[i])
#				#print "zi[i] is: "+str(zi[i])
#				print 'Diff = 0 - No Solutions!!!'
#				count_diffeq0 = count_diffeq0 + 1
#				count_nosolns = count_nosolns + 1
#				sys.exit()
#			else:
#				x_moduli.append(diff)
#				#print str(diff)+" appended to x_moduli"			
#				count_Bi_equals_zi=count_Bi_equals_zi + 1
#		else:
#			print('Checks done and trivial solutions not found.') 
#			raw_input("Waiting for user..")	
#
#		i = i + 1
#
#	return x_final, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, x_moduli_final, count_diffeq0

#def chinese_remainder(x, x_moduli):
#	print "Running chinese remainder.."	
#	#print "x are: "+str(x)
#	#print "x_moduli are: "+str(x_moduli)
#	#cong=[]
#	cong_x=[]
#	cong_moduli=[]
#	for number in xrange(0,len(x)):
#		#print('--------------------')
#		#print "number is: "+str(number)		
#		#store values in 1st congruence	
#		a= x[number]
#		b= x_moduli[number]
#		if b<>1:		
#			if not cong_x:
#				#cong has no elements
#				#Add values in first congruence			
#				#print "Appending info from 1st congruence"
#				cong_x.append(a)
#				x_new = a		
#				cong_moduli.append(b)
#				M = b			
#				#cong.append(1)
#			else:
#				print('--------------------')
#				#cong_x has elements
#				print "Working on congruence number: "+str(number+1)
#				#print "cong_x["+str(number-1)+"] is: "+str(cong_x[number-1])
#				#print "cong_moduli["+str(number-1)+"] is: "+str(cong_moduli[number-1])
#				#Subtract current cong_x[number-1] from current x[number]
#				#print "Subtracting cong_x["+str(number-1)+"] from current x["+str(number)+"].."
#				c = x[number] - cong_x[-1]
#				#c = x[number] - cong_x[number-1]
#				print "c now is: "+str(c)				#c=
#			
#				#print "cong_moduli["+str(number-1)+"] to use in inverse is: "+str(cong_moduli[number-1]) 
#				#number=
#				#print "x_moduli[number] to use in inverse is: "+str(b)			#moduli=
#
#				#now want to find (cong_moduli[number-1]**-1) mod(b)		
#				f = calc_modinverse(cong_moduli[-1], 1, b)
#				#f = calc_modinverse(cong_moduli[number-1], 1, b)
#				print "inverse (f) is: "+str(f) 			#inverse=
#
#				#now take c and times it by the inverse, f, and reduce mod b
#				print "c*f is: "+str(c*f)
#				print "b is: "+str(b)
#				k = (c*f) % b			
#				print "k is: "+str(k)
#
#				#now take value of k and use it to work out new value of x
#				print "cong_x[-1] is: "+str(cong_x[-1])
#				#print "cong_x[number-1] is: "+str(cong_x[number-1])
#				print "cong_moduli[-1] * k is: "+str((cong_moduli[-1] * k))
#				#print "cong_moduli[number-1] * k is: "+str((cong_moduli[number-1] * k))
#				x_new = cong_x[number-1] + (cong_moduli[number-1] * k)
#				#x_new = cong_x[-1] + (cong_moduli[-1] * k)
#				print "x_new is: "+str(x_new)
#				cong_x.append(x_new)
#			
#				#now work out value of M
#				M = cong_moduli[-1] * b
#				#M = cong_moduli[number-1] * b
#				print "M is now: "+str(M)
#				cong_moduli.append(M)
#	return x_new, M


#for C in C_list:
				#	print "============================"			
				#	i = C_list.index(C)
				#	print "i is: "+str(i)
				##	print "g is: "+str(g)
				#	print "h is: "+str(h)
				#	print "primes_list[i] is: "+str(primes_list[i])
				#	print "powers[i] is: "+str(powers[i])
				#	print "p is: "+str(p)
				#	result_prop_234 = prop_234(g, h, primes_list[i], powers[i], p)

					#result_prop_234 = prop_234(g, h, qi[i], ei[i], p)
					#result_prop_234 = prop_234(Bi[i], zi[i], qi[i], ei[i], p)
					#return x, M, calc_xi_status

				#	calc_xi_status = result_prop_234[2]
				#
				#	if calc_xi_status == True:
				#		#Calc_xi method found solutions	#				
		#				x.append(result_prop_234[0])
				#		#print str(result_prop_234[0])+" appended to x"
				#		x_moduli.append(result_prop_234[1])
						#print str(result_prop_234[1])+" appended to x_moduli"
				#		count_normal_soln = count_normal_soln + 1
				#	else:
						#Calc_xi method failed to find solutions - lhs=1 and rhs=1	
				#		print "Calc_xi method failed to find solutions - lhs=1 and rhs=1"
				#		sys.exit()


#def isprime_old(p,floor_sqrt_p):			#O(sqrt(n)+1)
#	#print('p is: '+str(p))	
#	#status=0 for prime
#	status=0
#	if p % 2 == 0:					#O(1)
#		#status=1 for not prime
#		status=1
#	
#	n = 3
#	while n <= floor_sqrt_p: 			#O(n+1)
#		if p % n == 0:
#			#status=1 for not prime
#			status=1
#			break 
#		else:
#			#status=1 for not prime
#			status=0
#		n = n + 2
#	#print('status is: '+str(status))	
#	#status=0 for prime
#	#status=1 for not prime
#	return status

#result=check_answer(g,h,p,x)			#O(4)
	#if result==False:
	#	#status=False
	#	print "CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x: "+str(x)+", M: "+str(M)
	#else:
	#	print("======================================")
	#	print "Final solution: x= "+str(x)+" mod "+str(M)
	#
	#print("======================================")

#def check_answer(g, h, p, x):				### Section O(4) ###
#	#def check_answer(g, h, p, x, answers_to_be_checked):
#	status=True	
#	if pow(g,x,p) <> h:				#O(2)	#Subtotal O(3)
#	#if g**x % p <> h:				#O(n+2)	#Subtotal O(n+3) 
#		#print "CHECK ANSWER!!!"
#		#answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))
#		status=False
#		
#	return status


#result = factorise_old(ep, primes)			#Worst: O(n**2 + 8n + 21)	#Best: O(27 ???) - assuming there are elements in "list"
		#return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem

		#prime_factors = result[0]				#O(1)
		#powers=result[1]					#O(1)
		#remainder=result[2]					#O(1)

		#print "prime_factors are: "+str(prime_factors)
		#print "powers are: "+str(prime_factors)

#for prime in prime_factors:				#O(n)	#Worst: O(len(prime_factors)*[3n + 4])	#Best: O(len(prime_factors) * 8)
		#	if status==True:					#O(1)	#Worst: O(3n + 4)	#Best: O(8)
		#		print "================="
		#		print "prime is: "+str(prime)
		#		power = 1						#O(1)
		#		power_index = 0						#O(1)
		#		print "power_index is: "+str(power_index)
		#		while power < powers[power_index]:			#O(n)	#Worst: O(3n + 1) #Best: O(3)
		#			print "------------------"
		#			print "power is: "+str(power)			
		#			if pow(g,ep / powers[power_index],power) == 1:		#O(3) 	#Worst: O(3) #Best: O(3)	
		#				print "pow(g,ep / powers[power_index],power) is 1"						
		#				status=False						#O(1)
		#				#print "Status is False!"				
		#				break							#O(1)
		#			power = power + 1					#O(1)
		#		power_index = power_index + 1				#O(1)

		#print "Status is: "+str(status)	

#def max_element_below_or_equal_target(List,target):
#	if target in List:
#		return List.index(target)
#	elif target > List[-1]:
#		#Target value is not in list. Return index of last number in list.
#		return List.index(List[-1])
#	elif target < List[-1]:
#		#Target value is less than largest number in list
#		# start from 2 and increase until last number is found that is less than target.
#		i=0
#		while List[i] < target:
#			i = i + 1 
#		return i
#	else:
#		print 'List[-1] is: '+str(List[-1])
#		print 'target is: '+str(target)	
#		print "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))
#		sys.exit()
#		#return "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))

#def factorise_old(N,list):		
#	print("Running factorise()...")
	
#	#Worst: O(n**2+8n+21)	#Best: O(27 ???) - assuming there are elements in "list"

#	#Create lists to hold prime factors of N, corresponding powers and any remainder
#	s_before_lists = time.clock()			#O(1)
#	prime_factors = []				#O(1 ???)
#	powers = []					#O(1 ???)
#	remainder=()					#O(1 ???)

#	c_lists = time.clock() - s_before_lists		#O(1)

	#initialise N_remainder
#	N_remainder = long(N)				#O(1)
#	i=2	

	#call calc_primes_powers_remainder
	#print('Calculating prime factors, powers and initial remainder...')
#	s_before_factorisations = time.clock()		#O(1)
#	result2=calc_primes_powers_remainder(list,N_remainder)		#Worst: O(n**2 + 12n + 20)	#Best: O(13 ???) - assuming there are elements in "list" 
#
#	c_factorisations = time.clock() - s_before_factorisations	#O(1)

#	prime_factors=result2[0] 					#O(1)
#	powers=result2[1]						#O(1)
#	remainder=result2[2]						#O(1)
#	c_pps=result2[3]						#O(1)
#	c_nrem=result2[4]						#O(1)
	#mult_primes_powers=result2[5]					

#	return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem, mult_primes_powers

#def calc_primes_powers_remainder_old(list, N_remainder):

	#Worst: O(n**2 + 12n + xxxx)	#Best: O( ???) - Assuming elements in "list"

	#O(4)

#	prime_factors=[]			#O(1 ???)
#	powers=[]				#O(1 ???)
	#mult_primes_powers=[]			
#	remainder=()				#O(1 ???)

	#==================================================================================
	#Worst: O(n**2 + 12n + 2)	#Best: O(7 ???) - Assuming elements in "list"
	#	
	#Check if there are elements in prime list
#	s_primefactors_powers = time.clock()	#O(1)
#	if not list:				#O(1 ???)		#Subtotal: O(3)
		#There are no elements in isliced_primes list		
#		print("There are no elements in isliced_primes list??")		
#		N_remainder=[]				#O(1 ???)
		#remainder=[]
		
#	else:					#O(1)		#Worst: O(n**2 + 12n + 1)	#Best: O(6)
		#There are elements in primes list
		# N_remainder is not in isliced_primes:
#		for prime in list:					#O(n)	#Worst: O(n**2 + 12n) #Best: O(5)
			#print("prime is now: "+str(prime))			
#			prime_int=int(prime)					#O(1)
			#print "type(N_remainder) is: "+str(type(N_remainder))
			#print "type(prime_int) is: "+str(type(prime_int))
			
#			if N_remainder <> 1:					#O(1)	#Subtotal: O(n+11)
			#while N_remainder <> 1: 
#				if N_remainder % prime_int == 0:		#O(1)	
					#prime is a factor				#Subtotal: O(n+9)
					#prime^m divides N_remainder, m integer
#					m = MaxPower(prime_int,N_remainder)		#O(n+3)
#					prime_factors.append(prime_int)			#O(1)
#					powers.append(m)				#O(1)
					#mult_primes_powers.append(pow(prime_int,m))	
#					N_remainder = N_remainder/(pow(prime_int,m))	#O(2)
					#break
				#else:
					#break
#			else:
#				break
	#==================================================================================

#	c_primefactors_powers = time.clock() - s_primefactors_powers		#O(1)
	
	#==================================================================================
	#Check if there are elements in N_remainder list
#	s_nremainder = time.clock()						#O(1)
#	if not N_remainder:							#O(1)
		#There are no elements in N_remainder list		
#		N_remainder=()								#O(1)
#	else:
		#There are elements in N_remainder list

		#check if N_remainder is also a prime
#		if N_remainder > long(list[-1]) and math.sqrt(N_remainder) <= list[-1]: 	#O(6)
			#N_remainder is prime since its square root is less than largest prime in prime list file, and all those primes have been checked earlier.			
			#print('Appending last prime factor and power..')				
#			prime_factors.append(N_remainder)						#O(1)
#			powers.append(1)								#O(1)
			#mult_primes_powers.append(N_remainder)						
#			N_remainder=()									#O(1)
#		elif N_remainder > long(list[-1]) and math.sqrt(N_remainder) > list[-1]:	#O(6)
			#print('Appending remainder..')
#			remainder=(N_remainder)								#O(1)
#			print('There is a remainder of: '+str(N_remainder))
#		elif N_remainder <> 1:								#O(1)
#			print('There is a remainder of: '+str(N_remainder))

#	c_nremainder = time.clock() - s_nremainder				#O(1)
	
	#Now set N_remainder to ''
#	N_remainder=()								#O(1)
		
	#Return factors of N using factors() list
#	return prime_factors, powers, remainder, c_primefactors_powers, c_nremainder
	#return prime_factors, powers, remainder, c_primefactors_powers, c_nremainder, mult_primes_powers

#def a_exp_x_eq_r(a,p,r):
	#print("Running a_exp_x_eq_r()..")
#	x=1
#	x_values=[]
#	count=0
#	diff=0
#	for x in xrange(0,p):
		#print "count is: "+str(count)		
#		if pow(a,x,p) == r:
		#if a**x % p == r:
			#print "a**x % p is: "+str(r)
#			x_values.append(x)
			#print str(x)+" appended to x_values"
#			count=count+1
#			if count==2:
				#print "count is: "+str(count)
				#x_values.append(x)
				#print str(x)+" appended to x_values
#				diff = x_values[1] - x_values[0]				
				#diff = answer2 - answer1
				#print "diff is: "+str(diff)
#				break
		#x = x + 1
#	return diff

#def MaxPower(i,N_remainder):				### Section: O(n+3)
#	m=0						#O(1)
#	while N_remainder > 1 and not N_remainder % i:	#O(n+2)
#		m += 1		
#		N_remainder //= i
#	return m



