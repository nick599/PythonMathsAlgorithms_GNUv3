#Copyright Nick Prowse 2017. Code Licenced under GNU GPL3.
#Version 4. 21/01/2018.
#Programmed & tested in Python 2.76 only
#This program attempts to factorise a number N specified by user, via wheel-factorisation using a 2,3,5-wheel. 
#Results printed are three arrays - first for prime factors, second for powers of those primes, third for any remainder (where a larger prime list is needed).
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second.

import sys
import math
import csv
import os
import itertools
import time
	
def main():
	#prime_list_path="/home/mint/Desktop/"
	#prime_list_filename="primes_upto_100000.csv"
	#primefile=prime_list_path + prime_list_filename

	print "Copyright Nick Prowse 2017. Code Licenced under GNU GPL3."
	print "Version 4. 21/01/2018."
	print "Programmed & tested in Python 2.76 only."
	print "This program attempts to factorise a number N specified by user, via wheel-factorisation using a 2,3,5-wheel." 
	print "Results printed are three arrays - first for prime factors, second for powers of those primes."
	#print "Prime list file should be a .CSV file with each prime separated by commas."
	#print "Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used."
	#print "The larger the prime file is that is used, the longer the factorisation will take!"
	print "It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to factorise most numbers under 2.5x10^9 in 1 second." 
	print "---------------------------------------------------------------------"
	
	#Check if primefile exists.
	#if os.path.exists(primefile) is False:
	#	#File doesn't exist in location. Exit process.
	#	print('Prime file doesn\'t exist in location specified. Exiting.')
	#	sys.exit()

	#print('Using primefile: '+str(primefile))
	
	print('Number to attempt to factorise?')
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()	

	#now convert type for N into a long:
	N = long(N_initial)

	#call number_checks() for simple checks on input 
	number_checks(N)	
	
	#Call size_input_check() if want to stop program running for very large numbers 
	#size_input_check()

	result1 = factorise(N)
	#return factors, c_factorisations
	factors = result1[0]
	c_factorisations = result1[1]

	print "factors are: "+str(factors)
	print "time for factorisation is: "+str(c_factorisations)
	
	result2 = calc_powers(factors)
	#return prime_factors, powers, c_calc_powers		
	prime_factors = result2[0]
	powers = result2[1]
	c_calc_powers = result2[2]
	total_calc_time = c_factorisations + c_calc_powers

	print "prime factors are: "+str(prime_factors)
	print "powers are: "+str(powers)
	print "time for calc prime factors & powers is: "+str(c_calc_powers)
	print "total calc time is: "+str(total_calc_time)

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	print "Running factorise().."	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.clock()	
	factors = []
	#c_lists = time.clock() - s_before_lists

	#print "Calculating prime factors and powers"
	s_before_factorisations = time.clock()	
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
	if N > 1: factors.append(N)
		
	c_factorisations = time.clock() - s_before_factorisations

	#print "factors are: "+str(factors)
	#print "c_factorisations are: "+str(c_factorisations)

	#raw_input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem

def calc_powers(factors):
	#print "------------------"
	print "Running calc_powers.."
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]
	powers = []
	fac_list = []
	count = 0
	c_primefactors_powers = 0
	s_before_calc_powers = time.clock()	
	for factor in factors:		
		#print "------------------"	
		#print "factor is: "+str(factor)		
		if fac_list:
			#temp factor list for comparisons has values
			if factor in fac_list:
				#print str(factor)+" is in fac_list"
				count += 1
				#print "count is: "+str(count)
				#temp_factor, temp_count = factor, count
				#print temp_factor, temp_count
			else:
				#factor is not in fac_list
				#add factor to prime_factors
				prime_factors.append(factor)
				#print "Added "+str(factor)+" to prime_factors"
				#print "prime_factors is: "+str(prime_factors)
				#add current count to powers for previous factor
				#print "count is: "+str(count)
				powers.append(count)
				#print "Added "+str(count)+" to powers for previous factor"
				#count = 0
				#print str(factor)+" is NOT in fac_list"
				#append it				
				fac_list.append(factor)	
				#count += 1
				count = 1
				#print "count is: "+str(count)
				#print "fac_list is: "+str(fac_list)
				
		else:
			#temp factor list for comparisons is empty
			#store 1st factor
			#print "fac_list is empty"
			fac_list.append(factor)
			#print str(factor)+" added to fac_list"
			prime_factors.append(factor)
			#print "Added "+str(factor)+" to prime_factors"
			#print "prime_factors is: "+str(prime_factors)			
			count += 1
			#print "count is: "+str(count)	

	#add count to powers for the last factor and the last factor
	#prime_factors.append(factor)
	#print "Added "+str(factor)+" to prime_factors"
	#print "prime_factors are: "+str(prime_factors)
	powers.append(count)
	#print "Added "+str(count)+" to powers for previous factor"
	#print "powers are: "+str(powers)

	#prime_factors = fs
	
	#print "prime_factors are: "+str(prime_factors)
	#print "powers are: "+str(powers)

	#raw_input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	c_calc_powers = time.clock() - s_before_calc_powers

	return prime_factors, powers, c_calc_powers

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

#def MaxPower(i,N):
#	print "Running MaxPower("+str(i)+","+str(N)+").."
#	m=0
#	while N > 1 and not N % i:	
#		m += 1		
#		N //= i
#	return m

#def max_element_below_or_equal_target(List,target):
	#bool1=False

	#List = primes
	#target = 25

	#raw_input("Waiting for user.. problem in max_element_below_or_equal_target()")
#	if target in List:
		#print 'target is: '+str(target)
		#print 'List.index(target) is: '+str(List.index(target))
		#return List.index(target)
#		return List.index(target) + 1
#	elif target > List[-1]:
		#Target value is not in list. Return index of last number in list.
		#bool1=True
		#return List.index(List[-1])
#		return List.index(List[-1]) + 1
	#elif target < 2:
	#	return ""
#	elif target < List[-1]:
		#Target value is less than largest prime in list
		# start from 2 and increase until last number is found that is less than target.
#		i=0
#		while List[i] < target:
#			i = i + 1 
		#return i
#		return i
#	else:
#		print 'List[-1] is: '+str(List[-1])
#		print 'target is: '+str(target)	
#		print "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))
#		return "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))



#def csvfile_store_primes(csv_filename_var):
#
#	with open(csv_filename_var,'r') as csvfile:
#		# Want to limit highest prime imported from csv to be <= math.sqrt(N)
#		# Need to get index of the highest prime <= math.sqrt(N)
#		# Strip quotes, eol chars etc, and convert strings to integers
#		#Use generator to get number of primes to use in prime file..
#		print 'Running generator..'
#		z1=(int(x) for row in csv.reader(csvfile) for x in row)
#		primes=list(z1)
#		csvfile.close()	
#	return primes

#def xrange_mod(start=0,stop=None,step=1):
#	if stop is None: 	
#		stop=start
#		start=0
#	i=start
#	while i < stop:
#		#function returns a generator i
#		yield i
#		i += step

#def MaxPower(i,N_remainder):
#	m=1
#	MxP=1
#	for n in xrange_mod(2, N_remainder + 1,1):	
#		b = i**n		
#		a = N_remainder % b
#		if a==0: 	
#			m = m+1					
#		else: 
#			MxP = m
#			break
#	return MxP

	

