#Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.
#Version 3. 12/06/2018.
#Programmed & tested in Python 3.4.3 only
#This program attempts to factorise a number N specified by user, via pollard brent rho. 
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in xxx seconds.

#import sys
import math
from fractions import gcd
import csv
#import os
#import itertools
import time
import random
	
version = 3

primes_under_100 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,97]

#prime_list_path="/home/mint/Desktop/"
#prime_list_filename="primes_upto_100000.csv"
#primefile=prime_list_path + prime_list_filename

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.")
print("Version:",version,". 12/06/2018.")
print("Programmed & tested in Python 3.4.3 only.")
print("This program loops through all numbers upto N specified by user, and attempts to factorise each number via difference of sqaures.") 
#print("Results printed are three arrays - first for prime factors, second for powers of those primes.")
#print("Prime list file should be a .CSV file with each prime separated by commas."
#print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
#print("The larger the prime file is that is used, the longer the factorisation will take!"
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in XXX seconds.")
print("---------------------------------------------------------------------")
	
def main():
	
	print('Number to attempt to factorise?')
	N_initial = input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()	

	#now convert type for N into a long:
	N = int(N_initial)

	#Overrite N with N = for testing
	#N = 9788111

	diff_of_squares_main(N)

def diff_of_squares_main(N):
	
	#Step 1 - relation building
	print("N:",N)

	result_rel = relation(N)
	#return c_i, a_i
	c_i = result_rel[0]
	a_i = result_rel[1]
	primes_upto_50 = result_rel[2]

	#Step 2 - Elimination
	result_elim = elimination(c_i, a_i, primes_upto_50)

	#Step 3 - GCD computation
	result_gcd_comp = gcd_computation()


def relation(N):
	#relation building
	print("Running relation building..")

	#Find many integers a_1, a_2, .. , a_r with the property that the quantity c_i = pow(a_i,2,N) factors as a product of small primes
	#For N = 9788111, we look for numbers that are 50-smooth. 
	primes_upto_50 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]

	initial_a = int(math.ceil(math.sqrt(N)))
	print("initial a to consider from:",initial_a)

	a_i = [3129,3130,3131,3166,3174,3215,3313,3449,3481,3561,4394,4425,4426,4432,4442,4468,4551,4595,4651,4684]
	print("a_i:",a_i)
	#c_i = [2530,8789,15050,235445,286]
	
	c_i = []
	#generate each c_i
	for num in a_i:
		c_i.append(pow(num,2,N))
	print("c_i:",c_i)
	
	return c_i, a_i, primes_upto_50

def elimination(c_i, a_i, primes_upto_50):
	#elimination
	print("Running elimination..")

	#Take a product c_i_1, c_i_2 , .. , c_i_n of some of the c_i's so that every prime appearing in the product appears to be an even power.
	#Then c_i_1 x c_i_2 .. x c_i_n = b**2 is a perfect square.
	#Goal is to take a product of some of the c_i's in order to make each each prime on rhs of equation appear to an even power.
	#aka problem reduces to finding u_1, u_2, .. , u_r in {0,1} s.t. c_i_1 x c_i_2 .. x c_i_n is a perfect square.
	#We take u_i = 1 if we want to include c_i in the product
	#we take u_i = 0 if we don't want to include c_i in the product
	#Pi_i=1^r[c_i**u_i] = Pi_j=1^t[p_j**[Sum_i=1^r[e_ij*u_i]]]
	#we are searching for integers u_1, u_2, .. , u_r s.t. 

		#e_11*u_1 + e_21*u_2 + ... + e_r1*u_r = 0 (mod 2)
		#e_12*u_1 + e_22*u_2 + ... + e_r2*u_r = 0 (mod 2)
		# ...		
		#e_1t*u_1 + e_2t*u_2 + ... + e_rt*u_r = 0 (mod 2)

	#initialise lists
	prime_factors_all=[]
	powers_all=[]

	#need to factorise each of the c_i
	for c in c_i:
		factors = factorise_wheel235(c)
		#return factors

		result2 = calc_primefactors_powers(c, factors)
		#return prime_factors, powers
		prime_factors = result2[0]
		powers = result2[1]

		prime_factors_all.append(prime_factors)
		powers_all.append(powers)
		
	#print("prime_factors_all:",prime_factors_all)
	#print("powers_all:",powers_all)

	for pf in prime_factors_all:
		index_pf = prime_factors_all.index(pf)
		#print("index_pf",index_pf)
		print("prime_factors:",pf,", powers:",powers_all[index_pf])

	len_c_i_all = len(c_i)
	len_primes_upto_50 = len(primes_upto_50)	

	print("len_c_i_all:",len_c_i_all, "len_primes_upto_50:",len_primes_upto_50)

	#creates a list containing h lists (h = len_prime_factors_all), each of 20 items, all set to 0
	w = 20				#number of items in each list
	h = len_c_i_all			#number of lists

	Matrix = [[0 for x in range(w)] for y in range(h)]	

	print("initial Matrix:",Matrix)

	#Update each list of Matrix with a prime factor using "primes_upto_50" list
	for prime_factor in primes_upto_50:
		pf_index = primes_upto_50.index(prime_factor)		
		Matrix[pf_index][0]= prime_factor

	print("Matrix after prime_factors update:",Matrix)

	#Matrix[][]

	#for pf in prime_factors_all:
	#	print("pf:",pf)
	#	list_dummy = []
	#	for element in pf:
	#		element_index = pf.index(element)
	#		if element not in list_dummy:
	#			list_dummy.append(element)

	input("Waiting for user..")

	
def gcd_computation(a_i, b, N):
	print("Running gcd computation..")
	#gcd computation
	#Let a = a_i_1 x a_i_2 x .. x a_i_n 
	#Compute the GCD d = gcd(N, a-b)
	#Since a**2 = (a_i_2 x a_i_2 x .. x a_i_n)**2 = (a_i_1)**2 x (a_i_2)**2 x .. x (a_i_n)**2 = c_i_1 x c_i_2 .. x c_i_n = b**2 (mod N),
	#Then there is a reasonable chance that d is a non-trivial factor of N.
	#Find many integers a_1, a_2, .. , a_r with the property that the quantity c_i = pow(a_i,2,N) factors as a product of small primes

def factorise_wheel235(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print("Running factorise_wheel235()..")	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.time()	
	factors = []
	#c_lists = time.time() - s_before_lists

	#print("Calculating prime factors and powers"
	#s_before_factorisations = time.time()	
	#N=5 - gets listed as remainder instead of factor!!!	
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]
	length, cycle = 11,3
	f, factors, next = 2, [], 0
	while f*f <= N:
		while N % f == 0:		
			#f is a factor. Add factor f to fs
			factors.append(f)
			N /= f
		f += gaps[next]		
		next += 1
		if next == length:
			next = cycle
	if N > 1: factors.append(int(N))
		
	#c_factorisations = time.time() - s_before_factorisations

	#print("factors are: "+str(factors)
	#print("c_factorisations are: "+str(c_factorisations)

	#input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors
	#return factors, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem

def calc_primefactors_powers(N, factors):
	#print("------------------"
	#print("Running calc_primefactors_powers(",factors,")..")
	
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]
	fac_list = []
	#c_calc_primefactors = 0
	#s_before_primefactors = time.time()	
	for factor in factors:		
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if factor not in fac_list:
			#factor is not in fac_list
			#add factor to prime_factors
			prime_factors.append(factor)
			#print("Added "+str(factor)+" to prime_factors"
			#print("prime_factors is: "+str(prime_factors)
			#print str(factor)+" is NOT in fac_list"
			#append it				
			fac_list.append(factor)				
			
			#print("count is: "+str(count)
			#print("fac_list is: "+str(fac_list)
				
		else:
			#factor is in fac_list
			fac_list.append(factor)
			#print str(factor)+" added to fac_list"
	
	#prime_factors = fs
	#print("prime_factors are: "+str(prime_factors)
	#prime_factors.append(factor)
	#print("Added "+str(factor)+" to prime_factors"
	
	#print("prime_factors are: "+str(prime_factors)
	#c_calc_primefactors = time.time() - s_before_primefactors

	powers = []
	#s_before_calc_powers = time.time()
	for prime_factor in prime_factors:
		count = 0
		while N % prime_factor == 0:
			count = count + 1
			N = N / prime_factor		
		else:
			powers.append(count)
				
	#print("powers are: "+str(powers)
	#c_calc_powers = time.time() - s_before_calc_powers

	#input("Waiting for user..")	

	return prime_factors, powers
	#return prime_factors, powers, c_calc_primefactors, c_calc_powers

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
	
	#print("Running isprime(",p,")..")
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

def gcd(a,b):
	a = abs(a)
	b = abs(b)
	while a:
		a,b = b % a, a
	return b

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
	if input_number > 2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	diff_of_squares_main(9788111)
	#main()

	

