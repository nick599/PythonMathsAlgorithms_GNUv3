#Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.
#Version 12. 23/08/2019.
#Programmed & tested in Python 3.5.2 only
#This program attemps to solve a Discrete Log Problem (DLP) specified by user, via brute force of values for x. 
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v4.4.0 x86_64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

import sys
import math
import os
import itertools
import csv
import time

print("Copyright Nick Prowse 2019. Code Licenced under GNU GPL v3.")
print("Version 12. 23/08/2019.")
print("Programmed & tested in python 3.5.2 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via brute force of values of x")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v4.4.0 x86_64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")
	
def main():

	print('What is g?')
	g_initial = input()
	if g_initial.isdigit() is False:
		print('You have not entered a positive integer for g. g is: ',g_initial,'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = int(g_initial)

	print('What is p?')
	p_initial = input()
	if p_initial.isdigit() is False:
		print('You have not entered a positive integer for p. p is: ',p_initial,'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = int(p_initial)
	
	dlp_bruteforce(g,p)

def dlp_bruteforce(g,p):
	print("---------------------")
	print("g:",g,", p:",p)

	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_10000.csv"
	primefile=prime_list_path + prime_list_filename
	print('primefile currently is:',primefile)

	#print(sys.version_info)

	#define counts for different types of results
	count_nosolns=0
	count_needlargerprimelist=0
	count_brute_force_soln=0	
	#count_moduli=0

	#define lists for different types of results
	answers_to_be_checked=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	#print("======================================")

	#Run checks on g & p	 
	result_ghp = ghp_checks(g, p)

	if result_ghp == 0:
		sys.exit()

	primes=csvfile_store_primes(primefile)

	#check if sqrt_p > largest element in primes
	sqrt_p = math.sqrt(p)
	largest_prime = primes[-1]
	count_needlargerprimelist=0
	if sqrt_p > largest_prime:
		print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
		#count_needlargerprimelist = count_needlargerprimelist + 1
		sys.exit()

	#legendre_symbol_g_p
	ls_g_p = legendre_symbol_g_p(g,p)	
	print('legendre_symbol_g_p(',g,',',p,'): ',ls_g_p)

	#print('Checking if a solution for x and h exists..')
	
	G_list=[]
	status = True
	
	if g!=p:
		
		if g>p:
			g_new=g%p
			print("g:",g," was larger than p: ",p," hence revised g is:",g_new)
			print("Generating G_list..")
			for num in range(1,p):
				a = pow(g_new,num,p)
		
				if num % 10000 == 0:
					print("number is:",num)
				if a not in G_list:
					G_list.append(a)			
				elif a in G_list:
					break
		else: #g < p	
			print("Generating G_list..")
			for num in range(1,p):
				a = pow(g,num,p)
		
				if num % 10000 == 0:
					print("number is:",num)
				if a not in G_list:
					G_list.append(a)			
				elif a in G_list:
					break

		G_list.sort()
	
		#Calculate moduli for g & p (doesn't depend on value of h)
		x_moduli_final=carmichael_moduli(g,p)
		#return diff

		if x_moduli_final!=0:
			print("x_moduli_final:",x_moduli_final)
		else:
			print('x_moduli_final = 0 - No Solutions!!!')
			sys.exit()

	    #consider all possible h_values			
		x_values = []	
		for h in G_list:
			result_dlp = dlp(g, p, h, primefile, count_nosolns, count_needlargerprimelist, answers_to_be_checked, count_brute_force_soln, x_moduli_final, primes)		
		    #return x_final, count_nosolns, count_brute_force_soln, answers_to_be_checked

			x=result_dlp[0]
			count_brute_force_soln=result_dlp[2]
			
			result=check_answer(g,h,p,x)
			if result!=False:
				if x not in x_values:
					x_values.append(x)	
			else:	
				print("CHECK FAILED - g: ",g,", h: ",h,", p: ",p,", x: ",x,", M: ",x_moduli_final)
				sys.exit()
		
		print("x_values:")
		print(x_values)

		if len(Glist) < p-1:
			print("h_values - length:",len(Glist))
			print(G_list)
		else:
			print("h_values is all values from h = 1 to",p-1)


	elif g==p:
	    print("g is equal to p. h is thus arbitary!")

	
def ghp_checks(g,p):

	#print('Checking if p is prime ..')
	status=1
	
	#Need to check if p is prime
	#print('Checking if p is prime ..')
	#a = isprime(p)
	a = isprime_SO(p)
	
	if a != True:
		print('The number entered for p: ',p,' is not prime. Please choose a number that is prime for p.')
		#status=0
		#count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	if (g==0 or p==0):
		print('One or more numbers entered for g and p are 0. Please choose numbers that are not 0.')
		#status=0
		sys.exit()
	elif g==1:
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
		#status=0
		sys.exit()
	elif g<0:
		print('Number for g is negative. Please enter another number')
		#status=0
		sys.exit()
	elif p<0:
		print('Number for p is negative. Please enter another number')
		#status=0
		sys.exit()	
	
	return status

def check_answer(g, h, p, x):
	status=True	
	if g**x % p != h:
		#print "CHECK ANSWER!!!"
		#answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))
		status=False
		
	return status

def dlp(g, p, h, primefile, count_nosolns, count_needlargerprimelist, answers_to_be_checked, count_brute_force_soln, x_moduli_final, primes):

#result = dlp(g,p,h, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked)

	if h % 200 == 1:
		print('Running dlp(',g,',',p,',',h,')')

	#define boolean values
	brute_force_status = False

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.
	
	# Brute Force Algorithm
	x=[]		

	#print('Running brute force search to solve for x...')
	result = exponent_g_n(g,h,p)
	#return x, status
	#status=True for exponent found, status=False for exponent not found
	status=result[1]
	if status == True:
		brute_force_status == True
		x.append(result[0])
		#print(result[0],"appended to x")
		
		count_brute_force_soln=count_brute_force_soln + 1

		#print "x is: "+str(x)
		if pow(g,x[0],p) != h:
			print("CHECK ANSWER!!!")
			answers_to_be_checked.append("g: ",g," h: ",h," p: ",p," x: ",x[0])

		x_final=x[0]
	else:
		#exponent not found
		print("Brute force alg failed to find x..")
		sys.exit()

	return x_final, count_nosolns, count_brute_force_soln, answers_to_be_checked

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

def carmichael_moduli(g,p):
	#print("Running carmichael_moduli(",g,",",p,",)..")
	x=1
	x_values=[]
	count=0
	diff=0
	for x in range(1,2*p):
		#print ("x is: ",str(x),",count is: ",str(count))		
		if pow(g, x, p) == 1:
			#print ("pow(g, x, p) = pow(",g,", ",x,", ",p,") = 1")
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

def isprime_SO(p):		#this is O(sqrt(n))
	
	#print("Running isprime(",p,")..")
	# http://stackoverflow.com/questions/4545114/quickly-determine-if-a-number-is-prime-in-python-for-numbers-1-billion
	
	if p<=100:
		return p in primes_under_100

	if p % 2 ==0 or p % 3 == 0:
		return False	
	
	temp=int(p ** .5)
	#for f in range(5, int(p ** .5),6):
	for f in range(5, temp, 6):
		if p % f == 0 or p % (f+2) == 0:
			return False
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

def legendre_symbol_g_p(g,p):

	#print('Running legendre_symbol_g_p(',g,',',p,')...')

	#outputs the legendre symbol (g over p) for inputs g and p 
	#legendre_g_p(g over p) == -1 when g is a quadratic residue mod p and g % p !=0 
	#legendre_g_p(g over p) == 1 when g is a non-quadratic residue mod p
	#legendre_g_p(g over p) == 0 when g % p = 0

	power=int((p-1)/2)
	#print('power:',power)

	legendre_symbol_g_p=pow(g,power,p)

	if legendre_symbol_g_p > 1:
		legendre_symbol_g_p = legendre_symbol_g_p - p
	
	return legendre_symbol_g_p

if __name__=='__main__':
	#main()
	#dlp_bruteforce(51,1009) - circa 1 sec
	dlp_bruteforce(513,100907)

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

#def a_exp_x_eq_r(g,p,h):
#	#print("Running a_exp_x_eq_r(",g,",",p,",",h,")..")
#	x=1
#	x_values=[]
#	count=0
#	diff=0
#	for x in range(0,2*p):
#		#print "count is: "+str(count)		
#		if pow(g, x, p) == h:
#			#print "a**x % p is: "+str(r)
#			x_values.append(x)
#			#print str(x)+" appended to x_values"
#			count = count + 1
#			if count == 2:
#				#print "count is: "+str(count)
#				#x_values.append(x)
#				#print str(x)+" appended to x_values
#				diff = x_values[1] - x_values[0]				
#				#diff = answer2 - answer1
#				#print "diff is: "+str(diff)
#				break
#		#x = x + 1
#	return diff
