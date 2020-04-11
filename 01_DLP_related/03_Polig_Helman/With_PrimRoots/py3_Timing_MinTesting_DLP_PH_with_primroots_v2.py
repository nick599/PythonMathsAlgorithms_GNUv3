#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 2. 03/05/2018.
#Programmed & tested in Python 3.4.3 only
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
print("Version 2. 03/05/2018.")
print("Programmed & tested in python 3.4.3 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via Polig-Helman Algorithm via factorisation of (p-1) where p is a prime number")
print("Results printed are three arrays ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997")
print("---------------------------------------------------------------------")

def main():

	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	print("primefile currently is:",primefile)

	primes = csvfile_store_primes(primefile)
	sample_range = range(1,21)
	g_values = range(2,4)
	#time_values = []
	#total_combinations = []
	for num in range(1,11):	
		#p_values= primes[0:(num*100)+1]
		if num == 1:		
			p_values= primes[0:101]
			print("Test number is: 1 p_values: 0:101")
		else: 
			p_values= primes[((num-1)*100)+1:(num*100)+1]
			print("Test number is:",num,", p_values:",((num-1)*100)+1,"to",(num*100)+1)
		
		time_values=[]
		total_combinations=[]
		for x in sample_range:			
			result = test(g_values, p_values, primes)
			#return c_after_loops_mins, Grand_total_values
			#time = result[0]
			time_values.append(result[0])
			if not total_combinations:			
				total_combinations.append(result[1])
			
		total_time = 0
		for time in time_values:
			total_time = total_time + time

		mean_time = round(float(total_time) / len(time_values),4)
		max_time = round(max(time_values),4) 	
		min_time = round(min(time_values),4)

		print("Total combinations:",total_combinations[0],", time taken (mins) - mean:",mean_time,", max:",max_time,", min:",min_time)			
		
def test(g_values, p_values, primes):
	#prime_list_path="/home/mint/Desktop/"
	#prime_list_filename="primes_upto_100000.csv"
	#primefile=prime_list_path + prime_list_filename
	#print("primefile currently is: ",primefile)

	#primes = csvfile_store_primes(primefile)
	
	#initialise g_values, p_values, and h_values
	#g_values = range(2,4)
	#p_values = primes[0:1001]
	
	total_g_values=len(g_values)
	#print("total_g_values: ",total_g_values)

	total_p_values=len(p_values)
	#print("total_p_values: ",total_p_values)

	sum_primes=0
	for p in p_values:
		sum_primes = sum_primes + p		

	#print("Sum of primes in p_values is:",sum_primes)

	#total_h_values is the sum of (p[0]-1) + (p[1]-1) + ... + (p[n-1]-1) = sum(primes) - (number of primes)
	total_h_values = sum_primes - total_p_values	

	Grand_total_values = total_p_values * total_g_values * total_h_values
	#print("Grand_total_values:",Grand_total_values)
	
	#define lists for different types of results
	answers_to_be_checked=[]
	n_prime=[]
	
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

	#print("======================================")

	#print("Looping through values for g, p, & h..")

	s_before_loops = time.clock()
	for g in g_values:
		#print("======================================")
		#print("g is: ",g)
		for p in p_values:
			p_position = p_values.index(p)
			#if p_position % 50 == 0:
				#print("index of p: ",p_position)
			h_soln_alreadyfound = False
			if g == p:
				count_nosolns = count_nosolns + len(range(1,p))	
			else:				
				#Want to calculate and store group G				
				G_list = []				
				for number in range(1, p):
					a = pow(g,number,p)
					if a not in G_list:					
						G_list.append(a)
					else:
						break

				for h in range(1, p):								
					#check if h is in G generated by g 
					if h not in G_list:
						count_nosolns = count_nosolns + 1
					elif h >= p:
						h_soln_alreadyfound = True							
						break													
					elif g == h:
						x_final = 1
						x_moduli_final = p - 1
						#x_to_print = str(x_final)+" mod "+str(x_moduli_final)
	
						#Check answers
						if pow(g, x_final, p) != h:
							print("CHECK x_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
							input("Waiting for user..")

						elif pow(g, x_final+x_moduli_final, p) != h:
							print("CHECK x_moduli_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
							input("Waiting for user..")					
					else:
						result = dlp(g, p, h, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked)

						x_final = result[0]
						count_nosolns = result[1]
						count_normal_soln = result[6]
						x_moduli_final = result[7]
						count_x_equals_0 = result[4]
						x_status=result[9]
					
						if x_status == True:
							#if x_final != "No solns!":
							#	x_to_print = str(x_final)+" mod "+str(x_moduli_final)
						
							#Check answers
							checks_fail = False							
							if pow(g, x_final, p) != h:
								checks_fail = True
								print("CHECK x_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
							
							elif pow(g, x_final + x_moduli_final, p) != h:
								checks_fail = True
								print("CHECK x_moduli_final! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final,", x_moduli_final: ",x_moduli_final)
							for number in (1, x_moduli_final):
								a = pow(g, x_final + number, p)
									
								if a == h and number < x_moduli_final:
									checks_fail = True
									print("CHECK x_moduli_final! - smaller x_moduli found! g: ",g,", h: ",h,", p: ",p,", x_final: ",x_final)
							if checks_fail != False:
								print("*** 1 or more Checks FAILED! ***")
								input("Waiting for user..")

						#else:
							#count_x_status_false = count_x_status_false + 1
						

	c_after_loops = time.clock() - s_before_loops
	c_after_loops_mins = float(c_after_loops)/60

	#print("Grand total combinations considered:",Grand_total_values,", total_g_values:",total_g_values,", total_p_values:",total_p_values,", total_h_values:",total_h_values,", number_no_solns:",count_nosolns,", largerprimelist:",count_needlargerprimelist,", count_x_status_false:",count_x_status_false,"Time_mins:",c_after_loops_mins)

	return c_after_loops_mins, Grand_total_values

def ghp_checks(g, p, h, floor_sqrt_p, count_notprime):

	#print("Running ghp_checks().."

	status=1
	
	#Need to check if p is prime
	a = isprime(p)	
	#return True for prime, False for not prime
	if a == False:
		print("The number entered for p: ",p," is not prime. Please choose a number that is prime for p.")
		status=0
		count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	if (g==0 or h==0 or p==0):
		print("One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.")
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
	cong_x=[]
	cong_moduli=[]
	x_new = 0
	M = 0
	a = 0
	b = 0
	for number in range(0,len(x)):		
		#store values in 1st congruence	
		a= x[number]
		b= x_moduli[number]
		if b!=1:		
			if not cong_x:
				#cong has no elements. Add values in first congruence			
				cong_x.append(a)
				x_new = a		
				cong_moduli.append(b)
				M = b			
			else:
				#cong_x has elements. Subtract current cong_x[number-1] from current x[number]
				c = x[number] - cong_x[-1]
				#now want to find (cong_moduli[number-1]**-1) mod(b)		
				f = calc_modinverse(cong_moduli[-1], 1, b)
				#now take c and times it by the inverse, f, and reduce mod b
				k = (c*f) % b			
				#now take value of k and use it to work out new value of x
				x_new = cong_x[number-1] + (cong_moduli[number-1] * k)
				cong_x.append(x_new)
				#now work out value of M
				M = cong_moduli[-1] * b
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

	status = True
	check = 0	
	ep = euler_phi_primesused(p)
	#return a	
	#ep=result[0]
	
	factors = factorise(ep)	
	result2 = calc_primefactors_powers(factors, ep)
	#return prime_factors, powers, c_calc_powers		
	prime_factors = result2[0]
	powers = result2[1]
	power=1

	#Do we need to check prim roots now???
	for prime in prime_factors:		
		if status==True:
			power=1
			power_index = 0
			while power < powers[power_index]:
				if pow(g,int(ep / pow(powers[power_index],power)),p) == 1:
					status=False	
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

	if n==1:					#O(1)	#subtotal O(3)
		a = 1					#O(1)				
		return a				#O(1)		
			
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
		prime_factors = calc_primefactors_nopowers(factors) 	#O(???)		#Best operations: ??? 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		
		len_prime_factors = len(prime_factors)

		#initialise ep
		ep=n
		
		for prime in prime_factors:			#O(prime_factors)
			#now calculate first (1-1/p) for p|n
			term = 1 - 1 / float(prime)
			#recalculate ep
			ep = ep * term
			
		ep = int(ep)
		return ep				#O(1)
		
def check_answer(g, p, h, x):
	status=True	
	if pow(g,x,p) != h:
		status=False
		
	return status	

def dlp(g, p, h, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked):	

	floor_sqrt_p = int(math.floor(math.sqrt(p)))
	
	#Run checks on g, h & p	
	count_notprime = 0
	
	#define prime list
	#primes=csvfile_store_primes(primefile)
	
	#check if sqrt_p > largest element in primes
	sqrt_p = math.sqrt(p)
	largest_prime = primes[-1]
	count_needlargerprimelist=0
	if sqrt_p > largest_prime:
		print("Square root of p - ",sqrt_p," is greater than largest prime in list - ",largest_prime,". Consider using a larger prime list. Exiting..")
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
	
	#1st step: Check if g is a primitive root mod p, and factorise p_minus_1 into product of prime powers
	count_primroot=0
	result=prim_root(g,p,primes)
	status=result[0]
	prime_factors=result[1]
	powers=result[2]
	
	if result is False:
		print(g,' is not a primitive root mod ',p,'! Exiting ...')
		sys.exit()
	else:
		#print(str(g)+' is a primitive root mod '+str(p))	
		count_primroot = count_primroot + 1

		#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

		primes_list=prime_factors

		#################################################
		# Polig-Helman Algorithm
		result_polig = polig_helman(primes_list, powers, g, p, h, count_nosolns, count_gi_hi_equal_1, count_diffeq0, count_x_equals_0, count_gi_equal_1_hi_ntequal_0_1, count_normal_soln, count_gi_equals_hi, count_gi_hi_equal_1)
	
		#return x, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status		

		x = result_polig[0]
		x_moduli = result_polig[7]
		x_status = result_polig[9]

		if x_status == False:
			return 0, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, 0, count_diffeq0, x_status, count_needlargerprimelist
		
		elif x_status == True:
			#now need to combine x's and x_moduli via CRT
			result = chinese_remainder(x, x_moduli)
			x_final = result[0]
			x_moduli_final = result[1]
		
			return x_final, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status, count_needlargerprimelist

		else:
			print("x_status is: ",x_status)
			input("Waiting for user..")
			return x_final, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli_final, count_diffeq0, x_status, count_needlargerprimelist


def polig_helman(primes_list, powers, g, p, h, count_nosolns, count_gi_zi_equal_1, count_diffeq0, count_x_equals_0, count_gi_equal_1_hi_ntequal_0_1, count_normal_soln, count_gi_equals_hi, count_gi_hi_equal_1):

	p_minus_1 = p-1

	#3: Calculate C - number of unique primes in factorisation (also is number of congruences to solve)
	C=0
	for prime in primes_list:
		C = C + 1		
	#print('Number of primes in primes_list = C = '+str(C))

	#4: Need to create a list (with C elements) for each of: qi, ei, Wi, gi, hi 
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
		qi.append(primes_list[i])
		ei.append(powers[i])
		Wi.append(int(p_minus_1 / pow(qi[i],ei[i])))	
		gi.append(pow(g,Wi[i],p))
		hi.append(pow(h,Wi[i],p))
		
		#7: Now Bi[i]**x = zi[i] mod p for each i. Need to solve for x for each.
		
		init_moduli = p
			
		#now x = a mod (qi**ei) is a solution where a is unknown
		if gi[i] == 1 and hi[i] == 1:
			x_status = False
			break
			
		elif gi[i] == 1 and hi[i] != 1:
			x_status = False
			break
		else:
			#need to check all x s.t 0 <= x < qi**ei 
			#start with init_moduli. If an exponent is not found then consider prime powers from qi**ei to qi**1 in turn
			
			result = exponent_g_n(gi[i], hi[i], init_moduli)
			#return x, status, moduli		
			status = result[1]			
			#status = False for no exponent found

			if status == False:
				#Exponent is not found for init moduli. Hence consider prime powers from qi**ei to qi**1 in turn
			
				ei_init = ei[i]
				while ei_init >= 1:
					moduli = pow(qi[i],ei_init)
					result = exponent_g_n(gi[i], hi[i], moduli)
					status = result[1]			
					#status = False for no exponent found
					if status == True:
						x_moduli.append(moduli)
						break
					else:				
						ei_init = ei_init - 1	
			else:
				#Exponent & Moduli found
				x.append(result[0])
				x_moduli.append(result[2])
				
			i = i + 1

	return x, count_nosolns, count_gi_hi_equal_1, count_gi_equal_1_hi_ntequal_0_1, count_x_equals_0, count_gi_equals_hi, count_normal_soln, x_moduli, count_diffeq0, x_status

def exponent_g_n(generator, h_value, p):

	#print("Running exponent_g_n("+str(generator)+", "+str(h_value)+", "+str(p)+")"	
	n = 1
	x = 0
	moduli = 0
	status = False
	while n < p:
		if pow(generator, n, p) == h_value:
			x = n
			status = True
			for number in range(x+1, 2*p):
				if pow(generator, number, p)== h_value:
					moduli = number - x
					break
			break
		n = n + 1

	if status == False:
		x = "No exponent found"
		moduli = 0

	return x, status, moduli 

def a_exp_x_eq_r(g, p, r):
	#print("Running a_exp_x_eq_r("+str(g)+", "+str(p)+", "+str(r)+").."
	x=1
	x_values=[]
	count=0
	diff=0
	for x in range(0,p):
		if pow(g,x,p) == r:
			x_values.append(x)
			count=count+1
			if count==2:
				diff = x_values[1] - x_values[0]				
				break
	return diff

def calc_modinverse(g, power, p):
	#print("Running calc_modinverse("+str(g)+", "+str(power)+", "+str(p)+").."	
	
	#this only works for p being prime!	
	if isprime(p) == True:	
		result=pow(g,p-2,p)
		c = pow(result,power,p)
	else:
		#p is not prime!
		c = modinv(g, p)	
	return c

def csvfile_store_primes(csv_filename_var):

	#print 'Running generator..'
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..		
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
	factors = []					#O(1)		
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
		
	return factors		#O(1)
	
def calc_primefactors_nopowers(factors):
	#Worst: O(n+13)	#Best: O(18)

	#print("Running calc_primefactors.."
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	fac_list = []						#O(1)
	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
		if factor not in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
			prime_factors.append(factor)				#O(1)
			fac_list.append(factor)					#O(1)
		else:								#O(1)	#Subtotal: O(4)
			fac_list.append(factor)						#O(1)	
			
	return prime_factors
	
def calc_primefactors_powers(factors, N):
	#print("Running calc_primefactors_powers("+str(factors)+", "+str(N)+").."
	
	#Now want to find max powers m for each factor in factors. can do this by counting unique factors			
	prime_factors=[]
	fac_list = []
	for factor in factors:		
		if factor not in fac_list:
			prime_factors.append(factor)
			fac_list.append(factor)					
		else:
			fac_list.append(factor)
			
	powers = []
	for prime_factor in prime_factors:
		count = 0
		while N % prime_factor == 0:
			count = count + 1
			N = N / prime_factor		
		else:
			powers.append(count)
				
	return prime_factors, powers
	
def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number > 2 * pow(10,8):
		print("Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..")
		sys.exit()

def egcd(a, b):
	#print("Running egcd("+str(a)+","+str(b)+")")
	if a == 0:
		return (b, 0, 1)
	g, y, x = egcd(b % a, a)
	return (g, x - (b//a) * y, y)

def modinv(a, m):
	#print("Running modinv("+str(a)+","+str(m)+")")	
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('No Modular Inverse') 
	return x % m

if __name__=='__main__':
	main()

