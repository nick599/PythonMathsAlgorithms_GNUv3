#Copyright Nick Prowse 2018. Code Licenced under GNU GPL3.
#Version 1. 03/06/2018.
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
print("Source: http://gist.github.com/ssanin82/18582bf4a1849dbf8afd. Code Licenced under GNU GPL3.")
print("Version:",version,". 03/06/2018.")
print("Programmed & tested in Python 3.4.3 only.")
print("This program loops through all numbers upto N specified by user, and attempts to factorise each number via pollards brent rho / pollards rho.") 
print("mbers upto N specified by user, and attempts to factorise each number via pollards brent rho / pollards rho.") 
#print("Results printed are three arrays - first for prime factors, second for powers of those primes.")
#print("Prime list file should be a .CSV file with each prime separated by commas."
#print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
#print("The larger the prime file is that is used, the longer the factorisation will take!"
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in XXX seconds.")
print("---------------------------------------------------------------------")
	
#1) 8563846098436981 - 16 digits - works fine

# 2) 49680348603860068094680968683 - seed 2 - >> 2 mins!
# This is prime. Found out using ECM / SIQS applet on Dario Alpern's routine.

#3) 54978548758709587057809788703 - seed 2 - works fine

#4) 6896276987698754967986754986759467541 - 36 digits - 612043 and 3658873 appended as factors

#5) 938469860986094836084096843096840968904698368374689368937467343 - multiple factors found quickly.

##### 6) 1018,452335,082256,642989,215628,692657,146881,526417 - seed 2 - >> 20 mins! 
# This is prime. Found out using ECM / SIQS applet on Dario Alpern's routine.

# How many numbers need to be processed??? 
# Why is d always 1 for this??? 
# What to do in this case???
# If pbr algorithm takes over 2 mins to find a number then it is probably prime?
	
def main():
	
	print('Number to attempt to factorise?')
	N_initial = input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()	

	#now convert type for N into a long:
	N = int(N_initial)

	size_input_check(input_number)
	brent(N)
	#brent_main(N)

def brent_main(N):
	for num in range(1,N+1):
		if num % 100000 == 1:
			print("Number:",num)
		result_main = brent(num)
		#return factor, steps, total_factoring_time
		factor = result_main[0]
		steps = result_main[1]
		total_factoring_time = result_main[2]
		if total_factoring_time >= 1:
			print("Number:",num,", Factor:",factor,", steps:", steps, ", total_factoring_time:", round(total_factoring_time,6))	

def brent(N):
	print("Running brent(",N,")")
	s_before = time.time()
	steps = 0
	if N == 1:
		steps = 1
		total_factoring_time = time.time() - s_before
		print("N:",N,", g:1, steps:",steps,", total factoring time:",total_factoring_time)
	if N % 2 == 0:
		steps = 1
		total_factoring_time = time.time() - s_before
		print("N:",N,", g:2, steps:",steps,", total factoring time:",total_factoring_time)
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
	print("N:",N,", g:",g,", steps:",steps,", total factoring time:",total_factoring_time)

#def g(x,n):
	#result = (x*x + 1) % n
#	print(x,"*",x,"+1 %",n,"is:",(x*x + 1) % n)
	#return result
#	return (x*x + 1) % n

def isprime_Step2_squaring(p):		#this is O(sqrt(n))
	
	print("Running isprime_Step2_squaring(",p,")..")
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	s_before_primes = time.time()
	if p==1:
		c_after_primes = 0
		#return False, c_after_primes
		print("p is prime", c_after_primes)	
	if p==2:
		c_after_primes = 0
		#return True, c_after_primes
		print("p is prime", c_after_primes)
	
	i = 3
	while i*i <= p:
		#print("i*i:",i*i,", p:",p)
		if pow(i,2,5) == 0:
			print("i*i:",i*i)
		if p % i == 0:
			c_after_primes = time.time() - s_before_primes	
			print("p is NOT prime", c_after_primes)
			return False, c_after_primes
		i += 2

	c_after_primes = time.time() - s_before_primes
	print("p is prime", c_after_primes)
	return True, c_after_primes

def isprime_SO_step6(p):	#this is O(???)
	
	print("Running isprime_SO_step6(",p,")..")
	# http://stackoverflow.com/questions/4545114/quickly-determine-if-a-number-is-prime-in-python-for-numbers-1-billion
	
	s_before_primes = time.time()
	if p<=100 and p in primes_under_100:
		c_after_primes = time.time() - s_before_primes
		#return (p in primes_under_100), c_after_primes
		print("p is prime", c_after_primes)

	if p % 2 ==0 or p % 3 == 0 or p % 7 == 0 or p % 11 == 0:
		c_after_primes = time.time() - s_before_primes
		#return False, c_after_primes
		print("p is divisible by 2 or 3 or 7 or 11", c_after_primes)
	for f in range(5, int(p ** .5),6):
		if f % 25000000 == 1:
			print("f:",f)
		if p % f == 0 or p % (f+2) == 0:
			c_after_primes = time.time() - s_before_primes
			print("p is not prime", c_after_primes)
			return False, c_after_primes
	c_after_primes = time.time() - s_before_primes
	#return True, c_after_primes
	print("True", c_after_primes)

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
	#brent(8563846098436981)
	#takes < 5*10^-5s	

	#####isprime_Step2_squaring(49680348603860068094680968683)
	#####isprime_SO_step6(49680348603860068094680968683)
	#####brent(49680348603860068094680968683)
	##### number is prime. 

	#brent(9680348603860068094680968683)
	#takes < 7.6*10^-5
	#isprime_SO_step6(9680348603860068094680968683)[0]
	#isprime_Step2_squaring(9680348603860068094680968683)[0]	
	#p is not prime!

	#brent(54978548758709587057809788703)
	#takes < 4.2*10^-5s

	#brent(6896276987698754967986754986759467541)
	#takes 0.006s

	#####isprime_SO_step6(1018452335082256642989215628692657146881526417)
	#####brent(1018452335082256642989215628692657146881526417)

	#brent(938469860986094836084096843096840968904698368374689368937467343)
	#takes < 5.9*10^-5 s

	
	#brent_main(8563846098436981)
	#brent_main(49680348603860068094680968683)
	#brent_main(6896276987698754967986754986759467541)
	#brent_main(1018452335082256642989215628692657146881526417)
	
	#main()

	

