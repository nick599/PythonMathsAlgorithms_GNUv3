#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 6. 19/04/2018.
#Programmed & tested in Python 3.4 only
#This program attemps to solve a Discrete Log Problem (DLP) specified by user, via Polig-Helman Algorithm via factorisation of (p-1) where p is a prime number. 
#Results printed are three arrays ...
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

import sys
import math
import os
import itertools
import csv
import time

python_version = sys.version

print(python_version)

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version 6. 19/04/2018.")
print("Programmed & tested in python 3.4 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via Polig-Helman Algorithm via factorisation of (p-1) where p is a prime number")
print("Results printed are three arrays ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")

def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	print("primefile currently is: ",primefile)

	#define prime list
	#print('Importing primes from csv file')
	primes = csvfile_store_primes(primefile)
	#print('First ten primes are: '+str(primes[0:10]))

	#print(sys.version_info)

	#initialise g_values, p_values, and h_values
	
	g_values = range(2,4)
	#g_values = range(2,20)
	p_values = primes[0:101]
	#h_values = range(2,201)

	total_g_values=len(g_values)
	print("total_g_values: ",total_g_values)

	total_p_values=len(p_values)
	print("total_p_values: ",total_p_values)

	#need formulae for sum of first n prime numbers !	
	#print("need formulae for sum of first n prime numbers !")
	#input("Waiting for user..")

	sum_primes=0
	for p in p_values:
		sum_primes = sum_primes + p		

	print("Sum of primes in p_values is:",sum_primes)

	#total_h_values is the sum of (p[0]-1) + (p[1]-1) + ... + (p[n-1]-1) = sum(primes) - (number of primes)
	total_h_values = sum_primes - total_p_values	

	#total_h_values = total_p_values - 1
	#total_h_values=len(h_values)
	#print("total_h_values: "+str(total_h_values)

	#Total_values = total_p_values * total_g_values
	Grand_total_values = total_p_values * total_g_values * total_h_values
	#print("Total_values "+str(Total_values)
	print("Grand_total_values:",Grand_total_values)
	
	#percent_thresholds=[]	
	#percent_thresholds[1]=total_values / 10
	#for x in range(2,11):
	#	percent_thresholds[x] = x * percent_thresholds[1]
	#print("percent_thresholds: "+str(percent_thresholds)

	#define lists for different types of results
	answers_to_be_checked=[]
	n_prime=[]
	#q_e_nf_order_p_list=[]

	#define counts for different types of results
	count_nosolns=0
	count_x_equals_0=0
	count_normal_soln=0
	count_needlargerprimelist=0
	count_notprime=0
	count_zi_bi_equal_1=0
	count_bi_equal_1_zi_ntequal_0_1=0
	count_Bi_equals_zi=0
	count_x_status_false = 0

	print("======================================")

	print("Looping through values for g, p, & h..")

	for g in g_values:
		print("======================================")
		print("g is: ",g)
		for p in p_values:
			#print("--------------------------------------")
			p_position = p_values.index(p)
			if p_position % 50 == 0:
				print("index of p: ",p_position)
			#print("p is: ",p)		
			#no_prim_roots = p - 1 #for F_p this is euler_phi(p) = p-1 since p is prime.			
			h_soln_alreadyfound = False
			#concat_g_p = str(g)+"_"+str(p)
			#print("concat_g_p is: ",concat_g_p)			
			if g == p:
				#print("Value of g: "+str(g)+" equals value of p: "+str(p)+". Check count_nosolns!"
				#input("Waiting for user..")
				count_nosolns = count_nosolns + len(range(1,p))	
			else:				
				#print("g_p is: ",g+"_"+p)
				
				#Want to calculate and store group G				
				G_list = []				
				for number in range(1, p):
					a = pow(g,number,p)
					if a not in G_list:					
						G_list.append(a)
					else:
						#print("a: ",a," is in G_list")						
						break

					#print("pow("+str(g)+","+str(number)+","+str(p)+") is: "+str(pow(g,number,p))
					#G_list.append(pow(g,number,p))
				
				#print("G_list is: "+str(G_list)
				#input("Waiting for user..")

				for h in range(1, p):								
					#concat_g_h = str(g)+"_"+str(h)
					#print("-----------------------------------"
					#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)
					
					#check if h is in G generated by g 
					if h not in G_list:
						#print("h: "+str(h)+" is not in Group G. Hence no solutions!"
						count_nosolns = count_nosolns + 1
						#sys.exit()	 

					elif h >= p:
						#print("Setting h_soln_alreadyfound to true.."
						h_soln_alreadyfound = True							
						break													
					
					elif g == h:
						x_final = 1
						#x_final = int(x_final)
						x_moduli_final = p - 1
						x_to_print = str(x_final)+" mod "+str(x_moduli_final)
	
						#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", x: "+str(x_final)							
	
						#Check answers
						if pow(g, x_final, p) != h:
						#if pow(g, x_final, p) != h:
							print("CHECK x_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
							#print("CHECK x_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli_final: "+str(x_moduli_final)
							input("Waiting for user..")

						elif pow(g, x_final+x_moduli_final, p) != h:
						#elif pow(g, x_final+x_moduli_final, p) != h:
							print("CHECK x_moduli_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
							#print("CHECK x_moduli_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli_final: "+str(x_moduli_final)
							input("Waiting for user..")					
					else:
						result = dlp(g, p, h, primefile, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked)

						#return x_final, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status

						#print("return back to h_values loop.."								

						x_final = result[0]
						count_nosolns = result[1]
						count_normal_soln = result[6]
						x_moduli_final = result[7]
						#answers_to_be_checked.append(result[5])
						count_x_equals_0 = result[4]
						#count_needlargerprimelist = result[7]
						#count_notprime = result[8]
						x_status=result[9]
					
						#print("x_status is: "+str(x_status)
						#print("count_nosolns after dlp(): "+str(count_nosolns)
						#print("x_final is: "+str(x_final)
						#print("x_moduli_final is: "+str(x_moduli_final)
						
						if x_status == True:
							if x_final != "No solns!":
							#if x_final != "No solns!":						
								#print("x_final != No solns!"
								x_to_print = str(x_final)+" mod "+str(x_moduli_final)
								#input("Waiting for user..")						

							#Check answers
							checks_fail = False							
							if pow(g, x_final, p) != h:
								checks_fail = True
								print("CHECK x_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
								#print("CHECK x_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli_final: "+str(x_moduli_final)
								#input("Waiting for user..")

							elif pow(g, x_final + x_moduli_final, p) != h:
								checks_fail = True
								print("CHECK x_moduli_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
								#print("CHECK x_moduli_final! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)+", x_moduli_final: "+str(x_moduli_final)
								#input("Waiting for user..")

							for number in (1, x_moduli_final):
								a = pow(g, x_final + number, p)
								#print("number is: "+str(number)+", pow("+str(g)+", "+str(x_final)+" + "+str(number)+", "+str(p)+") is: "+str(a)								
								if a == h and number < x_moduli_final:
									checks_fail = True
									print("CHECK x_moduli_final! - smaller x_moduli found! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final)
									#print("CHECK x_moduli_final! - smaller x_moduli found! g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x_final: "+str(x_final)
									#input("Waiting for user..")

							if checks_fail != False:
								print("*** 1 or more Checks FAILED! ***")
								input("Waiting for user..")

							#print("*** Checks Passed! ***"
						else:
							count_x_status_false = count_x_status_false + 1
						

	print("Grand total combinations considered: ",Grand_total_values,", total_g_values: ",total_g_values,", total_p_values: ",total_p_values,", total_h_values: ",total_h_values,", number_no_solns: ",count_nosolns,", largerprimelist: ",count_needlargerprimelist,", count_x_status_false: ",count_x_status_false)

	#print("Grand total combinations considered: "+str(Grand_total_values)+", total_g_values: "+str(total_g_values)+", total_p_values: "+str(total_p_values)+", total_h_values: "+str(total_h_values)+", number_no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_x_status_false: "+str(count_x_status_false)

	#print("Total values considered: "+str(Total_values)+", total_g_values: "+str(total_g_values)+", total_p_values: "+str(total_p_values)+", total_h_values: "+str(total_h_values)+", number_no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_q_e_found: "+str(count_q_e_found)+", count_q_e_not_found: "+str(count_q_e_not_found)+", count_order_prime: "+str(count_order_prime)+", count_order_not_prime: "+str(count_order_not_prime)+", count_xi_not_found: "+str(count_xi_not_found)+", count_calc_xi_status_false: "+str(count_calc_xi_status_false)

def ghp_checks(g, p, h, floor_sqrt_p, count_notprime):

	#print("Running ghp_checks().."

	status=1
	
	#Need to check if p is prime
	#print('Checking if p is prime ..')
	a = isprime(p)	
	#return True for prime, False for not prime
	if a == False:
		print("The number entered for p: ",p," is not prime. Please choose a number that is prime for p.")
		#print("The number entered for p: '+str(p)+' is not prime. Please choose a number that is prime for p.")
		status=0
		count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	#print('Running simple checks on g..')
	if (g==0 or h==0 or p==0):
		print("One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.")
		#print('One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.')
		status=0
		sys.exit()
	elif g==1:
		print("g = 1 has trivial solutions for the dlp. Please choose another number.")
	elif g<0:
		print("Number for g is negative. Please enter another number")
		status=0
		sys.exit()	
	
	return status

def chinese_remainder(x, x_moduli):
	#print("Running chinese remainder("+str(x)+","+str(x_moduli)+").."	
	#print("x are: "+str(x)
	#print("x_moduli are: "+str(x_moduli)
	#cong=[]
	cong_x=[]
	cong_moduli=[]
	x_new = 0
	M = 0
	a = 0
	b = 0
	for number in range(0,len(x)):
		#print('--------------------')
		#print("number is: "+str(number)		
		#store values in 1st congruence	
		a= x[number]
		#print("x[number] is: "+str(a)
		b= x_moduli[number]
		if b!=1:		
			if not cong_x:
				#cong has no elements
				#Add values in first congruence			
				#print("Appending info from 1st congruence"
				cong_x.append(a)
				x_new = a		
				cong_moduli.append(b)
				M = b			
				#cong.append(1)
			else:
				#print('--------------------')
				#cong_x has elements
				#print("Working on congruence number: "+str(number+1)
				#print("cong_x["+str(number-1)+"] is: "+str(cong_x[number-1])
				#print("cong_moduli["+str(number-1)+"] is: "+str(cong_moduli[number-1])
				#Subtract current cong_x[number-1] from current x[number]
				#print("Subtracting cong_x["+str(number-1)+"] from current x["+str(number)+"].."
				c = x[number] - cong_x[-1]
				#print("c now is: "+str(c)				#c=
			
				#print("cong_moduli["+str(number-1)+"] to use in inverse is: "+str(cong_moduli[number-1]) 
				#number=
				#print("x_moduli[number] to use in inverse is: "+str(b)			#moduli=

				#now want to find (cong_moduli[number-1]**-1) mod(b)		
				f = calc_modinverse(cong_moduli[-1], 1, b)
				#print("inverse (f) is: "+str(f) 			#inverse=

				#now take c and times it by the inverse, f, and reduce mod b
				#print("c*f is: "+str(c*f)
				#print("b is: "+str(b)
				k = (c*f) % b			
				#print("k is: "+str(k)

				#now take value of k and use it to work out new value of x
				#print("cong_x[-1] is: "+str(cong_x[-1])
				#print("cong_x[number-1] is: "+str(cong_x[number-1])
				#print("cong_moduli[-1] * k is: "+str((cong_moduli[-1] * k))
				#print("cong_moduli[number-1] * k is: "+str((cong_moduli[number-1] * k))
				x_new = cong_x[number-1] + (cong_moduli[number-1] * k)
				
				#if g > 2:
				#print("x_new is: "+str(x_new)
				
				cong_x.append(x_new)
			
				#now work out value of M
				M = cong_moduli[-1] * b
				#print("M is now: "+str(M)
				cong_moduli.append(M)
	return x_new, M


def isprime(p):		#this is O(sqrt(n))
	
	#print("Running isprime("+str(p)+").."
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	return True	

def prim_root(g,p,primes):

	#print("Running prim_root("+str(g)+", "+str(p)+", primes).."

	#print('Checking if '+str(g)+' is a primitive root mod '+str(p)+' ..')
	status = True
	check = 0	
	ep = euler_phi_primesused(p)
	#return a	
	#ep=result[0]
	#print("euler_phi("+str(p)+") is: "+str(ep)

	factors = factorise(ep)	
	#result1 = factorise(ep)	
	#return factors, c_factorisations
	#factors = result1[0]
	#c_factorisations = result1[2]

	#print("factors of ep("+str(p)+") are: "+str(factors)
	#print("type(factors) is: "+str(type(factors))
	
	result2 = calc_primefactors_powers(factors, ep)
	#return prime_factors, powers, c_calc_powers		
	prime_factors = result2[0]
	powers = result2[1]
	#c_calc_powers = result2[2]

	#print("prime_factors are: "+str(prime_factors)
	power=1

	#Do we need to check prim roots now???
	for prime in prime_factors:		
		if status==True:
			#print("================="
			#print("prime is: "+str(prime)
			power=1
			power_index = 0
			#print("power_index is: "+str(power_index)
			while power < powers[power_index]:
				#print("------------------"
				#print("power is: "+str(power)			
				if pow(g,ep / pow(powers[power_index],power),p) == 1:
					status=False	
					#print("Status is False!"				
					break
				power = power + 1
			power_index = power_index + 1

	return status, prime_factors, powers

def euler_phi_primesused(n):				
	
	#when n is not prime
	# Worst: O(sqrt(n)+8)  
	# Best:	O(4) when n=1

	#when n is prime
	#O(sqrt(n)+5) 
	
	#print("Running euler_phi_primesused("+str(n)+", primes).."
	
	#print("isprime_result is: "+str(isprime_result)

	#left_isprime_result=left()

	#status = True 					#O(1)
	#floor_sqrt_n = math.floor(math.sqrt(n))

	#print("isprime(n) is: "+str(isprime(n)
	#print("isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#status=1 for not prime
	#status=0 for prime

	if n==1:					#O(1)	#subtotal O(3)
		a = 1					#O(1)
		#status = False						
		return a				#O(1)
		#return a, status			
			
	elif isprime(n)==True:
		return n-1
	else:							#subtotal O(???)
		#euler_phi(p**k) = (p-1)*p**(k-1) for prime p 
		#euler_phi(m*n) = euler_phi(m)*euler_phi(n) for coprime m & n

		#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.
		#n = p_1**(k_1)*p_2**(k_2)*p_3**(k_3)... , where p_i are prime factors of n, and k_i are corresponding powers.
		#n, and P_i are known 
		#need primes from factorise()!
				
		factors = factorise(n)					#O(sqrt(size(n)))
		#return 		


		#print("factors of "+str(n)+" are: "+str(factors)
		prime_factors = calc_primefactors_nopowers(factors) 	#O(???)		#Best operations: ??? 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		
		#print("prime factors are: "+str(prime_factors)
		
		len_prime_factors = len(prime_factors)

		#initialise ep
		ep=n
		#print("ep initialised as: "+str(ep)

		#print("prime_factors are: "+str(prime_factors)

		for prime in prime_factors:			#O(prime_factors)
			#now calculate first (1-1/p) for p|n
			#print("prime is: "+str(prime)
			#print("1 / float(prime) is: "+str(1 / float(prime))
			#print("1 / prime is: "+str(1 / prime)
			term = 1 - 1 / float(prime)
			#print("term is: "+str(term)
		
			#recalculate ep
			ep = ep * term
			#print("ep is now: "+str(ep)

		ep = int(ep)
		#print("final ep is: "+str(ep)

		#input("Waiting for user...")		

		#status = True				#O(1)
		return ep				#O(1)
		#return ep, status

def check_answer(g, p, h, x):
	status=True	
	if pow(g,x,p) != h:
		#print("CHECK ANSWER!!!"
		#answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))
		status=False
		
	return status	

def dlp(g, p, h, primefile, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked):	

	#print("--------------------"
	#print("Running dlp("+str(g)+", "+str(p)+", "+str(h)+"..)"

	floor_sqrt_p = int(math.floor(math.sqrt(p)))
	#print("floor_sqrt_p is: "+str(floor_sqrt_p)"

	#Run checks on g, h & p	
	count_notprime = 0
	#result=ghp_checks(g, p, h, floor_sqrt_p, count_notprime) 

	#if result == 0:
	#	sys.exit()

	#define prime list
	#print('Importing primes from csv file')
	primes=csvfile_store_primes(primefile)
	#print('First ten primes are: '+str(primes[0:10]))

	#check if sqrt_p > largest element in primes
	#print('checking if square root of p > largest element in primes...')
	sqrt_p = math.sqrt(p)
	largest_prime = primes[-1]
	count_needlargerprimelist=0
	if sqrt_p > largest_prime:
		print("Square root of p - ",sqrt_p," is greater than largest prime in list - ",largest_prime,". Consider using a larger prime list. Exiting..")
		#print("Square root of p - "+str(sqrt_p)+" is greater than largest prime in list - "+str(largest_prime)+". Consider using a larger prime list. Exiting.."
		count_needlargerprimelist = count_needlargerprimelist + 1
		sys.exit()

	#define counts for different types of results
	count_nosolns=0
	count_gi_hi_equal_1=0
	count_gi_equal_1_hi_ntequal_0_1=0
	count_x_equals_0=0
	count_gi_equals_hi=0
	count_normal_soln=0
	count_diffeq0=0
	
	#Check if g is a primitive root mod p
	count_primroot=0
	result=prim_root(g,p,primes)

	#1st step: calculate p-1 from p
	#p_minus_1 = p-1
	#print('p-1 is: '+str(p-1))	

	#2nd step: factorise p_minus_1 into product of prime powers
	status=result[0]
	prime_factors=result[1]
	powers=result[2]
	#moduli=result[3]

	#print("prime_factors is: "+str(prime_factors)
	#print("powers is: "+str(powers)

	if result is False:
		print(g,' is not a primitive root mod ',p,'! Exiting ...')
		#print(str(g)+' is not a primitive root mod '+str(p)+'! Exiting ...')		
		sys.exit()
	else:
		#print(str(g)+' is a primitive root mod '+str(p))	
		count_primroot = count_primroot + 1

		#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

		primes_list=prime_factors

		#print('primes for factorisation of p-1 are:'+str(prime_factors))
		#print('powers for factorisation of p-1 are:'+str(powers))
	
		#################################################
		# Polig-Helman Algorithm
		result_polig = polig_helman(primes_list, powers, g, p, h, count_nosolns, count_gi_hi_equal_1, count_diffeq0, count_x_equals_0, count_gi_equal_1_hi_ntequal_0_1, count_normal_soln, count_gi_equals_hi, count_gi_hi_equal_1)
	
		#return x, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status		

		x = result_polig[0]
		x_moduli = result_polig[7]
		x_status = result_polig[9]

		if x_status == False:
			#print("Polig helman method failed for g: "+str(g)+", p: "+str(p)+", h: "+str(h)
			#input("Waiting for user..")
			return 0, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, 0, count_diffeq0, x_status, count_needlargerprimelist
		elif x_status == True:
			#print('========================')
			#print("x's are: "+str(x)
			#print("x_moduli are: "+str(x_moduli)

			#print('========================')
			#now need to combine x's and x_moduli via CRT
			#print('Running chinese remainder..')
			result = chinese_remainder(x, x_moduli)
			x_final = result[0]
			x_moduli_final = result[1]
		
			#print('After CRT - x\'s are: '+str(x))
			#print('After CRT - x_moduli are: '+str(x_moduli))

			#print("x_final is: "+str(x_final)
			#print("x_moduli_final is: "+str(x_final)
			
			return x_final, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status, count_needlargerprimelist

		else:
			input("Waiting for user..")
			print("x_status is: ",x_status)
			#print("x_status is: "+str(x_status)
			return x_final, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status, count_needlargerprimelist


def polig_helman(primes_list, powers, g, p, h, count_nosolns, count_gi_zi_equal_1, count_diffeq0, count_x_equals_0, count_gi_equal_1_hi_ntequal_0_1, count_normal_soln, count_gi_equals_hi, count_gi_hi_equal_1):

	#count_gi_hi_equal_1

	#print("Running polig-helman ("+str(primes_list)+", "+str(powers)+", "+str(g)+", "+str(h)+", "+str(p)+", count_nosolns, count_gi_hi_equal_1, count_diffeq0, count_x_equals_0, count_gi_equal_1_hi_ntequal_0_1, count_normal_soln, count_gi_equals_hi)"	

	p_minus_1 = p-1

	#3: Calculate C - number of unique primes in factorisation (also is number of congruences to solve)
	C=0
	for prime in primes_list:
		C = C + 1		
	#print('Number of primes in primes_list = C = '+str(C))

	#4: Need to create a list (with C elements) for each of: q_i, e_i, W, g_i, h_i, z_i, & V_i 
	C_list=list(range(1,C+1))
	#print('C_list is: '+str(C_list))

	#5: initialise lists and values
	qi=[]
	ei=[]
	Wi=[]
	gi=[]
	hi=[]
	x=[] 
	x_moduli=[]
	i = 0
	x_status = True

	#6: loop through each C calculating values & storing them
	for C in C_list:
		#print("-------------------"
		#print("current C is:"+str(C)
		#print("i is: "+str(i)
		#print("primes_list["+str(i)+"] is "+str(primes_list[i])
		qi.append(primes_list[i])
		#print("type(qi) is: "+str(type(qi))
		#print("qi["+str(i)+"] is: "+str(qi[i])
		#print("type(ei) is: "+str(type(ei))
		ei.append(powers[i])
		#print('ei['+str(i)+'] is: '+str(ei[i]))
		Wi.append(p_minus_1 / pow(qi[i],ei[i]))	
		#Wi.append(p_minus_1 / (qi[i]**ei[i]))		
		
		gi.append(pow(g,Wi[i],p))
		#print('gi['+str(i)+'] is: '+str(gi[i]))
		#Bi.append(gi[i] % p)
		#print('Bi['+str(i)+'] = gi['+str(i)+'] % p is: '+str(Bi[i]))
		
		hi.append(pow(h,Wi[i],p))
		#print('hi['+str(i)+'] is: '+str(hi[i]))
		#zi.append(hi[i] % p)
		#print('zi['+str(i)+'] = hi['+str(i)+'] % p is: '+str(zi[i]))
	
		#7: Now Bi[i]**x = zi[i] mod p for each i
		# Need to solve for x for each.
		
		#print('i is: '+str(i))
		#print('qi['+str(i)+'] is: '+str(qi[i]))
		#print('ei['+str(i)+'] is: '+str(ei[i]))	
		#print("gi[i] is: "+str(gi[i])
		#print("hi[i] is: "+str(hi[i])
		
		init_moduli = p
		#print("init_moduli is: "+str(init_moduli)

		#print('Solving for x...')
		
		#print('Checks done and trivial solutions not found.') 
			
		#now x = a mod (qi**ei) is a solution where a is unknown
		
		if gi[i] == 1 and hi[i] == 1:
			x_status = False
			#print("gi["+str(i)+"] is: "+str(gi[i])+", hi["+str(i)+"] is: "+str(hi[i])
			break
			
			#input("Waiting for user..")
		
		elif gi[i] == 1 and hi[i] != 1:
			x_status = False
			#print("gi["+str(i)+"] is: "+str(gi[i])+", hi["+str(i)+"] is: "+str(hi[i])
			break
		else:
			#need to check all x s.t 0 <= x < qi**ei 
			#start with init_moduli. If an exponent is not found then consider prime powers from qi**ei to qi**1 in turn
			
			result = exponent_g_n(gi[i], hi[i], init_moduli)
			#return x, status, moduli		
			status = result[1]			
			#status = False for no exponent found

			#print("exponent_g_n status is: "+str(status)

			if status == False:
				#print("Exponent not found for init_moduli: "+str(init_moduli)
				#Exponent is not found for init moduli. Hence consider prime powers from qi**ei to qi**1 in turn
			
				ei_init = ei[i]
				#print("ei_init is: "+str(ei_init)
				while ei_init >= 1:
					#print("---------------------------"	
					#print("ei_init now is: "+str(ei)
					moduli = pow(qi[i],ei_init)
					#moduli = qi[i]**ei
					#print("Moduli to try is: "+str(moduli)			
					result = exponent_g_n(gi[i], hi[i], moduli)
					status = result[1]			
					#status = False for no exponent found
					if status == True:
						#diff=qi[i]**ei
						#print("Moduli found: "+str(moduli)
						x_moduli.append(moduli)
						break
					else:				
						ei_init = ei_init - 1

				#print("moduli is: "+str(moduli)			
				#input("Do we need moduli not empty??")	
			else:
				#Exponent & Moduli found
				x.append(result[0])
				#print str(result[0])+" appended to x"	
				x_moduli.append(result[2])
				#print str(result[2])+" appended to Moduli"

				#diff = a_exp_x_eq_r(gi[i], init_moduli, hi[i]) #a_exp_x_eq_r(g, p, r):
				#if diff==0:
				#	print 'Diff = 0 - No Solutions!!!'
				#	count_diffeq0 = count_diffeq0 + 1
				#	count_nosolns = count_nosolns + 1
				#	sys.exit()
				#else:
				#	x_moduli.append(diff)
				#	#print str(diff)+" appended to x_moduli"			
				#	count_normal_soln = count_normal_soln + 1
			i = i + 1

	return x, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli, count_diffeq0, x_status

def exponent_g_n(generator, h_value, p):

	#print("-------------------------------------------------"	
	#print("Running exponent_g_n("+str(generator)+", "+str(h_value)+", "+str(p)+")"	
	n = 1
	x = 0
	moduli = 0
	status = False
	while n < p:
		#print("n is:"+str(n)+" , generator**n % p is: "+str(pow(generator,n,p))
		if pow(generator, n, p) == h_value:
			x = n
			#print("x is: "+str(x)
			#print("p is: "+str(p)
			status = True
			for number in range(x+1, 2*p):
				if pow(generator, number, p)== h_value:
					moduli = number - x
					#print("moduli is: "+str(moduli)
					break
			break
		n = n + 1

	if status == False:
		x = "No exponent found"
		#status=False
		moduli = 0

	return x, status, moduli 

def a_exp_x_eq_r(g, p, r):
	#print("Running a_exp_x_eq_r("+str(g)+", "+str(p)+", "+str(r)+").."
	x=1
	x_values=[]
	count=0
	diff=0
	for x in range(0,p):
		#print("count is: "+str(count)		
		if pow(g,x,p) == r:
			#print("pow(g,x,p) is: "+str(r)
			#print("g**x % p is: "+str(r)
			x_values.append(x)
			#print str(x)+" appended to x_values"
			count=count+1
			if count==2:
				#print("count is: "+str(count)
				#x_values.append(x)
				#print str(x)+" appended to x_values
				diff = x_values[1] - x_values[0]				
				#diff = answer2 - answer1
				#print("diff is: "+str(diff)
				break
	return diff

def calc_modinverse(g, power, p):
	#print("----------------"
	#print("Running calc_modinverse("+str(g)+", "+str(power)+", "+str(p)+").."	
	#print("g is: "+str(g)
	#print("power is: "+str(power)
	#input("Waiting for user..")	

	#print("p is: "+str(p)
	
	#floor_sqrt_p = math.floor(math.sqrt(p))

	#this only works for p being prime!	
	if isprime(p) == True:	
		result=pow(g,p-2,p)
		#result=g**(p-2)% p
		#print str(g)+"**(-1) mod "+str(p)+" is: "+str(result)
		c = pow(result,power,p)
		#c = result**power % p
		#print("c is: "+str(c)	
		#print str(g)+"**(-"+str(power)+") mod "+str(p)+" is: "+str(c)
	else:
		#p is not prime!
		#print("p: "+str(p)+" is not prime!"
		c = modinv(g, p)
		#return x % m
		#print("inverse is: "+str(c)		

		#input("Waiting for user..")	
	return c

def csvfile_store_primes(csv_filename_var):

	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		primes=list(z1)
		csvfile.close()	
	return primes

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print("Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.clock()	
	factors = []					#O(1)
	#c_lists = time.clock() - s_before_lists

	#print("Calculating prime factors and powers"
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

	#print("factors are: "+str(factors)
	#print("c_factorisations are: "+str(c_factorisations)

	#input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors		#O(1)
	#return factors, c_factorisations		

def calc_primefactors_nopowers(factors):
	#Worst: O(n+13)	#Best: O(18)

	#print("Running calc_primefactors.."
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	#powers = []						#O(1)
	fac_list = []						#O(1)
	#c_primefactors = 0				#O(1)
	#s_before_calc_primefactors = time.clock()			#O(1)
	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if factor not in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
			prime_factors.append(factor)				#O(1)
			fac_list.append(factor)					#O(1)
		else:								#O(1)	#Subtotal: O(4)
			fac_list.append(factor)						#O(1)	
			
	#print("prime_factors are: "+str(prime_factors)
	
	#c_calc_primefactors = time.clock() - s_before_calc_primefactors

	return prime_factors
	#return prime_factors, c_calc_primefactors

def calc_primefactors_powers(factors, N):
	#print("------------------"
	#print("Running calc_primefactors_powers("+str(factors)+", "+str(N)+").."
	
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]
	fac_list = []
	#c_calc_primefactors = 0
	#s_before_primefactors = time.clock()	
	for factor in factors:		
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if factor not in fac_list:
			prime_factors.append(factor)
			fac_list.append(factor)					
		else:
			fac_list.append(factor)
			
	#prime_factors = fs
	#print("prime_factors are: "+str(prime_factors)
	#prime_factors.append(factor)
	#print("Added "+str(factor)+" to prime_factors"
	
	#print("prime_factors are: "+str(prime_factors)
	#c_calc_primefactors = time.clock() - s_before_primefactors

	powers = []
	#s_before_calc_powers = time.clock()
	for prime_factor in prime_factors:
		count = 0
		while N % prime_factor == 0:
			count = count + 1
			N = N / prime_factor		
		else:
			powers.append(count)
				
	#print("powers are: "+str(powers)
	#c_calc_powers = time.clock() - s_before_calc_powers

	#input("Waiting for user..")	

	return prime_factors, powers
	#return prime_factors, powers, c_calc_primefactors, c_calc_powers

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number > 2 * pow(10,8):
		print("Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..")
		#print("Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues.."
		sys.exit()

def egcd(a, b):
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print("a is: "+str(a)
	#print("b is: "+str(b)	
	if a == 0:
		#print("STOPPING since a is 0."
		return (b, 0, 1)
	g, y, x = egcd(b % a, a)
	#print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
	return (g, x - (b//a) * y, y)

def modinv(a, m):
	#print("Running modinv("+str(a)+","+str(m)+")")	
	#print("a is: "+str(a)
	#print("m is: "+str(m)	
	#egcd(a, m)
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('No Modular Inverse') 
	#print("x mod m is: "+str(x % m))	
	return x % m

if __name__=='__main__':
	main()

#def MaxPower(i,N_remainder):
#	m=0
#	while N_remainder > 1 and not N_remainder % i:	
#		m += 1		
#		N_remainder //= i
#	return m

#def max_element_below_or_equal_target(List,target):
#	if target in List:
#		return List.index(target)
#	elif target > List[-1]:
#		#Target value is not in list. Return index of last number in list.
#		return List.index(List[-1])
#	elif target < List[-1]:
#		#Target value is less than largest prime in list
#		# start from 2 and increase until last number is found that is less than target.
#		i=0
#		while List[i] < target:
#			i = i + 1 
#		return i
#	else:
#		print 'List[-1] is: '+str(List[-1])
#		print 'target is: '+str(target)	
#		print("Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))
#		return "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))

#print("What is g?"
	#g_initial = input()
	#if g_initial.isdigit() is False:
	#	print("You have not entered a positive integer for g. g is: "+str(g_initial)+". Please reenter."
	#	sys.exit()

	#now convert g into a long:
	#g = long(g_initial)

	#print("What is h?"
	#h_initial = input()
	#if h_initial.isdigit() is False:
	#	print("You have not entered a positive integer for h. h is: "+str(h_initial)+". Please reenter."
	#	sys.exit()

	#now convert h into a long:
	#h = long(h_initial)

	#print("What is p?"
	#p_initial = input()
	#if p_initial.isdigit() is False:
	#	print("You have not entered a positive integer for p. p is: "+str(p_initial)+". Please reenter."
	#	sys.exit()

	#now convert p into a long:
	#p = long(p_initial)


#count_nosolns = order_result[0]
				#count_order_not_prime = order_result[1]
				#count_q_e_found = order_result[2]
				#count_q_e_not_found = order_result[3]
				#q_e_nf_order_p_list = order_result[4]
				#order_false_list = order_result[4]
				#q = order_result[5]
				#e = order_result[6]
				#order_status = order_result[7]
				#n_prime = order_result[8]
				#count_order_prime = order_result[9]
				#order = order_result[10]
				#lhs = order_result[11]
				#concat_order_p=str(order)+"_"+str(p)

				#if str(order)+"_"+str(p) in q_e_nf_order_p_list:
				#elif concat_g_p in order_false_list:
				#	count_nosolns = count_nosolns + len(h_values)
					#print("Previously calculated - "+str(concat_order_p)+" is NOT in form q**e !"
				#	x_final = "No solns!"			
					#print("g: "+str(g)+", p: "+str(p)+", h: "+str(h)+", x: "+str(x_final)+", no_solns: "+str(count_nosolns)+", largerprimelist: "+str(count_needlargerprimelist)+", count_q_e_found: "+str(count_q_e_found)+", count_q_e_not_found: "+str(count_q_e_not_found)+", count_order_prime: "+str(count_order_prime)+", count_order_not_prime: "+str(count_order_not_prime)+", count_xi_not_found: "+str(count_xi_not_found)+", count_calc_xi_status_false: "+str(count_calc_xi_status_false)
				#else:

#def testing():

	#print("---------------------"
#	print("g: "+str(g)+", h: "+str(h)+", p: "+str(p)
	
	#check if h > p	
#	if h > p:
		#set h to h mod p
#		h = h % p
#		print("This is equivalent to the problem for h = "+str(h)+" mod "+str(p)+". Using this new value for h: "+str(h)+".."

	#initialise G_list & calculate elements of G:
#	G_list = []

#	for number in range(1, p):
#		element = int(pow(g, number, p))
#		if element not in G_list:
#			G_list.append(element)
#
#	print("Group G is: "+str(G_list)

#	#check if h is in G generated by g 
#	if h not in G_list:
#		print("h is not in Group G. Hence no solutions! Exiting.."
#		sys.exit()				

	#define counts for different types of results
#	count_nosolns=0
#	count_zi_bi_equal_1=0
#	count_bi_equal_1_zi_ntequal_0_1=0
#	count_x_equals_0=0
##	count_Bi_equals_zi=0
#	count_normal_soln=0
#	count_needlargerprimelist=0

	#define lists for different types of results
#	answers_to_be_checked=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

#	print("-----------------------------------"

	#print('Running dlp()..')
#	result = dlp(g, p, h, primefile, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked)

#	x=result[0]
#	M=result[7]
#	x_status=result[7]	

#	result=check_answer(g,p,h,x)
#	if result==False:
##		#status=False
#		print("CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x: "+str(x)+", M: "+str(M)
#	else:
#		print("-----------------------------------"
#		print("Final solution: x= "+str(x)+" mod "+str(M)
	

