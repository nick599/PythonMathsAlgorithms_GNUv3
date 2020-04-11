#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 2. 04/04/2018.
#Programmed & tested in Python 2.76 only
#This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
import math
import csv
import os.path
import time

print "Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3."
print "Version 2. 04/04/2018."
print "Programmed & tested in Python 2.76 only."
print "This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N."
print "It has been tested on Linux Mint v3.19 x64."
print "Using Lists instead of sets for storage to minimise memory usage."
print "---------------------------------------------------------------------"

def main():
	print "What is the largest number you want primes to go upto in the prime list?"	
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print "You have not entered an integer. Please reenter."
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)
	
	#Simple Checks for N:
	if N==0:
		print "Number entered is 0. Please choose another number."
		sys.exit()
	if N==1:
		print "1 is not a prime. Please choose another number."
		sys.exit()
	if N<0:
		print "Number entered is negative. Please enter another number"
		sys.exit()

	desktop_path = "/home/mint/Desktop/"
	
	Primes_filename = "primes_upto_10000000.csv"
	Primes_filepath = desktop_path + Primes_filename
	
	primes = csvfile_store_primes(Primes_filepath)

	#result = Lucas_lehmer(7)
	#print "Lucas_lehmer(7) is: "+str(result)
	#raw_input("Waiting for user..")
	
	print "Running 1st comparison.. "

	candidates = CreateMersenneCandidates(N)
	print "Candidates is: "+str(candidates)
	print "Number of candidates is: "+str(len(candidates))
	mersenne_primes = []
	s_before_result_CMC_LL = time.clock()
	for candidate in candidates:
		print "candidate is now: "+str(candidate)		
		if Lucas_lehmer(candidate) == True:	
			#candidate is a Mersenne Prime
			print str(candidate)+" is prime"
			mersenne_primes.append(candidate)

	#result = checkprimality(candidates)
	c_result_CMC_LL = time.clock() - s_before_result_CMC_LL

	print "mersenne_primes upto "+str(N)+" are: "+str(mersenne_primes)
	print 'c_result_CMC_LL is: '+str(c_result_CMC_LL)

	print "Running 2nd comparison.. "

	s_before_result_MathLog = time.clock()
	result_MathLog = Mersenne_prime_create_math_log(N, primes)
	c_result_MathLog = time.clock() - s_before_result_MathLog

	print 'c_result_MathLog is: '+str(c_result_MathLog)

	print "Running 3rd comparison.. "

	s_before_result_LL = time.clock()
	result_LL = Mersenne_prime_create_LL(N, primes)
	c_result_LL = time.clock() - s_before_result_LL

	print 'c_result_LL is: '+str(c_result_LL)

	#print 'len Mersenne_prime_candidates ia: '+str(len(Mersenne_prime_candidates))
	#print 'First 10 Mersenne_prime_candidates are: '+str(Mersenne_prime_candidates[0:10])
	#print 'Last 10 Mersenne_prime_candidates are: '+str(Mersenne_prime_candidates[-10:])

	#next_mem_usage_Kb = round(float(result[1])/ 1024, 1)
	#sieve_mem_usage_Kb = round(float(result[2]) / 1024, 1)
	#primes_mem_usage_Kb = round(float(result[3]) / 1024, 1)
	#final_mem_usage_Kb = round(float(result[4]) / 1024, 1)
	#isprime_mem_usage_Kb = round(float(result[5]) / 1024, 1)
	#primes = result[6]

	Mersenne_filename = 'Mersenne_primes_upto_'+str(N)+'.csv'
	Mersenne_filepath = desktop_path + Mersenne_filename
	#print 'First 10 primes are: '+str(primes[0:10])
	#print 'Last 10 primes are: '+str(primes[-10:])
	
	print "Running checks on Mersenne primes file .."
	#Check if primefile already exists.
	if os.path.exists(Mersenne_filename) is True: 
		print "Mersenne primes file already exists in that location. Existing Mersenne primes file will be deleted before new one is created."
		os.remove(Mersenne_filename)
		
	print "Now creating file for Mersenne primes upto "+str(N)		
	csvfile_create(Mersenne_prime_candidates, Mersenne_filepath)
	print str(Mersenne_filename)+" created."

	#next_mem_usage = sys.getsizeof(next)
	#sieve_mem_usage = sys.getsizeof(sieve)
	#primes_mem_usage = sys.getsizeof(primes)
	#final_list_mem_usage = sys.getsizeof(final_list)
	
	#print'End memory used by is_prime list: '+str(isprime_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by last next list: '+str(next_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by last sieve list: '+str(sieve_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by primes list: '+str(primes_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by final_list: '+str(final_mem_usage_Kb)+' Kbytes.'

def CreateMersenneCandidates(N):

	candidates=[]
	for number in xrange(2,N+1):
		candidate = pow(2,number) - 1
		if candidate <= N:		
			candidates.append(candidate)
			#print str(candidate)+" added to candidates"
		else:
			break
	return candidates

def Mersenne_prime_create_math_log(N, primes):
	#if N % 2 == 0:
	#	#N is even
	#	number = N/2
	#else:
	#	#N is odd
	#	number = (N-1)/2 - 1
	#
	#print "number is: "+str(number)+" .."	

	Mersenne_prime_candidates=[]
	for prime in primes:
		prime_index = primes.index(prime) + 1
		if prime_index % 20000 == 0:
			print "Prime index is: "+str(prime_index)		

		if primes.index(prime)+1 <= N:
			candidate = math.log((prime+1),2)
			if candidate - int(candidate) == 0:
				#Candidate is a Mersenne prime				
				#candidate = int(candidate)
				Mersenne_prime_candidates.append(prime)

	#Mersenne_prime_candidates = result[0]
	return Mersenne_prime_candidates	

def Lucas_lehmer(p):

	print "p is: "+str(p)	
	s = 4
	M = pow(2,p) - 1
	#print "M initial is: "+str(M)	
	for number in xrange(0, p-2):
		s = (s*s - 2) % M
		#print "s is now: "+str(s)

	if s == 0:
		#print str(p)+" is prime"
		return True
	else:
		return False


def Mersenne_prime_create_LL(N, primes):
	Mersenne_prime_candidates = []
	#print "Looping through list of primes in "+str(desktop_path)+" .."
	for prime in primes:
		if prime <= N:			
			prime_index = primes.index(prime) + 1
			if prime_index % 50 == 0:
				print "Prime index is: "+str(prime_index)		 
			if Lucas_lehmer(prime) == True:
			#result = Lucas_lehmer(prime)
			#if result == True:
				#Candidate is a Mersenne prime
				Mersenne_prime_candidates.append(prime)

	return Mersenne_prime_candidates


def isprime(p):		#this is O(sqrt(n))
	
	#print "Running isprime("+str(p)+").."
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	return True

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
