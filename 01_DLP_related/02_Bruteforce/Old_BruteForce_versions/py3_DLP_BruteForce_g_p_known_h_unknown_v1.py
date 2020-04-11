#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 1. 07/05/2018.
#Programmed & tested in Python 3.4.3 only
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
print("Version 1. 07/05/2018.")
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
	print('primefile currently is:',primefile)

	#print(sys.version_info)

	print('What is g?')
	g_initial = input()
	if g_initial.isdigit() is False:
		print('You have not entered a positive integer for g. g is: ',g_initial,'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = int(g_initial)

	#print('What is h?')
	#h_initial = input()
	#if h_initial.isdigit() is False:
	#	print('You have not entered a positive integer for h. h is: ',h_initial,'. Please reenter.')
	#	sys.exit()

	#now convert h into a long:
	#h = int(h_initial)

	print('What is p?')
	p_initial = input()
	if p_initial.isdigit() is False:
		print('You have not entered a positive integer for p. p is: ',p_initial,'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = int(p_initial)

	print("---------------------")
	#print("g: ",g,", h: ",h,", p: ",p)
	print("g:",g,", p:",p)

	#define counts for different types of results
	count_nosolns=0
	#count_zi_bi_equal_1=0
	#count_bi_equal_1_zi_ntequal_0_1=0
	#count_x_equals_0=0
	#count_Bi_equals_zi=0
	#count_normal_soln=0
	count_needlargerprimelist=0
	count_brute_force_soln=0	

	#define lists for different types of results
	answers_to_be_checked=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print("======================================")

	#Run checks on g, h & p	
	#result_ghp = ghp_checks(g, h, p) 
	result_ghp = ghp_checks(g, p)

	if result_ghp == 0:
		sys.exit()

	#print('Checking if a solution for x and h exists..')
	
	G_list=[]
	status = True
	for num in range(0,p):
		a = pow(g,num,p)
		#print("a is:",a)
		
		if num > 0 and num % 10000 == 0:
			print("number is:",num)
		if a not in G_list:
			G_list.append(a)
			#print(a,"appended to G_list")				
		elif a in G_list:
			break	

	#if len(G_list)< 10:
	#	print("G_list: ",G_list)

	#print("G_list: ",G_list)

	#if h not in G_list:
	#	status = False
	
	#consider all possible h_values			
	x_values = []	
	M_values = []
	for h in G_list:
		result_dlp = dlp(g, p, h, primefile, count_nosolns, count_needlargerprimelist, answers_to_be_checked, count_brute_force_soln)		
		#return x_final, count_nosolns, count_brute_force_soln, x_moduli_final

		x=result_dlp[0]
		M=result_dlp[3]
		
		#h_values.append(h)

		result=check_answer(g,h,p,x)
		if result==False:
			#status=False
			print("CHECK FAILED - g: ",g,", h: ",h,", p: ",p,", x: ",x,", M: ",M)
			sys.exit()
		#else:
			#print("======================================")
			#print("Final solution: x= ",x," mod ",M)
	
		x_values.append(x)	
		
		if M not in M_values:
			M_values.append(M)
		

	print("x_values:",x_values)
	print("M_values:",M_values)
	print("h_values:",G_list)

	#for x in x_values:
	#	i = x_values.index(x)	
	#	M_value = M_values[i]
	#	
	#	answer.append()

	#if status == False:
	#	print("Solution does not exist - h:",h," is not in G_list! - g: ",g,", h: ",h,", p: ",p)
	#	sys.exit()
	#else:
	#	print("Solution does exist -",h,"is in G_list")
	#	#sys.exit()
	
def ghp_checks(g,p):

	status=1
	
	#Need to check if p is prime
	#print('Checking if p is prime ..')
	a = isprime(p)	
	if a != True:
		print('The number entered for p: ',p,' is not prime. Please choose a number that is prime for p.')
		status=0
		#count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	#print('Running simple checks on g..')
	if (g==0 or p==0):
	#if (g==0 or h==0 or p==0):
		print('One or more numbers entered for g and p are 0. Please choose numbers that are not 0.')
		status=0
		sys.exit()
	elif g==1:
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
	elif g<0:
		print('Number for g is negative. Please enter another number')
		status=0
		sys.exit()	
	
	return status

def check_answer(g, h, p, x):
	#def check_answer(g, h, p, x, answers_to_be_checked):
	status=True	
	if g**x % p != h:
		#print "CHECK ANSWER!!!"
		#answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))
		status=False
		
	return status

def dlp(g, p, h, primefile, count_nosolns, count_needlargerprimelist, answers_to_be_checked, count_brute_force_soln):

#result = dlp(g,p,h, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked)

	#print('Running dlp(',g,',',p,',',h,')')

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
	#count_nosolns=0
	#count_x_equals_0=0
	#count_normal_soln=0
	#count_diffeq0=0
	#count_brute_force_soln=0

	#define boolean values
	brute_force_status = False

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	# Brute Force Algorithm
	#result_brute_force = exponent_g_n(g,h,p)

	x=[]		
	x_moduli=[]

	#print('Running brute force search to solve for x...')
	result = exponent_g_n(g,h,p)
	#return x, status
	#status=True for exponent found
	#status=False for exponent not found
	status=result[1]
	if status == True:
		brute_force_status == True
		x.append(result[0])
		#print(result[0],"appended to x")
		diff=a_exp_x_eq_r(g,p,h)
		#return diff
		if diff==0:
			#print('Diff = 0 - No Solutions!!!')
			count_diffeq0 = count_diffeq0 + 1
			count_nosolns = count_nosolns + 1
			sys.exit()
		else:
			x_moduli.append(diff)
			#print(diff,"appended to x_moduli")
			count_brute_force_soln=count_brute_force_soln + 1
	else:
		#exponent not found
		eval(input("Brute force alg failed to find x.."))
		sys.exit()

	#print "x is: "+str(x)
	if pow(g,x[0],p) != h:
		print("CHECK ANSWER!!!")
		answers_to_be_checked.append("g: ",g," h: ",h," p: ",p," x: ",x[0])

	x_final=x[0]
	x_moduli_final=x_moduli[0]

	return x_final, count_nosolns, count_brute_force_soln, x_moduli_final
	
	#return x_final, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, x_moduli_final, count_diffeq0

def exponent_g_n(generator,h_value, p):

	n=1
	x=0
	status=False
	while n < p:
		#print "n is:"+str(n)
		if pow(generator,n,p) == h_value:
			x = n
			status=True
			break
		n = n + 1

	if x==0:
		x="No exponent found"
		status=False

	return x, status

def a_exp_x_eq_r(g,p,h):
	#print("Running a_exp_x_eq_r(",g,",",p,",",h,")..")
	x=1
	x_values=[]
	count=0
	diff=0
	for x in range(0,2*p):
		#print "count is: "+str(count)		
		if pow(g, x, p) == h:
			#print "a**x % p is: "+str(r)
			x_values.append(x)
			#print str(x)+" appended to x_values"
			count = count + 1
			if count == 2:
				#print "count is: "+str(count)
				#x_values.append(x)
				#print str(x)+" appended to x_values
				diff = x_values[1] - x_values[0]				
				#diff = answer2 - answer1
				#print "diff is: "+str(diff)
				break
		#x = x + 1
	return diff

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
	if input_number > 2*(10**8):
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

