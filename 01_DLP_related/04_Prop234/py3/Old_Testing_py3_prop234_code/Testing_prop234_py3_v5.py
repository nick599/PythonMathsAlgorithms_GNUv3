#Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.
#Version 4. 12/09/2019.
#Programmed & tested in Python 3.XX only
#This program tests the algorithm in prop234_py3.py - solving multiple Discrete Log Problems (DLPs) specified by user in ranges, via Proposition 2.34 (in J Hoffstein, J Pipher & J Silverman) using order of g mod p, where p is a prime number.
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v4.XX x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

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

print("Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.")
print("Version 4. 12/09/2019.")
print("Programmed & tested in python 3.XX only.")
print("---------------------------------------------------------------------")
print("This program tests the algorithm in prop234.py - solving multiple Discrete Log Problems (DLPs) specified by user in ranges, via Proposition 2.34 (in J Hoffstein, J Pipher & J Silverman) using order of g mod p, where p is a prime number.")
#print("Results printed are three arrays ..."
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v4.XX x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")
	
def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	print("primefile currently is: "+str(primefile))

	#define prime list
	#print('Importing primes from csv file')
	primes = csvfile_store_primes(primefile)
	#print('First ten primes are: '+str(primes[0:10]))

	#print(sys.version_info)

	#initialise g_values, p_values, and h_values
	
	#g_values = range(2,3)
	g_values = range(2,20)
	p_values = primes[0:101]
	#p_values = primes[0:1001]
	#h_values = range(2,201)

	total_g_values=len(g_values)
	print("total_g_values: "+str(total_g_values))

	total_p_values=len(p_values)
	print("total_p_values: "+str(total_p_values))

	#total_h_values=len(h_values)
	#print("total_h_values: "+str(total_h_values)

	Total_values = total_g_values * total_p_values 
	print("Total_values: "+str(Total_values))
	#Grand_total_values = total_p_values * total_g_values * total_h_values
	#print("Grand_total_values: "+str(Grand_total_values)

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
	#order_false_list=[]
	n_prime=[]
	q_e_nf_order_p_list=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print("======================================")

	print('Looping through values for g, p, & h..')

	previous_calc_g_p=[]
	previous_calc_orders=[]
	for g in g_values:
		print("g is:",str(g))
		order = 0		
		#h_values_no_solution = False
		for p in p_values:
			print("p is:",str(p))
			#print("===================================="	
			#print("p is: "+str(p)	
			if g % p == 0:
				count_nosolns = count_nosolns + len(range(1,p+1))

			if g > p:			
				g_old = g				
				g_new = g % p
				print("g:",g_old,"> p:",p,"- revised g_new is:",g_new)
				
				# 2 < order <= p - 1
				#no_prim_roots = p - 1 #for F_p this is euler_phi(p) = p-1 since p is prime.					
			
				result = Calc_prop_234(g_new,p,count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, primes, n_prime, count_order_prime, previous_calc_g_p, previous_calc_orders, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, count_xi_not_found, count_calc_xi_status_false)



			elif str(g)+"_"+str(p) not in previous_calc_g_p:
			
				result = Calc_prop_234(g,p,count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, primes, n_prime, count_order_prime, previous_calc_g_p, previous_calc_orders, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, count_xi_not_found, count_calc_xi_status_false)



	#print("Grand_total_considered: "+str(Grand_total_values)+", total_g_values: "+str(total_g_values)+", total_p_values: "+str(total_p_values)+", total_h_values: "+str(total_h_values)+", number_no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_q_e_found: "+str(count_q_e_found)+", count_q_e_not_found: "+str(count_q_e_not_found)+", count_order_prime: "+str(count_order_prime)+", count_order_not_prime: "+str(count_order_not_prime)+", count_xi_not_found: "+str(count_xi_not_found)+", count_calc_xi_status_false: "+str(count_calc_xi_status_false))

	print("total_g_values: "+str(total_g_values)+", total_p_values: "+str(total_p_values)+", number_no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_q_e_found: "+str(count_q_e_found)+", count_q_e_not_found: "+str(count_q_e_not_found)+", count_order_prime: "+str(count_order_prime)+", count_order_not_prime: "+str(count_order_not_prime)+", count_xi_not_found: "+str(count_xi_not_found)+", count_calc_xi_status_false: "+str(count_calc_xi_status_false))

def Calc_prop_234(g,p,count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, primes, n_prime, count_order_prime, previous_calc_g_p, previous_calc_orders, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, count_xi_not_found, count_calc_xi_status_false):

				print("Running Calc_prop_234(",g,",",p,")")
				if str(g)+"_"+str(p) in previous_calc_g_p:
					#Order for g & p has already been calculated previously
					print("Order for g_new:",g,",p:",p,"has already been calculated previously")
					input("Waiting for user..")
					order=""
				elif str(g)+"_"+str(p) not in previous_calc_g_p:
					g_p_to_append=[]
					g_p_to_append.append(str(g)+"_"+str(p))
					previous_calc_g_p.append(g_p_to_append)
				else:				
					print("Order for g:",g,",p:",p,"does not match criteria - not in previous_calc_g_p!")

				if g == 1:
					#order = Not found!
					count_nosolns = count_nosolns + 1
					count_order_not_prime = count_order_not_prime + 1
					count_q_e_not_found = count_q_e_not_found + 1
					order="Not found"

					g_p_order_to_append=[]
					g_p_order_to_append.append(str(g)+"_"+str(p))
					g_p_order_to_append.append(str(order))
					previous_calc_orders.append(g_p_order_to_append)

				else:
					#Calculate order							
					order_result = calc_order(g, p, count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, primes, n_prime, count_order_prime, previous_calc_g_p)

					#return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, q, e, order_status, n_prime, count_order_prime, order, lhs

					count_nosolns = order_result[0]
					count_order_not_prime = order_result[1]
					count_q_e_found = order_result[2]
					count_q_e_not_found = order_result[3]
					q_e_nf_order_p_list = order_result[4]
					q = order_result[5]
					e = order_result[6]
					order_status = order_result[7]
					n_prime = order_result[8]
					count_order_prime = order_result[9]
					order = order_result[10]
					lhs = order_result[11]
					concat_order_p=str(order)+"_"+str(p)

					g_p_order_to_append=[]
					g_p_order_to_append.append(str(g)+"_"+str(p))
					g_p_order_to_append.append(order)
					previous_calc_orders.append(g_p_order_to_append)
				
					if str(order)+"_"+str(p) in q_e_nf_order_p_list:
						#print(str(order)+"_"+str(p),"is in q_e_nf_order_p_list")
					#elif concat_g_p in order_false_list:
						count_nosolns = count_nosolns + len(range(1, p+1))
						#count_nosolns = count_nosolns + len(h_values)
						#print("Previously calculated - "+str(concat_order_p)+" is NOT in form q**e !"
						x_final = "No solns!"			
						#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", x: "+str(x_final)+", no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_q_e_found: "+str(count_q_e_found)+", count_q_e_not_found: "+str(count_q_e_not_found)+", count_order_prime: "+str(count_order_prime)+", count_order_not_prime: "+str(count_order_not_prime)+", count_xi_not_found: "+str(count_xi_not_found)+", count_calc_xi_status_false: "+str(count_calc_xi_status_false)
					else:
						h_soln_alreadyfound = False
						for h in range(1, p+1):
						#for h in h_values:								
							#concat_g_h = str(g)+"_"+str(h)
							#print("-----------------------------------"
							#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)
							if h >= p:
								#print("Setting h_soln_alreadyfound to true.."
								h_soln_alreadyfound = True							
								break													
						
							elif g == h:
								x_final = 1
								x_moduli_final = p - 1
								x_to_print = str(x_final)+" mod "+str(x_moduli_final)
	
								#Check answers
								if pow(g, x_final, p) != h:
									print("CHECK x_final! g_new: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli: "+str(x_moduli))
									input("Waiting for user..")

								elif pow(g, x_final + x_moduli_final, p) != h:
									print("CHECK x_moduli_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli_final: "+str(x_moduli_final))
									input("Waiting for user..")

								#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", x: "+str(x_final)
						
								#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", x: "+str(x_final)+", no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_q_e_found: "+str(count_q_e_found)+", count_q_e_not_found: "+str(count_q_e_not_found)+", count_order_prime: "+str(count_order_prime)+", count_order_not_prime: "+str(count_order_not_prime)+", count_xi_not_found: "+str(count_xi_not_found)+", count_calc_xi_status_false: "+str(count_calc_xi_status_false)							
	
							else:										
								if order_status == True:
									#print("q is: "+str(q)+", e is: "+str(e) 
									#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.	
									#print('Running dlp()..')
							
									#print("-----------------------------------"
									#print("count_nosolns before dlp(): "+str(count_nosolns)

									result = dlp(g, p, h, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, q_e_nf_order_p_list, primes, q, e, n_prime, count_xi_not_found, count_calc_xi_status_false, lhs)

									#print("return back to h_values loop.."								

									x_final = result[0]
									count_nosolns = result[1]
									count_calc_xi_no_solns = result[2]
									count_normal_soln = result[3]
									x_moduli_final = result[4]
									answers_to_be_checked.append(result[5])
									count_x_equals_0 = result[6]
									count_needlargerprimelist = result[7]
									count_notprime = result[8]
									q_e_nf_order_p_list = result[9]
									#order_false_list = result[9]
									count_xi_not_found = result[10]
									count_calc_xi_status_false = result[11]

									#print("count_nosolns after dlp(): "+str(count_nosolns)
									#print("x_final is: "+str(x_final)
									#print("x_moduli_final is: "+str(x_moduli_final)
									if x_final != "No solns!":						
										#print("x_final != No solns!"
										x_to_print = str(x_final)+" mod "+str(x_moduli_final)
										#input("Waiting for user..")						

										#Check answers
										if pow(g, x_final, p) != h:
											print("CHECK x_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli: "+str(x_moduli))
											input("Waiting for user..")

										elif pow(g, x_final + x_moduli_final, p) != h:
											print("CHECK x_moduli_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli_final: "+str(x_moduli_final))
											input("Waiting for user..")

									#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", x: "+str(x_final)

								elif order_status != False:
									print("***ERROR!!!*** order_status is: "+str(order_status))
									input("Waiting for user..")								
									#error=True

				return x_final, count_nosolns, count_calc_xi_no_solns, count_normal_soln, x_moduli_final, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, q_e_nf_order_p_list, count_xi_not_found, count_calc_xi_status_false


def ghp_checks(g,h,p,floor_sqrt_p, count_a_notprime):	
	
	#print("Running ghp_checks().."

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
	
	#print("Running isprime(",p,")")
	
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		#print("p is: "+str(p)+", i is: "+str(i)		#"g = 4" #"p is: No exponent found, i is: 2"
		if p % i == 0:
			return False
		i += 1

	return True		

def dlp(g, p, h, count_nosolns, count_x_equals_0, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_calc_xi_no_solns, count_notprime, q_e_nf_order_p_list, primes, q, e, n_prime, count_xi_not_found, count_calc_xi_status_false, lhs):

	#print("-------------------------------------------------"
	#print("Running dlp("+str(g)+", "+str(p)+", "+str(h)+"..)"

	floor_sqrt_p = int(math.floor(math.sqrt(p)))			#O(3)
	#print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	#result=ghp_checks(g,h,p,floor_sqrt_p)
	#count_notprime = 0						#O(1)
	
	result=ghp_checks(g, h, p, floor_sqrt_p, count_notprime) 	#Best case: O(sqrt(n)+5) 	Worst case: O(sqrt(n)+8)
	#return status, a
	#status=0 for problem and 1 for no problem
	#a=True for Prime, a=False for not prime
	
	status_ghp = result[0]
	status_isprime_a = result[1]

	if status_isprime_a == False:					#O(1)
		count_notprime = count_notprime + 1			#O(1)
		print(str(p)," is not prime! Exiting..")	
		sys.exit()							#O(1)
	elif status_ghp == 0:						#O(1)
		print("At least one of checks for g, h or p failed! Exiting..")	
		sys.exit()							#O(1)
	else:
		#store result of p and isprime(p) so later we do not need to run isprime(p) again				
		n_prime.append(p)
		
		#print("n_prime is: "+str(n_prime)

		#check if sqrt_p > largest element in primes
		#print('checking if square root of p > largest element in primes...')
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
			
			#print("g: "+str(g)+", h: "+str(h)+", q: "+str(q)+", e: "+str(e)+", p: "+str(p)
			#count_xi_not_found, count_calc_xi_status_false
			result_prop_234 = prop_234(g, h, q, e, p, count_xi_not_found, count_calc_xi_status_false, lhs)
			#result_prop_234 = prop_234(g, h, q, e, p)
			
			#return x, M, calc_xi_status, xi_found, count_xi_not_found, count_calc_xi_status_false
		
			x_initial = result_prop_234[0]
			moduli = result_prop_234[1]
			calc_xi_status = result_prop_234[2]				#O(1)				
			xi_found = result_prop_234[3]					#O(1)	
			count_xi_not_found = result_prop_234[4]
			count_calc_xi_status_false = result_prop_234[5]

			#print("calc_xi_status is: "+str(calc_xi_status)
			if calc_xi_status == True and xi_found == True:
				#Calc_xi method found solutions
				#print("x_initial is: "+str(x_initial))
				x.append(x_initial)
				#print("x is: "+str(x[0]))
				#print str(x_initial)+" appended to x"
				if x_initial == 0:		
					#print("x[0] = 0")
					count_x_equals_0 = count_x_equals_0 + 1 
					x_moduli.append(moduli)
					if moduli == 0:
						print("x[0]=0 and x_moduli[0] is 0!")
						input("Waiting for user..")
					else:
						count_normal_soln = count_normal_soln + 1

					if pow(g,x[0],p) != h:			#O(1)
						#print("CHECK ANSWER!!!"
						print("CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x[0])+", x_moduli: "+str(x_moduli[0]))
						answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x[0]))	#O(1)
						sys.exit()

					return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, q_e_nf_order_p_list, count_xi_not_found, count_calc_xi_status_false

				else:
					#print("x[0] != 0"
					x_moduli.append(moduli)
					#print str(result_prop_234[1])+" appended to x_moduli"
					if moduli == 0:
						print("x[0] != 0 and moduli is 0!")
						input("Waiting for user..")
					count_normal_soln = count_normal_soln + 1
					if pow(g,x[0],p) != h:			#O(1)
						#print("CHECK ANSWER!!!"
						print("CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x[0])+", x_moduli: "+str(x_moduli[0]))
						answers_to_be_checked.append(str(g)+"_"+str(h)+"_"+str(p)+"_"+str(x[0]))	#O(1)
						sys.exit()

					return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, x_moduli[0], answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, q_e_nf_order_p_list, count_xi_not_found, count_calc_xi_status_false

			elif xi_found == False:
				#input("xi_found = False ! ")
				#Calc_xi method failed to find solutions - an xi was not found !
				#print("Calc_xi method failed to find solutions - an xi was not found ! "
				#x.append(0)
				x.append("No solns!")
				count_calc_xi_no_solns = count_calc_xi_no_solns + 1
				count_nosolns = count_nosolns + 1				#O(1)

				return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, q_e_nf_order_p_list, count_xi_not_found, count_calc_xi_status_false
			elif calc_xi_status == False:
				#input("calc_xi_status = False ! ")
				#Calc_xi method failed to find solutions - lhs=1 and rhs=1	
				#print("Calc_xi method failed to find solutions - calc_xi_status is false ! "
				x.append("No solns!")
				#x.append(0)
				count_calc_xi_no_solns = count_calc_xi_no_solns + 1
				count_nosolns = count_nosolns + 1				#O(1)
				#sys.exit()

				return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, q_e_nf_order_p_list, count_xi_not_found, count_calc_xi_status_false
			else:
				print("calc_xi_status is: "+str(calc_xi_status))
				print("xi_found is: "+str(calc_xi_status))
				input("Waiting for user..")
				#sys.exit()

				return x[0], count_nosolns, count_calc_xi_no_solns, count_normal_soln, 0, answers_to_be_checked, count_x_equals_0, count_needlargerprimelist, count_notprime, q_e_nf_order_p_list, count_xi_not_found, count_calc_xi_status_false

#def calc_order(g, p, count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, order_false_list, primes, n_prime, count_order_prime):

#def calc_order(g, p, count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, primes, n_prime, count_order_prime):

def calc_order(g, p, count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, primes, n_prime, count_order_prime, previous_calc_g_p):

	#print("Running calc_order("+str(g)+", "+str(p)+", ..)")
	#print("previous_calc_g_p:",previous_calc_g_p)
	#print("Need to calculate & check order for: "+str(g)+"_"+str(p)
	#print("Need to calculate & check order for: "+str(concat_g_p)					

	#use exponent function to get order of g mod p
	result = exponent_g_p(g, p)				#Worst: O(n + 7)	#Best: O(8)
	#return x, status
	#status is False for "no exponent found"	
	#status is True for exponent found
	order = result[0]					#O(1)
	status = result[1]					#O(1)
	#status = result[1]					

	#print("order is: "+str(order)
	#input("Waiting for user..")

	#sqrt_order=math.floor(math.sqrt(order))

	# Now want order = q**e, where q is prime
	# obtain q and e 
	if status == False:					#O(1)
		q=0							#O(1)
		e=0							#O(1)
		concat_order_p = str(order)+"_"+str(p)
		q_e_nf_order_p_list.append(concat_order_p)		#O(1)
		count_order_not_prime = count_order_not_prime + 1	#O(1)
		count_q_e_not_found = count_q_e_not_found + 1		#O(1)
		count_nosolns = count_nosolns + 1			#O(1)
		order_status = False
		lhs = 0
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, q, e, order_status, n_prime, count_order_prime, order, lhs
	elif order == 1:					#O(1)
		q = order						#O(1)
		e = 1							#O(1)
		print("q:",q,"e:",e,"g:",g,"p:",p,)
		#input("Order is 1! Waiting for user..")
		#print("order: "+str(order)
		#order_false_list.append(str(g)+"_"+str(p))
		concat_order_p = str(order)+"_"+str(p)
		q_e_nf_order_p_list.append(concat_order_p)
		count_order_not_prime = count_order_not_prime + 1	#O(1)
		count_q_e_not_found = count_q_e_not_found + 1		#O(1)
		count_nosolns = count_nosolns + 1			#O(1)
		#x_final = "No solns!"
		order_status = False
		#counts_added = True
		q = 0
		e = 0
		lhs = 0
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, q, e, order_status, n_prime, count_order_prime, order, lhs
	elif order in n_prime:				
		#print("order: "+str(order)+" is prime"
		q = order						#O(1)
		e = 1							#O(1)
		count_order_prime = count_order_prime + 1		#O(1)
		count_q_e_found = count_q_e_found + 1			#O(1)
		order_status = True
		lhs = pow(g,1,p)
		#counts_added = True
		#print("q: "+str(q)+", e: "+str(e)
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, q, e, order_status, n_prime, count_order_prime, order, lhs
	elif isprime(order) == True:				#O(sqrt(n))
		#True for prime
		#False for not prime
		#order is prime
		#print("order: "+str(order)+" is prime"
		n_prime.append(order)
		q = order						#O(1)
		e = 1							#O(1)
		count_order_prime = count_order_prime + 1		#O(1)
		order_status=True
		count_q_e_found = count_q_e_found + 1			#O(1)
		lhs = pow(g,1,p)
		#counts_added = True
		#print("q: "+str(q)+", e: "+str(e)
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, q, e, order_status, n_prime, count_order_prime, order, lhs

	else:
		#print("order is: "+str(order)+" - not 1 nor prime!"
		#input("Waiting for user..")
		#order is not 1 nor prime		
		count_order_not_prime = count_order_not_prime + 1	#O(1)

		#now check if order is of form q**e, where q is prime, e>=1. 
		#Need to find q and e.
					
		result = calc_q_e(primes, order, p)			#Worst: O(n**2+7n+4)	#Best: O(12)
		#return q, e, result

		q=result[0]						#O(1)
		e=result[1]						#O(1)
		order_status=result[2]					#O(1)
		#status=result[2]					
		#counts_added = False				
		#print("order_status is: "+str(order_status)

		if order_status == False:
			concat_order_p = str(order)+"_"+str(p)
			q_e_nf_order_p_list.append(concat_order_p)
			#order_false_list.append(str(g)+"_"+str(p))		#O(1)
			count_q_e_not_found = count_q_e_not_found + 1		#O(1)
			lhs = 0
			#counts_added = True
		elif order_status == True:
			lhs = pow(g,pow(q,e-1),p)
			count_q_e_found = count_q_e_found + 1			#O(1)
		else:
			print("order_status is: "+str(order_status))
			lhs = 0
			input("Waiting for user..")
			concat_order_p = str(order)+"_"+str(p)
			q_e_nf_order_p_list.append(concat_order_p)
		return count_nosolns, count_order_not_prime, count_q_e_found, count_q_e_not_found, q_e_nf_order_p_list, q, e, order_status, n_prime, count_order_prime, order, lhs
							
def calc_q_e(primes, order, p):
	#print("Running calc_q_e().."	
	#print("Running calc_q_e(primes, "+str(k)+", "+str(p)+").."

	#Worst: O(n**2+7n+4)	#Best: O(12)

	#q needs to be prime, e >= 1 
	#p is prime	

	result=False			#O(1)
	q=0				#O(1)
	e=0				#O(1)
	n=1				#O(1)
	#print("p is: "+str(p)
	
	#***********
	#"What should be used for calculating q & e - pow(prime,n) or pow(prime,n,p)??")***********

	for prime in primes:		#O(n)	#Worst: O(n**2+7n)	#Best: O(8)
		#print("=================="
		n = 1					
		#print("n is: "+str(n)+", order is: "+str(k) 		
		#print("prime is: "+str(prime)+", p is: "+str(prime)
		while result is False and prime < p and n <= order and pow(prime,n) <= order:	#O(n)	#Worst: O(n+7)	#Best: O(7)
			#print("-----------------"
			#print("n is: "+str(n)+", order is: "+str(order) 
			#print("prime is: "+str(prime)+", p is: "+str(p)
			#print("prime ** n is: "+str(prime**n)
			if pow(prime,n) == order:							#O(2)
				q = prime						#O(1)
				e = n							#O(1)
				result = True						#O(1)
				#print("result is: "+str(result)				
				break							#O(1)
			else:
				n = n + 1						#O(1)
	return q, e, result

def exponent_g_p(g, p):
	#print("Running exponent_g_p().."

	#Worst: O(n + 7)	#Best: O(8)

	n=1						#O(1)
	x=0						#O(1)
	status=False					#O(1)
	while n < p:					#O(n)	#Worst: O(n + 7)
		#print("n is:"+str(n)
		if pow(g,n,p) == 1:		#O(2)	#Worst: O(6)
			x = n				#O(1)
			status=True			#O(1)
			break				#O(1)
		elif pow(g,n,p) == -1:		#O(2)	#Worst: O(6)
			x = 2 * n			#O(1)
			status=True			#O(1)
			break				#O(1)
		n = n + 1				#O(1)

	if x==0:					#O(1)
		x="No exponent found"			#O(1)
		status=False				#O(1)

	return x, status

def a_exp_x_eq_r(a,p,r):
	#print("Running a_exp_x_eq_r("+str(a)+", "+str(p)+", "+str(r)+"..)"
	x=1
	x_values=[]
	count=0
	diff=0
	for x in range(0,2*p):
		#print("count is: "+str(count)		
		if pow(a,x,p) == r:
			#print("a**x % p is: "+str(r)
			x_values.append(x)
			#print str(x)+" appended to x_values"
			count=count+1
			if count==2:
				#print("count is: "+str(count)
				#print str(x)+" appended to x_values
				diff = x_values[1] - x_values[0]				
				#print("diff is: "+str(diff)
				break
		#x = x + 1
	return diff

def prop_234(g, h, qi, ei, p, count_xi_not_found, count_calc_xi_status_false, lhs):
	#print("-----------------------------------"
	#print("Running prop_234("+str(g)+", "+str(h)+", "+str(qi)+", "+str(ei)+", "+str(p)+"..) to solve for x..."
	
	#g[var], h[var], qi[var], ei[var], p
	#let x = x_0 +x_1*(q)+x_2*(q**2)+...+x_{e-1}q^(e-1), with 0 <= x_i < q, and determine successively x_0, x_1, x_2, ...

	#print("qi is: "+str(qi)
	#print("ei is: "+str(ei)

	# constuct list of q_powers from 0 to e-1
	q_powers=[]						#O(1)

	#when ei > 0: #worst: O(n+3)	#best: O(3)
	#when ei = 0: O(3)	
	#when ei not > 0 nor = 0: O(4)

	#first q_power will always be 1 (for k=0)
	if ei > 0:						#O(1)	#worst: O(n+3)	#best: O(1)
		for k in range(0,ei):					#O(n)
			q_powers.append(pow(qi,k))			#O(2)
			#q_powers.append(qi**k)
	elif ei==0:						#O(1)	#worst: O(3)
		print("ei = 0!")					
		sys.exit()					#O(1)

	else:							#O(1)	#worst: O(4)
		print("ei is: ",str(ei))
		sys.exit()					#O(1)

	#print("q_powers are: "+str(q_powers)

	#now want to calculate xi using function	
	result = calc_xi(q_powers, g, p, h, qi, ei, lhs)
	#return xi, calc_xi_status, xi_found	
	xi = result[0]
	calc_xi_status = result[1]
	xi_found = result[2]

	#Subtotal - Worst: O(n**2 + 7n + 3), Best: O(3) when calc_xi_status == False
	if calc_xi_status == False:
		count_calc_xi_status_false = count_calc_xi_status_false + 1
		#print("Calc_xi_status is false! - g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", qi: "+str(qi)+", ei: "+str(ei)
		x=0 						#O(1)
		M=0						#O(1)
		#input("Calc_xi method failed (lhs=rhs=1). Waiting for user..")
	elif xi_found == False:				#O(1)
		count_xi_not_found = count_xi_not_found + 1
		#print("An xi was not found! - g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", qi: "+str(qi)+", ei: "+str(ei)
		x=0 						#O(1)
		M=0						#O(1)
		#input("Calc_xi method failed (lhs=rhs=1). Waiting for user..")
	elif calc_xi_status == True and xi_found == True:		#O(1)	#Subtotal - Worst: O(n**2 + 7n + 2), Best: O(n+5) when only 1 as q_power
		#print("xi are: "+str(xi)

		#print("---------------------------"
	
		#print("q_powers are: "+str(q_powers)	
		for q_power in q_powers: 			#O(n)	#Worst: O(n**2 + 7n)	#Best: O(n+4) - when only 1 as q_power
			#print("q_power is: "+str(q_power)
			#print("index of q_power is: "+str(q_powers.index(q_power))
			#print("xi[(q_powers.index(q_power))] is: "+str(xi[(q_powers.index(q_power))])		
			a=xi[q_powers.index(q_power)] 							#O(n+1)
			if q_power==1: 									#O(1)
				#print("Adding "+str(xi[q_powers.index(q_power)])+" to x"
				x = a										#O(1)
				#x = xi[q_powers.index(q_power)]
			
			else:										#O(1)
				#print("Adding "+str(xi[(q_powers.index(q_power))])+"*"+str(q_power)+" to x, and reducing mod "+str(qi**ei)
				x = (x + a * q_power) % pow(qi,ei)					#O(4)
				#x = (x + xi[q_powers.index(q_power)]*q_power) % (pow(qi,ei))	
			
		M = pow(qi,ei)					#O(1)
		#print("x is: "+str(x)+" mod "+str(M))		
	else:
		print("calc_xi_status is: "+str(calc_xi_status))
		print("xi_found are: "+str(xi_found))
		input("Waiting for user..")

	return x, M, calc_xi_status, xi_found, count_xi_not_found, count_calc_xi_status_false

def calc_xi(q_powers, g, p, h, qi, ei, lhs):
	#print("---------------------------"			
	#print("Running calc_xi("+str(q_powers)+", "+str(g)+", "+str(h)+", "+str(qi)+", "+str(ei)+", "+str(p)+") .."				

	#initialise xi, cumul_q_powers, cumul_xi_q_powers
	xi = len(q_powers) * [0]				#O(len(q_powers))
	cumul_q_powers=[]					#O(1)
	cumul_xi_q_powers=[]					#O(1)
	calc_xi_status=True					#O(1)

	#Loop through each q_power until xi are calculated
	for q_power in q_powers:
		#print("q_power is: "+str(q_power)		
		if calc_xi_status == True:
			if q_power==1:							#total (incl top lev if) = 
				#solving for x_0		
				#print("---------------------------")			
				xi_found = False
				#print("Solving for xi[0] ..")				
				#print("q_power is: "+str(q_power))					
					
				#lhs= pow(g,pow(qi,ei-1),p)				#O(2)
				#lhs= (g**qi**(ei-1)) % p				
				#print("lhs is: "+str(lhs)) 		# lhs=76	
					
				rhs= pow(h,pow(qi,ei-1),p)				#O(2)
				#rhs= (h**qi**(ei-1)) % p				
				#print("rhs is: "+str(rhs)) 		# rhs=1		
			
				if lhs ==1 and rhs ==1:					#O(1)		#subtotal: O(2)	#section= O(2n+6)				
					#This method seems to fail for this instance. Try p-1/q method?? brute force search instead??				
					calc_xi_status=False				#O(1)

				else:							#O(1)		#Worst: O(4n+1)	#best: O(6)
					for t in range(0, qi):				#O(n)		#Worst: O(4n)	#best: O(5)
						if pow(lhs,t,p) == rhs:			#O(2)		#Worst: O(4)	#best: O(4)
						#if lhs**t % p ==rhs:					
							xi[0]=t  # xi[0]=		#O(1)
							xi_found = True
							#print("xi[0] is: "+str(t)	
							break				

				if calc_xi_status == True:				#O(1)		#subtotal= O(3)
					cumul_xi_q_powers.append(xi[0])			#O(1)
					cumul_q_powers.append(1)			#O(1)
					#print("cumul_xi_q_powers after append: "+str(cumul_xi_q_powers)
					#print("cumul_q_powers after append: "+str(cumul_q_powers)
			else:								#O(1)		#total (incl top lev if) = 
				#solving for x_n (n!=0)
				#print("---------------------------")			
				xi_found = False
				#print("solving for x_n (n!=0).."			
				#print("q_power is: "+str(q_power))			
				xi_number = q_powers.index(q_power)			#O(n)
				#print("Solving for xi["+str(xi_number)+"] ..")
				#print("cumul_xi_q_powers before append: "+str(cumul_xi_q_powers)
				#print("cumul_q_powers before append: "+str(cumul_q_powers)
			
				#print("g is: "+str(g) # g=
				#print("h is: "+str(h) # h=
				a = xi_number-1						#O(1)
				#print("xi["+str(a)+"] is: "+str(xi[a])) # xi[0]=0	
			
				#print("qi is: "+str(qi))	#qi = 
				#print("ei is: "+str(ei))	#ei = 
			
				#print("cumul_xi_q_powers is: "+str(cumul_xi_q_powers)	
				#print("cumul_q_powers is: "+str(cumul_q_powers)		
			
				z=0
				for cumul_xi_q_power in cumul_xi_q_powers:		#O(n+1)
					z = z + cumul_xi_q_power
				
				#print("sum_cumul_xi_q_power is now: "+str(z)		

				if xi[xi_number-1] >= 0:
					#need to work out what g**-[x_0+x_1*q_power+x_2*q_power**2 + ...], mod p is!!!
					#print("xi["+str(xi_number-1)+"] >= 0")
					#print("Calculating modular inverse of "+str(g)+"**"+str(-z)+", mod "+str(p))			
					#print("Calculating modular inverse of "+str(g)+"**"+str(-xi[xi_number-1])+", mod "+str(p))				
					b = calc_modinverse(g, z, p)									#O(n+5)
					#b = calc_modinverse(g, xi[xi_number-1], p) #b = 
					#print("inverse is: "+str(b)) #b = 								
				
					#(ei - xi_number - 1)

					#print("(h * b)**qi**(ei - xi_number - 1) % p is: "+str((h * b)**qi**(ei - xi_number - 1) % p)
					rhs = pow(h * b,pow(qi,ei - xi_number - 1),p)
					#rhs = (h * b)**qi**(ei - xi_number - 1) % p						#O(2n+2)			

					#print("rhs is: "+str(rhs))								

					if lhs == 1 and rhs == 1:									#O(1)	#Subtotal O(4)
						print("lhs == 1 and rhs == 1")								
						#print("xi["+str(xi_number-1)+"] >= 0, lhs=1, rhs=1, g: "+str(g)+" p: "+str(p)+" h: "+str(h))			
						calc_xi_status=False									#O(1)
						print("Calc_xi method failed. h is "+str(h)+", p is "+str(p)+", qi is "+str(qi)+", ei is "+str(ei)+", xi_number is "+str(xi_number))														#O(1)
						sys.exit()
					else:												#O(1)	#Subtotal O(n**2+5n+1)
						for t in range(0, qi):									#O(n)
							#print("t is now: "+str(t)					
							#print(str(lhs)+"**"+str(t)+" % "+str(p)+" is: "+str(lhs**t % p))
							if lhs**t % p == rhs:								#O(n+2)
								xi[xi_number]=t									#O(1)
								xi_found = True
								#print("xi["+str(xi_number)+"] is: "+str(t)					
								break										#O(1)

					if calc_xi_status == True:									#O(1)	#Subtotal O(n**2+5n+1)
						cumul_xi_q_powers.append(q_power * xi[xi_number])						#O(3)
						#print("Appended "+str(q_power * xi_number)+" to cumul_xi_q_powers")
						cumul_q_powers.append(q_power)									#O(1)
						#print("Appended "+str(q_power)+" to cumul_q_powers")
						#print("xi["+str(xi_number)+"] is: "+str(xi[xi_number]))
						#print("xi are now:"+str(xi)
						#print("cumul_xi_q_powers after append: "+str(cumul_xi_q_powers)
						#print("cumul_q_powers after append: "+str(cumul_q_powers)
				else:													#O(1)
					print("xi["+str(xi_number-1)+"] is negative !!! CHECK")							
					#input("Waiting for user..")										#O(1)
					sys.exit()												#O(1)
		
				#print("lhs is: "+str(lhs)
				#print("rhs is: "+str(rhs)

				#print("rhs is: "+str(rhs))
				#print("qi is: "+str(qi)
	return xi, calc_xi_status, xi_found

def calc_modinverse(g, power, p):
	#print("----------------"
	#print("Running calc_modinverse().."					#O(1)
	#print("g is: "+str(g)
	#print("power is: "+str(power)
	
	floor_sqrt_p = math.floor(math.sqrt(p))					#O(2)

	#this only works for p being prime!	
	if isprime(p) == True:							#O(1)	#Subtotal O(2n+4)
	#if isprime(p,floor_sqrt_p) == 0:	
		result=g**(p-2)% p						#O(n+2)	#Subtotal O(2n+3)
		#print str(g)+"**(-1) mod "+str(p)+" is: "+str(result)
		c = result**power % p						#O(n+1)
		#print("c is: "+str(c)	
		#print str(g)+"**(-"+str(power)+") mod "+str(p)+" is: "+str(c)
	else:
		#p is not prime!
		#print("p: "+str(p)+" is not prime!"
		c = modinv(g, p)						#O(n)
		#return x % m
		#print("inverse is: "+str(c)		

		#input("Waiting for user..")	
	return c

def calc_powers(factors):
	#Worst: O(n+13)	#Best: O(18)

	#print("Running calc_powers.."
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	powers = []						#O(1)
	fac_list = []						#O(1)
	count = 0						#O(1)
	c_primefactors_powers = 0				#O(1)
	s_before_calc_powers = time.clock()			#O(1)
	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if fac_list:						#O(1)	#Worst: O(n+2)	#Best: O(4)
			#temp factor list for comparisons has values
			if factor in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
				#print str(factor)+" is in fac_list"
				count += 1						#O(1)
				#print("count is: "+str(count)
				#temp_factor, temp_count = factor, count
				#print temp_factor, temp_count
			else:							#O(1)
				#factor is not in fac_list
				#add factor to prime_factors
				prime_factors.append(factor)				#O(1)
				#print("Added "+str(factor)+" to prime_factors"
				#print("prime_factors is: "+str(prime_factors)
				#add current count to powers for previous factor
				#print("count is: "+str(count)
				powers.append(count)					#O(1)
				#print("Added "+str(count)+" to powers for previous factor"
				#count = 0
				#print str(factor)+" is NOT in fac_list"
				#append it				
				fac_list.append(factor)					#O(1)
				#count += 1
				count = 1						#O(1)
				#print("count is: "+str(count)
				#print("fac_list is: "+str(fac_list)
				
		else:								#O(1)	#Subtotal: O(4)
			#temp factor list for comparisons is empty
			#store 1st factor
			#print("fac_list is empty"
			fac_list.append(factor)						#O(1)
			#print str(factor)+" added to fac_list"
			prime_factors.append(factor)					#O(1)
			#print("Added "+str(factor)+" to prime_factors"
			#print("prime_factors is: "+str(prime_factors)			
			count += 1							#O(1)
			#print("count is: "+str(count)	

	#add count to powers for the last factor and the last factor
	powers.append(count)
	#print("Added "+str(count)+" to powers for previous factor"
	
	#print("prime_factors are: "+str(prime_factors)
	#print("powers are: "+str(powers)

	c_calc_powers = time.clock() - s_before_calc_powers

	return prime_factors, powers, c_calc_powers

def csvfile_store_primes(csv_filename_var):		### Assumming O(n+len(z1)+1) ### 
		
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
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

	#print("Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	factors = []					#O(1)

	#print("Calculating prime factors and powers"
	s_before_factorisations = time.clock()		
		
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

	return factors, c_factorisations		#O(1)

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()

def egcd(a, b):							#O(n)
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print("a is: "+str(a)
	#print("b is: "+str(b)	
	if a == 0:						#O(1)	#Subtotal: O(2)
		return (b, 0, a)				#O(1)
	g, y, x = egcd(b % a, a)				
	#print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
	return (g, x - (b//a) * y, y)

def modinv(a, m):						#### O(n+5) ###
	#print("Running modinv("+str(a)+","+str(m)+")")		
	#print("a is: "+str(a)
	#print("m is: "+str(m)	
	#egcd(a, m)
	g, x, y = egcd(a, m)					#O(n)
	if g != 1:							#O(1)	#Subtotal: O(2)
		raise Exception('No Modular Inverse') 			#O(1)
	#print(str(a)+"**(-1) mod "+str(m)+" is: "+str(x % m))	
	return x % m						#O(1)

