#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 26. 15/03/2018.
#Programmed & tested in Python 2.76 only
#This program tests prop234.py 
#prop234.py attempts to solve a Discrete Log Problem (DLP) specified by user, via Proposition 2.34 (in J Hoffstein, J Pipher & J Silverman), via factorisation of (p-1) where p is a prime number. 
#Results printed are three arrays ...
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

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
	
def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	
	primes = csvfile_store_primes(primefile)
	
	#initialise g_values, p_values, and h_values	
	g_values = xrange(2,3)
	p_values = primes[0:1001]
	h_values = xrange(2,101)
	
	#define counts for different types of results
	count_nosolns=0
	count_x_equals_0=0
	count_normal_soln=0
	count_needlargerprimelist=0
	count_q_e_found=0
	count_q_e_not_found=0	
	count_notprime=0
	count_calc_xi_no_solns=0
	count_order_not_prime=0
	count_order_prime=0
	count_xi_not_found=0
	count_calc_xi_status_false=0
	
	#define lists for different types of results
	answers_to_be_checked=[]
	order_false_list=[]
	n_prime=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	
	print('Looping through values for g, p, & h..')
	print("======================================")

	#error = False	
	#while error==False:	
		for g in g_values:
			#h_values_no_solution = False
			for p in p_values:	
				max_order = p - 1
				no_prim_roots = p - 1			
				h_soln_alreadyfound = False
				concat_g_p = str(g)+"_"+str(p)
				print "concat_g_p is: "+str(concat_g_p)			
				if g == p:
					print "g = p !"
					count_nosolns = count_nosolns + len(h_values)	
				elif concat_g_p in order_false_list:
					count_nosolns = count_nosolns + len(h_values)
					print "Previously calculated - "+str(concat_g_p)+" is NOT in form q**e !"
					raw_input("Previously calculated - "+str(concat_g_p)+" is NOT in form q**e !")
					x_final = "No solns!"			
				else:				
					raw_input("******************calculating order*********************")
					print "******************calculating order*********************"

					#Calculate order							
					order_result = calc_order(g, p, count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, primes, n_prime, count_order_prime)

					#return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, q, e, order_status, n_prime, count_order_prime, order, lhs

					count_nosolns = order_result[0]
					count_order_not_prime = order_result[1]
					count_q_e_found = order_result[2]
					count_q_e_not_found = order_result[3]
					order_false_list = order_result[4]
					q = order_result[5]
					e = order_result[6]
					order_status = order_result[7]
					n_prime = order_result[8]
					count_order_prime = order_result[9]
					order = order_result[10]
					lhs = order_result[11]		

					for h in h_values:								
						concat_g_h = str(g)+"_"+str(h)
						if h >= p:
							print "Setting h_soln_alreadyfound to true.."
							h_soln_alreadyfound = True							
							break													
						
						elif g == h:
							x_final = 1
							x_moduli_final = p - 1
							x_final = str(x_final)+" mod "+str(x_moduli_final)	
						else:										
							if order_status == True:
								result = dlp(g, p, h, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, order_false_list, primes, q, e, n_prime, count_xi_not_found, count_calc_xi_status_false, lhs)

								#return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, count_xi_not_found, count_calc_xi_status_false

								x_final = result[0]
								#print "x_final after dlp() is: "+str(x_final)								
								count_nosolns = result[1]
								count_calc_xi_no_solns = result[2]
								count_normal_soln = result[3]
								x_moduli_final = result[4]
								answers_to_be_checked.append(result[5])
								count_x_equals_0 = result[6]
								count_needlargerprimelist = result[7]
								count_notprime = result[8]
								#order_false_list = result[9]
								count_xi_not_found = result[9]
								count_calc_xi_status_false = result[10]

								if x_final <> "No solns!":						
									x_final = str(x_final)+" mod "+str(x_moduli_final)
									
							elif order_status <> False:
								raw_input("******************calculating order*********************")
								print "***ERROR!!!*** order_status is: "+str(order_status)
								#error=True

def ghp_checks(g,h,p,floor_sqrt_p, count_a_notprime):	
	
	#print "Running ghp_checks().."

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

def isprime(p):			#this is O(sqrt(n))
	
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	return True			

#def dlp(g, p, h, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, order_false_list, primes, q, e, n_prime, count_xi_not_found, count_calc_xi_status_false):

def dlp(g, p, h, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, primes, q, e, n_prime, count_xi_not_found, count_calc_xi_status_false, lhs):

	#print "------------------------------------------------------"
	#print "Running dlp("+str(g)+", "+str(p)+", "+str(h)+", .. ).."

	floor_sqrt_p = int(math.floor(math.sqrt(p)))			#O(3)
	
	result=ghp_checks(g, h, p, floor_sqrt_p, count_notprime) 	#Best case: O(sqrt(n)+5) 	Worst case: O(sqrt(n)+8)
	#return status, a
	#status=0 for problem and 1 for no problem
	#a=True for Prime, a=False for not prime
	
	status_ghp = result[0]
	status_isprime_a = result[1]

	if status_isprime_a == False:					#O(1)
		count_notprime = count_notprime + 1			#O(1)
		print str(p)+" is not prime! Exiting.."		
		sys.exit()							#O(1)
	elif status_ghp == 0:						#O(1)
		print "At least one of checks for g, h or p failed! Exiting.."		
		sys.exit()							#O(1)
	else:
		#store result of p and isprime(p) so later we do not need to run isprime(p) again				
		n_prime.append(p)
	
		#check if sqrt_p > largest element in primes
		sqrt_p = math.sqrt(p)					#O(1)
		largest_prime = primes[-1]				#O(???)
		if sqrt_p > largest_prime:				#O(1)	#Subtotal: O(4)
			print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
			count_needlargerprimelist = count_needlargerprimelist + 1
			sys.exit()
		else:							#O(1)
			#initialise lists	
			x=[]		
			x_moduli=[]
					
			################################################
			# Prop_234 Algorithm
			
			result_prop_234 = prop_234(g, p, h, q, e, count_xi_not_found, count_calc_xi_status_false, lhs)
			#result_prop_234 = prop_234(g, p, h, q, e, count_xi_not_found, count_calc_xi_status_false)
			#return x, M, calc_xi_status, xi_found, count_xi_not_found, count_calc_xi_status_false
		
			x_initial = result_prop_234[0]
			moduli = result_prop_234[1]
			calc_xi_status = result_prop_234[2]				#O(1)				
			xi_found = result_prop_234[3]					#O(1)	
			count_xi_not_found = result_prop_234[4]
			count_calc_xi_status_false = result_prop_234[5]

			#print "x_initial after prop_234() is: "+str(x_initial)
			if calc_xi_status == True and xi_found == True:
				#Calc_xi method found solutions
				x.append(x_initial)
				if x_initial == 0:		
					count_x_equals_0 = count_x_equals_0 + 1 
					x_moduli.append(moduli)
					if moduli == 0:
						print "x[0]=0 and x_moduli[0] is 0!"
						raw_input("Waiting for user..")
					count_normal_soln = count_normal_soln + 1

					if pow(g,x[0],p) <> h:			#O(1)
						print "CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x[0])+", x_moduli: "+str(x_moduli[0])
						answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x[0]))	#O(1)
						sys.exit()

					return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, count_xi_not_found, count_calc_xi_status_false

				else:
					x_moduli.append(moduli)
					if moduli == 0:
						print "x[0] <> 0 and moduli is 0!"
						raw_input("Waiting for user..")
					count_normal_soln = count_normal_soln + 1
					if pow(g,x[0],p) <> h:			#O(1)
						#print "CHECK ANSWER!!!"
						print "CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x[0])+", x_moduli: "+str(x_moduli[0])
						answers_to_be_checked.append(str(g)+"_"+str(h)+"_"+str(p)+"_"+str(x[0]))	#O(1)
						sys.exit()

					return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, x_moduli[0], answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, count_xi_not_found, count_calc_xi_status_false

			elif xi_found == False:
				#Calc_xi method failed to find solutions - an xi was not found !
				x.append("No solns!")
				count_calc_xi_no_solns = count_calc_xi_no_solns + 1
				count_nosolns = count_nosolns + 1				#O(1)

				return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, count_xi_not_found, count_calc_xi_status_false
			elif calc_xi_status == False:
				#Calc_xi method failed to find solutions - lhs=1 and rhs=1	
				x.append("No solns!")
				count_calc_xi_no_solns = count_calc_xi_no_solns + 1
				count_nosolns = count_nosolns + 1				#O(1)
				
				return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, count_xi_not_found, count_calc_xi_status_false
			else:
				print "calc_xi_status is: "+str(calc_xi_status)
				print "xi_found is: "+str(calc_xi_status)
				raw_input("Waiting for user..")
				
				return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, count_xi_not_found, count_calc_xi_status_false

def calc_order(g, p, count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, primes, n_prime, count_order_prime):

	print "Running calc_order().."	

	#use exponent function to get order of g mod p
	result = exponent_g_n(g, 1, p)				#Worst: O(n + 7)	#Best: O(8)
	#return x, status
	#status is False for no exponent found	
	#status is True for exponent found
	order = result[0]					#O(1)
	status = result[1]					#O(1)
	
	raw_input("Can order only be 1 or prime??")

	# Now want order = q**e, where q is prime - obtain q and e 
	if order == 1:						#O(1)
		order_false_list.append(str(g)+"_"+str(p))
		count_order_not_prime = count_order_not_prime + 1	#O(1)
		count_q_e_not_found = count_q_e_not_found + 1		#O(1)
		count_nosolns = count_nosolns + 1			#O(1)
		order_status = False
		q = 0
		e = 0
		lhs = 0
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, q, e, order_status, n_prime, count_order_prime, order, lhs
	elif order in n_prime:				
		q = order						#O(1)
		e = 1							#O(1)
		count_order_prime = count_order_prime + 1		#O(1)
		count_q_e_found = count_q_e_found + 1			#O(1)
		order_status = True
		lhs = pow(g,pow(q,ei-1),p)
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, q, e, order_status, n_prime, count_order_prime, order, lhs
	elif isprime(order) == True:				#O(sqrt(n))
		n_prime.append(order)
		q = order						#O(1)
		e = 1							#O(1)
		count_order_prime = count_order_prime + 1		#O(1)
		order_status=True
		count_q_e_found = count_q_e_found + 1			#O(1)
		lhs = pow(g,1,p)
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, q, e, order_status, n_prime, count_order_prime, order, lhs
	else:
		raw_input("Check using calc_q_e()..")		
		count_order_not_prime = count_order_not_prime + 1	#O(1)

		#now check if order is of form q**e, where q is prime, e >= 1 - Need to find q and e.
					
		result = calc_q_e(primes, order, p)			#Worst: O(n**2+7n+4)	#Best: O(12)
		#return q, e, result

		q=result[0]						#O(1)
		e=result[1]						#O(1)
		order_status=result[2]					#O(1)
		if order_status == False:
			order_false_list.append(str(g)+"_"+str(p))		#O(1)
			count_q_e_not_found = count_q_e_not_found + 1		#O(1)
			lhs = 0
		elif order_status == True:
			count_q_e_found = count_q_e_found + 1			#O(1)
			lhs = pow(g,pow(q,ei-1),p)
		else:
			print "order_status is: "+str(order_status)
			raw_input("Waiting for user..")

		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, q, e, order_status, n_prime, count_order_prime, order, lhs
									
def calc_q_e(primes, order, p):
	
	#print "Running calc_q_e(primes, "+str(k)+", "+str(p)+")"	
	#q needs to be prime, e >= 1
	#p is prime

	raw_input("calc_q_e() - Should one take pow(prime,n) or pow(prime,n, p)??")

	#Worst: O(n**2+7n+4)	#Best: O(12)

	result=False			#O(1)
	q=0				#O(1)
	e=0				#O(1)
	n=1				#O(1)
	
	for prime in primes:		#O(n)	#Worst: O(n**2+7n)	#Best: O(8)
		n = 1					
		while result is False and prime < p and n <= order and pow(prime,n) <= order:	#O(n)	#Worst: O(n+7)	#Best: O(7)
			if pow(prime,n) == order:					#O(2)
				q = prime					#O(1)
				e = n						#O(1)
				result = True					#O(1)
				break						#O(1)
			else:
				n = n + 1					#O(1)
	if result==True:
		raw_input("calc_q_e() - q and e found!")

	return q, e, result

def exponent_g_n(generator,h_value, p):
	n=1						#O(1)
	x=0						#O(1)
	status=False					#O(1)
	while n < p:					#O(n)	#Worst: O(n + 7)
		if pow(generator,n,p) == h_value:		#O(2)	#Worst: O(6)
			x = n				#O(1)
			status=True			#O(1)
			break				#O(1)
		n = n + 1				#O(1)

	if x==0:					#O(1)
		x="No exponent found"			#O(1)
		status=False				#O(1)

	return x, status

def prop_234(g, p, h, qi, ei, count_xi_not_found, count_calc_xi_status_false, lhs):
	#print "Running prop_234("+str(g)+", "+str(p)+", "+str(h)+", "+str(qi)+", "+str(ei)+", "+str(count_xi_not_found)+", "+str(count_calc_xi_status_false)+").."

	# constuct list of q_powers from 0 to e-1
	q_powers=[]						#O(1)

	#first q_power will always be 1 (for k=0)
	if ei > 0:						#O(1)	#worst: O(n+3)	#best: O(1)
		for k in xrange(0,ei):					#O(n)
			q_powers.append(pow(qi,k))			#O(2)
	elif ei==0:						#O(1)	#worst: O(3)
		print "ei = 0!"					
		sys.exit()					#O(1)

	else:							#O(1)	#worst: O(4)
		print "ei is: "+str(ei)
		sys.exit()					#O(1)

	#now want to calculate xi using function	
	result = calc_xi(q_powers, g, p, h, qi, ei, lhs)
	#return xi, calc_xi_status, xi_found	
	xi = result[0]
	calc_xi_status = result[1]
	xi_found = result[2]

	#print "xi after calc_xi() is: "+str(xi) 
	#print "calc_xi_status after calc_xi() is: "+str(calc_xi_status) 
	#print "xi_found after calc_xi() is: "+str(xi_found) 

	if calc_xi_status == False:
		count_calc_xi_status_false = count_calc_xi_status_false + 1
		x=0 						#O(1)
		M=0						#O(1)
	elif xi_found == False:				#O(1)
		count_xi_not_found = count_xi_not_found + 1
		x=0 						#O(1)
		M=0						#O(1)
	elif calc_xi_status == True and xi_found == True:		#O(1)	#Subtotal - Worst: O(n**2 + 7n + 2), Best: O(n+5) when only 1 as q_power
		for q_power in q_powers: 			#O(n)	#Worst: O(n**2 + 7n)	#Best: O(n+4) - when only 1 as q_power
			a=xi[q_powers.index(q_power)] 							#O(n+1)
			if q_power==1: 									#O(1)
				x = a										#O(1)
			else:										#O(1)
				x = (x + a * q_power) % pow(qi,ei)					#O(4)
		M = pow(qi,ei)					#O(1)		
	else:
		print "calc_xi_status is: "+str(calc_xi_status)
		print "xi_found are: "+str(xi_found)
		raw_input("Waiting for user..")

	return x, M, calc_xi_status, xi_found, count_xi_not_found, count_calc_xi_status_false

def calc_xi(q_powers, g, p, h, qi, ei, lhs):
	#print "Running calc_xi("+str(q_powers)+", "+str(g)+", "+str(p)+", "+str(h)+", "+str(qi)+", "+str(ei)+", "+str(lhs)+").."

	#initialise xi, cumul_q_powers, cumul_xi_q_powers
	xi = len(q_powers) * [0]				#O(len(q_powers))
	cumul_q_powers=[]					#O(1)
	cumul_xi_q_powers=[]					#O(1)
	calc_xi_status=True					#O(1)

	#print "q_powers is: "+str(q_powers)
	#print "e is: "+str(ei)

	#Loop through each q_power until xi are calculated
	for q_power in q_powers:
		if calc_xi_status == True:
			if q_power==1:							#total (incl top lev if) = 
				#print "q_power is: "+str(q_power)				
				xi_found = False
				#print "pow("+str(qi)+","+str(ei-1)+") is: "+str(pow(qi,ei-1))
				#lhs= pow(g,pow(qi,ei-1),p)				#O(2)
				rhs= pow(h,pow(qi,ei-1),p)				#O(2)
				#print "lhs is: "+str(lhs)+", rhs is: "+str(rhs)
				if lhs ==1 and rhs ==1:					#O(1)		#subtotal: O(2)	#section= O(2n+6)				
					calc_xi_status=False				#O(1)

				else:							#O(1)		#Worst: O(4n+1)	#best: O(6)
					for t in xrange(0, qi):				#O(n)		#Worst: O(4n)	#best: O(5)
						if pow(lhs,t,p) == rhs:			#O(2)		#Worst: O(4)	#best: O(4)
							xi[0]=t  # xi[0]=		#O(1)
							xi_found = True
							break				

				if calc_xi_status == True:				#O(1)		#subtotal= O(3)
					cumul_xi_q_powers.append(xi[0])			#O(1)
					cumul_q_powers.append(1)			#O(1)
			else:								#O(1)		#total (incl top lev if) = 
				#print "q_power is: "+str(q_power)
				xi_found = False
				xi_number = q_powers.index(q_power)			#O(n)
				a = xi_number-1						#O(1)
				z=0
				for cumul_xi_q_power in cumul_xi_q_powers:		#O(n+1)
					z = z + cumul_xi_q_power
				
				if xi[xi_number-1] >= 0:
					#need to work out what g**-[x_0+x_1*q_power+x_2*q_power**2 + ...], mod p is!!!
					b = calc_modinverse(g, z, p)									#O(n+5)
					rhs = pow(h * b,pow(qi,ei - xi_number - 1),p)
					#print "lhs is: "+str(lhs)+", rhs is: "+str(rhs)
					if lhs == 1 and rhs == 1:									#O(1)	#Subtotal O(4)
						#print "lhs == 1 and rhs == 1"								
						#This method seems to fail for this instance. Brute force search instead??
						calc_xi_status=False									#O(1)
						print "Calc_xi method failed. h is "+str(h)+", p is "+str(p)+", qi is "+str(qi)+", ei is "+str(ei)+", xi_number is "+str(xi_number)															#O(1)
						sys.exit()
					else:												#O(1)	#Subtotal O(n**2+5n+1)
						for t in xrange(0, qi):									#O(n)
							if lhs**t % p == rhs:								#O(n+2)
								xi[xi_number]=t									#O(1)
								xi_found = True
								break										#O(1)

					if calc_xi_status == True:									#O(1)	#Subtotal O(n**2+5n+1)
						cumul_xi_q_powers.append(q_power * xi[xi_number])						#O(3)
						cumul_q_powers.append(q_power)									#O(1)
				else:													#O(1)
					print("xi["+str(xi_number-1)+"] is negative !!! CHECK")							
					sys.exit()												#O(1)
		
	return xi, calc_xi_status, xi_found

def calc_modinverse(g, power, p):
	#print "Running calc_modinverse("+str(g)+", "+str(power)+", "+str(p)+").."
	floor_sqrt_p = math.floor(math.sqrt(p))					#O(2)

	if isprime(p) == True:							#O(1)	#Subtotal O(2n+4)
		result=g**(p-2)% p						#O(n+2)	#Subtotal O(2n+3)
		c = result**power % p						#O(n+1)
	else:
		c = modinv(g, p)						#O(n)
	return c

def csvfile_store_primes(csv_filename_var):		### Assumming O(n+len(z1)+1) ### 
		
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers - Use generator to get number of primes to use in prime file..
		z1=(int(x) for row in csv.reader(csvfile) for x in row)			#O(n) - Potentially y rows and x items in each row, 
											# however only 1 row in csvfile being used. Hence x*y=x items to store
		primes=list(z1)								#O(len(z1))
		csvfile.close()								#O(1 ???)
	return primes

def egcd(a, b):							#O(n)
	if a == 0:						#O(1)	#Subtotal: O(2)
		return (b, 0, a)				#O(1)
	g, y, x = egcd(b % a, a)				
	return (g, x - (b//a) * y, y)

def modinv(a, m):						#### O(n+5) ###
	#print "Running modinv("+str(a)+", "+str(m)+").."
	g, x, y = egcd(a, m)					#O(n)
	if g != 1:							#O(1)	#Subtotal: O(2)
		raise Exception('No Modular Inverse') 			#O(1)
	return x % m						#O(1)

if __name__=='__main__':
	main()

#def size_input_check(input_number):
#
#	#if size of number >= 2*10^8 then return message about memory & exit
#	if input_number>2*(10**8):
#		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
#		sys.exit()

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

#def prim_root(g, p, n_prime):
#
#	print "Running prim_root("+str(g)+", "+str(p)+"..) .."

	#Assuming p is prime: 		Best case: O(46)	Worst case: O(???)
	#Assuming p is not prime: 	O()
	
#	if p in n_prime:				#O(n)
		#we have already ran isprime(p) and it was prime
		#hence ep = p-1
#		ep = p - 1					#O(1)	
#		status_ep = True				#O(1)
#	else:						#O(1)
		#Check if p is prime		
#		if isprime(p)==True:			#O(sqrt(size(p)))
#			ep = p - 1
#			status_ep = True
#		else:
			#p is not prime, hence need to factorise p first & get "primes" and "powers" first. 
			
#			result = euler_phi(p)			#when n is not prime 	Worst: O(sqrt(n)+8) Best: O(4) when n=1
								#when n is prime	#O(sqrt(n)+5) 
			#result = euler_phi(p, primes)				
			#return a, status
#			ep = result[0]					#O(1)
			#status_ep = result[1]				#O(1)
			#print "euler_phi("+str(p)+") is: "+str(ep)		
			
#	if status_ep == False:				#O(1)
		#ie p=1 or p is not prime
#		print "status_ep is: "+str(status_ep)+", ep is: "+str(ep)
#		sys.exit()					#O(1)
#	else:						#O(1)
		#p is prime, ep = p-1		
#		result1 = factorise(ep)				#Worst: O(sqrt(n))
		#return factors, c_factorisations
#		factors = result1[0]			#O(1)
#		c_factorisations = result1[1]		#O(1)

#		print "factors of "+str(ep)+" are: "+str(factors)
		#print "time for factorisation of "+str(ep)+" is: "+str(c_factorisations)
	
#		result2 = calc_powers(factors)				#Worst: O(n+13)	#Best: O(18) 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(n))
		#return prime_factors, powers, c_calc_powers		
#		prime_factors = result2[0]				#O(1)
#		powers = result2[1]					#O(1)
#		c_calc_powers = result2[2]				#O(1)
#		total_calc_time = c_factorisations + c_calc_powers	#O(1)

#		print "prime factors are: "+str(prime_factors)
#		print "powers are: "+str(powers)
		#print "time for calc prime factors & powers is: "+str(c_calc_powers)
		#print "total calc time for prime_factors and powers is: "+str(total_calc_time)
		
#		status = True						#O(1)	
#		power=1							#O(1)

		#print "Now testing if "+str(g)+" is a primitive root mod "+str(p)+".."
		#testing if g is a primitive root mod p
		# first compute euler_phi(n) = ep = p-1
		# then determine prime factors of ep, say p_1, p_2, ... p_k
		# Now for every element m of Z_n*, compute pow(m,ep/p_i,n), for i=1,..,k
		# eg p = 109 => ep = 108. 108=2**5 * 3**1
		# m = 2 
		# 1st loop compute pow(2,108/2,109) = pow(2,54,109) = 108 = -1
		# 2nd loop compute pow(2,108/3,109) = pow(2,36,109) = 108 = 1
		# break since RHS = 1
		
#		for prime in prime_factors:				#O(n)	#Worst: O(5*len(prime_factors))	#Best: O(6)
			#if status==True:					
			#print "================="
			#print "prime is: "+str(prime)
#			if pow(g,ep / prime,p)==1:				#O(3) 	#Worst: O(5) #Best: O(3)
#				print "pow("+str(g)+","+str(ep)+" / "+str(prime)+","+str(p)+") is 1"	
#				status=False						#O(1)
#				break							#O(1)

		#print "Status is: "+str(status)

		#raw_input("Waiting for user..")

#		return status, prime_factors, powers
		#return status, prime_factors, powers, remainder

#def euler_phi(n):				
	
	#when n is not prime
	# Worst: O(sqrt(n)+8)  
	# Best:	O(4) when n=1

	#when n is prime
	#O(sqrt(n)+5) 

	#euler_phi(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.	
	
	#print "Running euler_phi("+str(n)+")..."
	
	#print "isprime_result is: "+str(isprime_result)

	#left_isprime_result=left()

#	status = True 					#O(1)
	#floor_sqrt_n = math.floor(math.sqrt(n))

	#print "isprime(n) is: "+str(isprime(n)
	#print "isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#status=1 for not prime
	#status=0 for prime

#	if n==1:					#O(1)	#subtotal O(3)
#		a = 1					#O(1)
#		status = False				#O(1)		
#		return a, status			#O(1)

#	elif isprime(n) == True:			#O(sqrt(n)+1) #subtotal O(sqrt(n)+3) 
	#elif isprime(n,floor_sqrt_n) == 0:
#		a = n - 1				#O(1)
#		return a, status			#O(1)
				
#	else:							#subtotal O(???)
		#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.
		#euler_phi(p**k) = (p-1)*p**(k-1) for prime p 
		#euler_phi(m*n) = euler_phi(m)*euler_phi(n) for coprime m & n

		#euler_phi(n) = p_1**(k_1-1)*p_2**(k_2-1)*p_3**(k_3-1)... , where p_i are prime factors of n, and k_i are corresponding powers.
		#need primes & powers from factorise()!
				
#		result1 = factorise(n)				#Worst: O(sqrt(size(n)))
		#return factors, c_factorisations
#		factors = result1[0]			#O(1)
#		c_factorisations = result1[1]		#O(1)

#		print "factors of "+str(ep)+" are: "+str(factors)
#		print "time for factorisation of "+str(ep)+" is: "+str(c_factorisations)
	
#		result2 = calc_powers(factors)				#Worst: O(size(n)+13)	#Best: O(18) 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		#return prime_factors, powers, c_calc_powers		
#		prime_factors = result2[0]				#O(1)
#		powers = result2[1]					#O(1)
#		c_calc_powers = result2[2]				#O(1)
#		total_calc_time = c_factorisations + c_calc_powers	#O(1)

#		print "prime factors are: "+str(prime_factors)
#		print "powers are: "+str(powers)
		#print "time for calc prime factors & powers is: "+str(c_calc_powers)
		#print "total calc time for prime_factors and powers is: "+str(total_calc_time)
		
#		len_prime_factors = len(prime_factors)
#		len_powers = len(powers)
		
		#check lengths of lists
#		if len_prime_factors <> len_powers:
#			print "length(prime_factors) <> length(powers)! Exiting.."			
#			sys.exit() 

		#euler_phi(n) = p_1**(k_1-1)*p_2**(k_2-1)*p_3**(k_3-1)... , where p_i are prime factors of n, and k_i are corresponding powers.

#		raw_input("Waiting for user...")		

		#for b in xrange(0,len_prime_factors):
#		for prime in primes:
#			print "============================"
#			number = primes.index(prime)
#			print "number is: "+str(prime)
#			print "prime is: "+str(prime)
#			if not a:			
#				print "power is: "+str(power(number))
#				a = prime **(power(number)-1)
#				print "a is now: "+str(a)
#			else:
#				print "power is: "+str(power(number))
#				a = a * prime **(power(number)-1)
#				print "a is now: "+str(a)

#		status = True						#O(1)	
#		power=1							#O(1)

		#print str(n)+" is not prime!"		
#		status = False				#O(1)
#		return a, status			#O(1)

#def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#Create lists to hold prime factors of N and corresponding powers
#	factors = []					#O(1)
#	s_before_factorisations = time.clock()		
		
#	gaps=[1,2,2,4,2,4,2,4,6,2,6]			#O(1)
#	length, cycle = 11,3				#O(1)
#	f, factors, next = 2, [], 0			#O(1)
#	while f*f <= N:					#O(n)
#		while N % f == 0:				#O(n)
			#f is a factor. Add factor f to fs
#			factors.append(f)				#O(1)
#			N /= f						#O(1)
#		f += gaps[next]				#O(1)
#		next += 1				#O(1)
#		if next == length:			#O(1)
#			next = cycle				#O(1)
#	if N > 1: factors.append(N)
		
#	c_factorisations = time.clock() - s_before_factorisations	#O(1)

#	return factors, c_factorisations		#O(1)

#def a_exp_x_eq_r(a,p,r):
#	x=1
#	x_values=[]
#	count=0
#	diff=0
#	for x in xrange(0,2*p):
#		if pow(a,x,p) == r:
#			x_values.append(x)
#			count=count+1
#			if count==2:
#				diff = x_values[1] - x_values[0]				
#				break
#	return diff

#def calc_powers(factors):
#	#Now want to find max powers m for each factor in factors - can do this by counting unique factors			
#	prime_factors=[]					#O(1)
#	powers = []						#O(1)
#	fac_list = []						#O(1)
#	count = 0						#O(1)
#	c_primefactors_powers = 0				#O(1)
#	s_before_calc_powers = time.clock()			#O(1)
#	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
#		if fac_list:						#O(1)	#Worst: O(n+2)	#Best: O(4)
#			if factor in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
#				count += 1						#O(1)
#			else:							#O(1)
#				#factor is not in fac_list - add factor to prime_factors
#				prime_factors.append(factor)				#O(1)
#				#add current count to powers for previous factor
#				powers.append(count)					#O(1)
#				#append it				
#				fac_list.append(factor)					#O(1)
#				count = 1						#O(1)
#		else:								#O(1)	#Subtotal: O(4)
			#temp factor list for comparisons is empty - store 1st factor
#			fac_list.append(factor)						#O(1)
#			prime_factors.append(factor)					#O(1)
#			count += 1							#O(1)
		
	#add count to powers for the last factor and the last factor
#	powers.append(count)
#	c_calc_powers = time.clock() - s_before_calc_powers

#	return prime_factors, powers, c_calc_powers

