#Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.
#Version 1. 10/06/2018.
#Programmed & tested in Python 3.4.3 only
#This program attempts to factorise a number N specified by user, via pollard brent rho. 
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in xxx seconds.

#import sys
#import math
#from fractions import gcd
import csv
#import os
#import itertools
import time
import random
	
version = 1

primes_under_100 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,97]

#prime_list_path="/home/mint/Desktop/"
#prime_list_filename="primes_upto_100000.csv"
#primefile=prime_list_path + prime_list_filename

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.")
print("Version:",version,". 10/06/2018.")
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

	diff_of_squares_main(N)

def diff_of_squares_main(N):
	
	#Step 1 - relation building
#	result_rel = relation(N)
	#return c_i, a_i, m_i
#	c_i = result_rel[0]
#	a_i = result_rel[1]
#	m_i = result_rel[2]

	c_i = [3129,3130,3131,3166, ]
	a_i = []
	m_i = []

	#Step 2 - Elimination
	result_elim = elimination()

	#Step 3 - GCD computation
	result_gcd_comp = gcd_computation()


def relation(N)
	#relation building
	#Find many integers a_1, a_2, .. , a_r with the property that the quantity c_i = pow(a_i,2,N) factors as a product of small primes

	initial_a = int(math.ceil(math.sqrt(N)))
	print("initial_a:",initial_a)

	return c_i, a_i, m_i

def elimination()
	#elimination
	#Take a product c_i_1, c_i_2 , .. , c_i_n of some of the c_i'sso that every prime appearing in the product appears to be an even power.
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

def gcd computation()
	#gcd computation
	#Let a = a_i_1 x a_i_2 x .. x a_i_n 
	#Compute the GCD d = gcd(N, a-b)
	#Since a**2 = (a_i_2 x a_i_2 x .. x a_i_n)**2 = (a_i_1)**2 x (a_i_2)**2 x .. x (a_i_n)**2 = c_i_1 x c_i_2 .. x c_i_n = b**2 (mod N),
	#Then there is a reasonable chance that d is a non-trivial factor of N.

	


Find many integers a_1, a_2, .. , a_r with the property that the quantity c_i = pow(a_i,2,N) factors as a product of small primes

def brent(N):
	s_before = time.time()
	steps = 0
	if N == 1:
		steps = 1
		total_factoring_time = time.time() - s_before
		return 1, steps, total_factoring_time
	if N % 2 == 0:
		steps = 1
		total_factoring_time = time.time() - s_before
		return 2, steps, total_factoring_time

	y, c, m = random.randint(1, N-1), random.randint(1, N-1), random.randint(1, N-1)
	g, r, q = 1, 1, 1
	while g == 1:
		steps = steps + 1
		x=y
		#print("x,y:",x,y)
		for i in range(r):
			steps = steps + 1
			y = ((y * y) % N + c) % N
			#print("y is now:",y)
		k = 0
		while k < r and g == 1:
			steps = steps + 1
			#print("k is now:",k)
			ys = y
			#print("ys is now:",ys)
			for i in range(min(m, r-k)):
				steps = steps + 1
				y = ((y * y) % N + c) % N
				#print("y is now:",y)
				q = q * (abs(x - y)) % N
				#print("q is now:",q)
			g = gcd(q, N)
			#print("g is now:",g)
			k = k + m
		r *= 2
		#print("r is now:",r)

	if g == N:
		steps = steps + 1
		#print("g == N")
		while True:
			steps = steps + 1
			ys = ((ys * ys) % N + c) % N
			#print("ys is now:",ys)
			g = gcd(abs(x - ys), N)
			#print("g is now:",g)
			if g > 1:
				#print("g > 1")
				break
	total_factoring_time = time.time() - s_before
	return g, steps, total_factoring_time

#def g(x,n):
	#result = (x*x + 1) % n
#	print(x,"*",x,"+1 %",n,"is:",(x*x + 1) % n)
	#return result
#	return (x*x + 1) % n

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
	#brent_main(8563846098436981)
	#brent_main(49680348603860068094680968683)
	#brent_main(6896276987698754967986754986759467541)
	#brent_main(1018452335082256642989215628692657146881526417)
	main()

	

