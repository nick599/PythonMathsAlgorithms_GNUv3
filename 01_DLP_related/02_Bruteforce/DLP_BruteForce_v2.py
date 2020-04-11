#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 2. 04/03/2018.
#Programmed & tested in Python 2.76 only
#This program attemps to solve a Discrete Log Problem (DLP) specified by user, via brute force of values for x. 
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

print("Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.")
print("Version 2. 04/03/2018.")
print("Programmed & tested in python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via brute force of values of x")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")
	
def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	print('primefile currently is: '+str(primefile))

	#print(sys.version_info)

	print('What is g?')
	g_initial = raw_input()
	if g_initial.isdigit() is False:
		print('You have not entered a positive integer for g. g is: '+str(g_initial)+'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = long(g_initial)

	print('What is h?')
	h_initial = raw_input()
	if h_initial.isdigit() is False:
		print('You have not entered a positive integer for h. h is: '+str(h_initial)+'. Please reenter.')
		sys.exit()

	#now convert h into a long:
	h = long(h_initial)

	print('What is p?')
	p_initial = raw_input()
	if p_initial.isdigit() is False:
		print('You have not entered a positive integer for p. p is: '+str(p_initial)+'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = long(p_initial)

	print("---------------------")
	print("g: "+str(g)+", h: "+str(h)+", p: "+str(p))

	#define counts for different types of results
	count_nosolns=0
	count_zi_bi_equal_1=0
	count_bi_equal_1_zi_ntequal_0_1=0
	count_x_equals_0=0
	count_Bi_equals_zi=0
	count_normal_soln=0
	count_needlargerprimelist=0
	count_brute_force_soln=0	

	#define lists for different types of results
	answers_to_be_checked=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print("======================================")

	print('Running dlp()..')
	#result = dlp(g,h,p, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, prime_factors, powers, moduli)

	result = dlp(g,h,p, primefile, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_brute_force_soln)

	x=result[0]
	M=result[7]
	
	result=check_answer(g,h,p,x)
	if result==False:
		#status=False
		print "CHECK FAILED - g: "+str(g)+", h: "+str(h)+", p: "+str(p)+", x: "+str(x)+", M: "+str(M)
	else:
		print("======================================")
		print "Final solution: x= "+str(x)+" mod "+str(M)

def ghp_checks(g,h,p,floor_sqrt_p, count_notprime):

	status=1
	
	#Need to check if p is prime
	#print('Checking if p is prime ..')
	a = isprime(p,floor_sqrt_p)	
	if a<>0:
		print('The number entered for p: '+str(p)+' is not prime. Please choose a number that is prime for p.')
		status=0
		count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	#print('Running simple checks on g..')
	if (g==0 or h==0 or p==0):
		print('One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.')
		status=0
		sys.exit()
	elif g==1:
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
	elif g<0:
		print('Number for g is negative. Please enter another number')
		status=0
		sys.exit()	
	
	return status

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


#def isprime(p,floor_sqrt_p):
#	#print('p is: '+str(p))	
#	#status=0 for prime
#	status=0
#	if p % 2 == 0:
#		#status=1 for not prime
#		status=1
#	
#	n=3
#	while n <= floor_sqrt_p:
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

#def prim_root(g,p,primes):
#
#	#print('Checking if '+str(g)+' is a primitive root mod '+str(p)+' ..')
#	status=True
#	result = euler_phi(p, primes)		
#	ep=result[0]
#	#print "euler_phi("+str(p)+") is: "+str(ep)
#
#	result=factorise(ep, primes)	
#	prime_factors=result[0]
#	powers=result[1]
#	moduli=result[2]

	#print "prime_factors are: "+str(prime_factors)
	#print "powers are: "+str(prime_factors)
#	power=1

#	for prime in prime_factors:		
#		if status==True:
			#print "================="
			#print "prime is: "+str(prime)
#			power=1
#			power_index = 0
			#print "power_index is: "+str(power_index)
#			while power < powers[power_index]:
				#print "------------------"
				#print "power is: "+str(power)			
#				if g**(ep / powers[power_index]**power) % p == 1:
#					status=False	
					#print "Status is False!"				
#					break
#				power = power + 1
#			power_index = power_index + 1

#	return status, prime_factors, powers, moduli

#def euler_phi(n, primes):
	
	#euler_phi(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.	
	
	#print "Running euler_phi()..."
#	status = True 
#	floor_sqrt_n = math.floor(math.sqrt(n))

	#print "isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#status=1 for not prime
	#status=0 for prime

#	if isprime(n,floor_sqrt_n) == 0:
#		a = n - 1		
#	elif n==1:	
#		a = 1
#	else:
#		print str(n)+" is not prime!"
#		sys.exit()		
#	return a, status

def check_answer(g, h, p, x):
	#def check_answer(g, h, p, x, answers_to_be_checked):
	status=True	
	if g**x % p <> h:
		#print "CHECK ANSWER!!!"
		#answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))
		status=False
		
	return status

#def dlp(g, h, p, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, prime_factors, powers, moduli, answers_to_be_checked):

#result = dlp(g,h,p, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked)

#def dlp(g, h, p, primefile, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_brute_force_soln):	

	#print('--------------------')

#	floor_sqrt_p = int(math.floor(math.sqrt(p)))
	#print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	#result=ghp_checks(g,h,p,floor_sqrt_p)
#	count_notprime = 0
	result=ghp_checks(g, h, p, floor_sqrt_p, count_notprime) 

	if result == 0:
		sys.exit()

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
		print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
		count_needlargerprimelist = count_needlargerprimelist + 1
		sys.exit()

	#define counts for different types of results
	count_nosolns=0
#	count_zi_bi_equal_1=0
#	count_bi_equal_1_zi_ntequal_0_1=0
	count_x_equals_0=0
#	count_Bi_equals_zi=0
	count_normal_soln=0
	#count_primroot_sub=0
	count_diffeq0=0
	count_brute_force_soln=0

	#define boolean values
	brute_force_status = False

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	# Brute Force Algorithm
	#result_brute_force = exponent_g_n(g,h,p)

	x=[]		
	x_moduli=[]

	print('Running brute force search to solve for x...')
	result = exponent_g_n(g,h,p)
	#return x, status
	#status=True for exponent found
	#status=False for exponent not found
	status=result[1]
	if status == True:
		brute_force_status == True
		x.append(result[0])
		print str(result[0])+" appended to x"
		diff=a_exp_x_eq_r(g,p,h)
		#return diff
		if diff==0:
			print 'Diff = 0 - No Solutions!!!'
			count_diffeq0 = count_diffeq0 + 1
			count_nosolns = count_nosolns + 1
			sys.exit()
		else:
			x_moduli.append(diff)
			print str(diff)+" appended to x_moduli"
			count_brute_force_soln=count_brute_force_soln + 1
	else:
		#exponent not found
		raw_input("Brute force alg failed to find x..")
		sys.exit()

	#print "x is: "+str(x)
	if g**x[0] % p <> h:
		print "CHECK ANSWER!!!"
		answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x[0]))

	x_final=x[0]
	x_moduli_final=x_moduli[0]

	return x_final, count_nosolns, count_x_equals_0, count_brute_force_soln, x_moduli_final, count_diffeq0
	
	#return x_final, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, x_moduli_final, count_diffeq0

def exponent_g_n(generator,h_value, p):

	n=1
	x=0
	status=False
	while n < p:
		#print "n is:"+str(n)
		if generator**n % p == h_value:
			x = n
			status=True
			break
		n = n + 1

	if x==0:
		x="No exponent found"
		status=False

	return x, status

def a_exp_x_eq_r(a,p,r):
	#print("Running a_exp_x_eq_r()..")
	x=1
	x_values=[]
	count=0
	diff=0
	for x in xrange(0,p):
		#print "count is: "+str(count)		
		if a**x % p == r:
			#print "a**x % p is: "+str(r)
			x_values.append(x)
			#print str(x)+" appended to x_values"
			count=count+1
			if count==2:
				#print "count is: "+str(count)
				#x_values.append(x)
				#print str(x)+" appended to x_values
				diff = x_values[1] - x_values[0]				
				#diff = answer2 - answer1
				#print "diff is: "+str(diff)
				break
		#x = x + 1
	return diff

def csvfile_store_primes(csv_filename_var):

	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		primes=list(z1)
		csvfile.close()	
	return primes

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()

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

