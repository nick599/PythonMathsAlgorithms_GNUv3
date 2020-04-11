#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 18/05/2018.
#Programmed & tested in Python 3,14 only
#This program creates a list of Beta-Smooth numbers in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
#import math
import csv
import os.path

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version 1. 18/05/2018.")
print("Programmed & tested in Python 3.14 only.")
print("This program creates a list of Beta-smooth numbers in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.")
print("It has been tested on Linux Mint v3.19 x64.")
#print("Using Lists instead of sets for storage to minimise memory usage.")
print("---------------------------------------------------------------------")

desktop_path = "/home/mint/Desktop/"
Primes_filename = "primes_upto_10000.csv"
Primes_filepath = desktop_path + Primes_filename	

def main():
	#store size of L1 CPU cache in bytes
	#L1D_CACHE_SIZE = 32768 #32*1024 = 32Kbytes	
	
	print("What is the largest number (N) you want to go upto for primes to create the B-Smooth numbers list?")	
	N_initial = input()
	if N_initial.isdigit() is False:
		print("You have not entered an integer for N. Exiting..")
		sys.exit()

	#now convert type for N into a long:
	N = int(N_initial)
	
	print("N is:",N,"..")	

	#Simple Checks for N:
	if N==0:
		print("Number entered is 0. Please choose another number.")
		sys.exit()
	if N==1:
		print("1 is not a prime. Please choose another number.")
		sys.exit()
	if N<0:
		print("Number entered is negative. Please enter another number")
		sys.exit()

	print("What is the value of Beta?")
	beta_initial = input()
	if beta_initial.isdigit() is False:
		print("You have not entered an integer for beta. Exiting..")
		sys.exit()

	#now convert type for beta into a long:
	beta = int(beta_initial)
	
	print("Beta is:",beta,"..")	
	
	primes = csvfile_store_primes(Primes_filepath)

	#if N % 2 == 0:
		#N is even
	#	number = N/2
	#else:
		#N is odd
	#	number = (N-1)/2 - 1

	#print("number is: "+str(number)+" ..")	

	#need to get index of beta in primes list
	beta_index = primes.index(beta)

	print("beta_index:",beta_index)

	pminus1_Beta_Smooth_candidates = []
	print("Looping through list of primes in ",desktop_path," ..")
	for prime in primes:
		if primes.index(prime) + 1 <= N:
			candidate = prime - 1
			if B_Smooth(candidate, primes, beta, beta_index) == True:
				#pminus1 is Beta-Smooth
				pminus1_Beta_Smooth_candidates.append(candidate)

	#SG_prime_candidates = result[0]
	
	print('len pminus1_5smooth_candidates is:',len(pminus1_Beta_smooth_candidates))
	print('First 10 pminus1_5smooth_candidates are:',pminus1_Beta_smooth_candidates[0:10])
	print('Last 10 pminus1_5smooth_candidates are:',pminus1_Beta_smooth_candidates[-10:])

	#next_mem_usage_Kb = round(float(result[1])/ 1024, 1)
	#sieve_mem_usage_Kb = round(float(result[2]) / 1024, 1)
	#primes_mem_usage_Kb = round(float(result[3]) / 1024, 1)
	#final_mem_usage_Kb = round(float(result[4]) / 1024, 1)
	#isprime_mem_usage_Kb = round(float(result[5]) / 1024, 1)
	#primes = result[6]

	Beta_Smooth_filename = 'Beta_Smooth_upto_'+str(N)+'.csv'
	Beta_Smooth_filepath = desktop_path + Beta_Smooth_filename
	#print 'First 10 primes are: '+str(primes[0:10])
	#print 'Last 10 primes are: '+str(primes[-10:])
	
	print("Running checks on Beta-Smooth file ..")
	#Check if primefile already exists.
	if os.path.exists(Beta_Smooth_filepath) is True: 
		print("Beta-smooth file already exists in that location. Existing file will be deleted before new one is created.")
		os.remove(Beta_Smooth_filepath)
		
	print("Now creating file for Beta-Smooth numbers upto ",N)		
	csvfile_create(pminus1_Beta_Smooth_candidates, Beta_Smooth_filepath)
	print(Beta_Smooth_filename," created.")

	#next_mem_usage = sys.getsizeof(next)
	#sieve_mem_usage = sys.getsizeof(sieve)
	#primes_mem_usage = sys.getsizeof(primes)
	#final_list_mem_usage = sys.getsizeof(final_list)
	
	#print'End memory used by is_prime list: '+str(isprime_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by last next list: '+str(next_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by last sieve list: '+str(sieve_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by primes list: '+str(primes_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by final_list: '+str(final_mem_usage_Kb)+' Kbytes.'


#def isprime(p):		#this is O(sqrt(n))
	
	#print "Running isprime("+str(p)+").."
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
#	if p==1:
#		return False	
		
#	i = 2
#	while i*i <= p:
#		if p % i == 0:
#			return False
#		i += 1

#	return True

def B_Smooth(candidate, primes, beta, beta_index):
	status=False

	print("beta:",beta,", beta_index:",beta_index)
	#print("type(beta):",type(beta))

	#set list for beta-smooth check
	smooth_numbers = primes[0:beta_index+1]

	print("smooth_numbers:",smooth_numbers)

	#test if candidate is Beta-smooth
	factors = factorise(candidate)
	
	print("factors:",factors)

	prime_factors = []
	for factor in factors:
		if factor not in prime_factors:
			prime_factors.append(factor)

	print("prime factors:",prime_factors)

	if candidate in prime_factors and candidate <= beta:
		print(candidate," is ",beta,"- smooth")
		input("Waiting for user")
		return True
	else:
		print(candidate," is NOT ",beta,"- smooth")
		input("Waiting for user")
		return False

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print "Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.clock()	
	factors = []
	#c_lists = time.clock() - s_before_lists

	#print "Calculating prime factors and powers"
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]
	length, cycle = 11,3
	f, factors, next = 2, [], 0
	#s_before_factorisations = time.clock()
	while f*f <= N:
		while N % f == 0:		
			#f is a factor. Add factor f to fs
			factors.append(f)
			#print "appended "+str(f)+" to factors.."
			N /= f
		f += gaps[next]		
		next += 1
		if next == length:
			next = cycle
	if N > 1: factors.append(N)
		
	#c_factorisations = time.clock() - s_before_factorisations

	#print "factors are: "+str(factors)
	#print "c_factorisations are: "+str(c_factorisations)

	#raw_input("Waiting for user..")	

	return factors

def csvfile_store_primes(csv_filename_var):		### Assumming O(n+len(z1)+1) ### 
		
	print('Importing primes from csv file..')
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to getse) number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)			#O(n) - Potentially y rows and x items in each row, 
											# however only 1 row in csvfile being used. Hence x*y=x items to store
		primes=list(z1)								#O(len(z1))
		csvfile.close()								#1 operation
	return primes

def csvfile_create(data,filepath):
	#create csv file using data
	with open(filepath,'wb') as csvfile:
		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
		wr.writerow(data)		
		csvfile.close()	

if __name__=='__main__':
	main()
