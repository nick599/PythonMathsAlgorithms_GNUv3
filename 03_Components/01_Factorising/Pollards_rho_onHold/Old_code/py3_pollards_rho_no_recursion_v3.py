#Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.
#Version 3. 28/05/2018.
#Programmed & tested in Python 3.4.3 only
#This program attempts to factorise a number N specified by user, via pollards rho. 
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in xxx seconds.

import sys
import math
import fractions
import csv
import os
import itertools
import time
	
version = 3

primes_under_100 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,97]

#1) 8563846098436981 - works fine

#2) 6896276987698754967986754986759467541 - 612043 and 3658873 appended as factors
# 3079536996847765678773719 - using isprime() is prime.

#3) 938469860986094836084096843096840968904698368374689368937467343 - multiple factors found quickly.
# 1018452335082256642989215628692657146881526417 - seed 2 - >> 20 mins! 
# How many numbers need to be processed??? 
# Why is d always 1 for this??? 
# What to do in this case???

def main():
	#prime_list_path="/home/mint/Desktop/"
	#prime_list_filename="primes_upto_100000.csv"
	#primefile=prime_list_path + prime_list_filename

	print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.")
	print("Version:",version,". 28/05/2018.")
	print("Programmed & tested in Python 3.4.3 only.")
	print("This program attempts to factorise a number N specified by user, via pollards rho.") 
	#print("Results printed are three arrays - first for prime factors, second for powers of those primes.")
	#print("Prime list file should be a .CSV file with each prime separated by commas."
	#print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
	#print("The larger the prime file is that is used, the longer the factorisation will take!"
	print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in XXX seconds.")
	print("---------------------------------------------------------------------")
	
	#Check if primefile exists.
	#if os.path.exists(primefile) is False:
	#	#File doesn't exist in location. Exit process.
	#	print('Prime file doesn\'t exist in location specified. Exiting.')
	#	sys.exit()

	#print('Using primefile: '+str(primefile))
	
	print('Number to attempt to factorise?')
	N_initial = input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()	

	#now convert type for N into a long:
	N = int(N_initial)

	#call number_checks() for simple checks on input 
	number_checks(N)	
	
	#Call size_input_check() if want to stop program running for very large numbers 
	#size_input_check()

	#initialise seed
	seed = 2
	
	#initialise lists
	factors=[]	
	factoring_times=[]
	isprime_times=[]
	stage=""
	n_init=0	

	#if len(str(N)) > 15:
	while N != 1:
		if len(str(N))<=15:
			isprime_result = isprime_SO_step6(N)
			if isprime_result[0] == True:
				#return True, c_after_primes
				factors.append(N)
				print(N,"appended as factor resulting from being prime. Time:",round(isprime_result[1],3))
				isprime_times.append(isprime_result[1])
			N = 1
		else:
			#print("----------------------------------------------")
			#print("N is now:",N,", seed:",seed)
			#isprime_result = isprime_Step2_squaring(N)
		
			result = pollards_rho_factorise(N, seed, factors, factoring_times, stage)
			#return n, d, factors OR "Failure", factoring_times
			n_init = result[0]
			d = result[1]
			status = result[2]
			#print("n_init is:",n_init,", status:",status)
			#input("Waiting for user..")
			c_factorisations = result[3]
			#index = 0
			if status == "Failure":
				#index = index + 1
				#seed = primes_under_100[index] 
				seed = seed + 1
				#print("seed now is:",seed)
				#input("Waiting for user..")
				if seed == 8:
					isprime_result = isprime_SO_step6(N)
					if isprime_result[0] == True:
						#return True, c_after_primes
						factors.append(N)
						print(N,"appended as factor resulting from being prime. Time:",round(isprime_result[1],3))
						isprime_times.append(isprime_result[1])
						N = 1	
					#else:
					#	#N is not prime! Resume pollard rho..
					#	result = pollards_rho_factorise(N, seed, factors, factoring_times, stage)
					#	#return n, d, factors OR "Failure", factoring_times
					#	n_init = result[0]
					#	d = result[1]
					#	status = result[2]
					#	#print("n_init is:",n_init,", status:",status)
					#	#input("Waiting for user..")
					#	c_factorisations = result[3]
			else:
				factors.append(d)
				print(d,"appended as factor - using pollard_rho. Time:",round(c_factorisations,3))
				#print("c_factorisations:",c_factorisations)
				factoring_times.append(c_factorisations)
				#print("---------------------")
				N = n_init//d
			
	total_isprime_time = 0
	for time in isprime_times:
		total_isprime_time = total_isprime_time + time 		

	total_factoring_time = 0
	for time in factoring_times:
		total_factoring_time = total_factoring_time + time 		

	print("factors:",factors,"total time (pollard rho):",round(total_factoring_time,3), "total time (isprime):", round(total_isprime_time,3))

def pollards_rho_factorise(n, seed, factors, factoring_times, stage):		
	#based on code on https://en.m.wikipedia.org/wiki/Pollard%27s_rho_algorithm/
	#this is is O(???) and XXX times faster than trial division in practice
	
	#print("----------------------------------------------")
	print("Running pollards rho factorise(",n,",",seed,")..")	

	s_before_factorisations = time.time()	
		
	x = seed
	y = seed
	d = 1

	while d == 1:
		x = g(x,n)	
		#print("g(x,n):",x)
		#print("g(y,n):",g(y,n))
		y = g(g(y,n),n)		
		#print("g(g(y,n)):",y)
		#print("abs(x-y):",abs(x-y))
		d = fractions.gcd(abs(x-y),n)
		#print("x:",x,"y:",y,"d:",d)

	c_factorisations = time.time() - s_before_factorisations

	if d == n:
		#print(d,"=",n)
		return n, d, "Failure", c_factorisations		
	else:
		return n, d, factors, c_factorisations

def g(x,n):
	#result = (x*x + 1) % n

	#return result
	return (x*x + 1) % n

def isprime_Step2_squaring(p):		#this is O(sqrt(n))
	
	#print("Running isprime(",p,")..")
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	s_before_primes = time.time()
	if p==1:
		c_after_primes = 0
		return False, c_after_primes	
	if p==2:
		c_after_primes = 0
		return True, c_after_primes
	
	i = 3
	while i*i <= p:
		#print("i*i:",i*i,", p:",p)
		#if pow(i,2,5) == 5:
			#print("i*i:",i*i)
		if p % i == 0:
			c_after_primes = time.time() - s_before_primes
			return False, c_after_primes
		i += 2

	c_after_primes = time.time() - s_before_primes
	return True, c_after_primes

def isprime_SO_step6(p):	#this is O(???)
	
	print("Running isprime(",p,")..")
	# http://stackoverflow.com/questions/4545114/quickly-determine-if-a-number-is-prime-in-python-for-numbers-1-billion
	
	s_before_primes = time.time()
	if p<=100:
		c_after_primes = time.time() - s_before_primes
		return (p in primes_under_100), c_after_primes

	if p % 2 ==0 or p % 3 == 0:
		c_after_primes = time.time() - s_before_primes
		return False, c_after_primes	
	
	for f in range(5, int(p ** .5),6):
		if f % 25000000 == 1:
			print("f:",f)
		if p % f == 0 or p % (f+2) == 0:
			c_after_primes = time.time() - s_before_primes
			return False, c_after_primes
	c_after_primes = time.time() - s_before_primes
	return True, c_after_primes
	#return True

def number_checks(number):

	#Simple Checks for N:
	#print('Running simple checks for number...')
	if number==0:
		print('Number entered is 0. Please choose another value for N')
		sys.exit()
	if number==1:
		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
		sys.exit()
	if number<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()

	

