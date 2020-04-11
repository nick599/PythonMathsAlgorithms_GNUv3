#Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3.
#Version 1. 03/04/2018.
#Programmed & tested in Python 2.76 only
#This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
import math
import csv
import os.path

print "Copyright Nick Prowse 2017. Code Licenced under GNU GPL v3."
print "Version 1. 03/04/2018."
print "Programmed & tested in Python 2.76 only."
print "This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
print "It has been tested on Linux Mint v3.19 x64."
print "Using Lists instead of sets for storage to minimise memory usage."
print "---------------------------------------------------------------------"

def main():
	#store size of L1 CPU cache in bytes
	L1D_CACHE_SIZE = 32768 #32*1024 = 32Kbytes	
	
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

	#Store square root of N rounded to integer
	#sqrt_N = int(math.sqrt(N))

	#Set segment_size to be max of CPU's L1 data cache size and sqrt_N
	#segment_size = max(L1D_CACHE_SIZE,sqrt_N)

	#limit = N

	desktop_path = "/home/mint/Desktop/"
	
	Primes_filename = "primes_upto_100000.csv"
	Primes_filepath = desktop_path + prime_list_filename
	
	print "Looping through list of primes in "+str(desktop_path)+" .."
	result = SG_prime_canditates_Creation(N/2,)
	#return SG_prime_candidates
	SG_prime_candidates = result[0]
	
	print 'First 10 SG_prime_candidates are: '+str(SG_prime_candidates[0:10])
	print 'Last 10 SG_prime_candidates are: '+str(SG_prime_candidates[-10:])

	next_mem_usage_Kb = round(float(result[1])/ 1024, 1)
	sieve_mem_usage_Kb = round(float(result[2]) / 1024, 1)
	primes_mem_usage_Kb = round(float(result[3]) / 1024, 1)
	final_mem_usage_Kb = round(float(result[4]) / 1024, 1)
	isprime_mem_usage_Kb = round(float(result[5]) / 1024, 1)
	primes = result[6]

	Safeprimes_filename = 'Safe_primes_upto_'+str(N)+'.csv'
	Safeprimes_filepath = desktop_path + prime_list_filename
	#print 'First 10 primes are: '+str(primes[0:10])
	#print 'Last 10 primes are: '+str(primes[-10:])
	
	print "Running checks on primefile .."
	#Check if primefile already exists.
	if os.path.exists(primefile) is True: 
		print "Prime file already exists in that location. Existing prime file will be deleted before new one is created."
		os.remove(primefile)
		
	print "Now creating file for primes in prime list upto "+str(N)		
	csvfile_create(SG_prime_candidates, Safeprimes_filepath)
	print str(Safeprimes_filename)+" created."

	print'End memory used by is_prime list: '+str(isprime_mem_usage_Kb)+' Kbytes.'
	print'End memory used by last next list: '+str(next_mem_usage_Kb)+' Kbytes.'
	print'End memory used by last sieve list: '+str(sieve_mem_usage_Kb)+' Kbytes.'
	print'End memory used by primes list: '+str(primes_mem_usage_Kb)+' Kbytes.'
	print'End memory used by final_list: '+str(final_mem_usage_Kb)+' Kbytes.'

def SG_prime_canditates_Creation(N, limit):



	return SG_prime_candidates


def sieving(sqrt_N, segment_size, limit):
	if limit < 2:
		count=0
	else:
		count=1

	#Now need to generate sieving primes less than sqrt_N - which are needed to cross off multiples
	is_prime = [1] * (sqrt_N + 1) 
	
	print 'Running is_prime[] ..'
	i = 2
	while i * i <= sqrt_N:
		#print('i is: '+str(i))		
		if is_prime[i]: 		
			j = i * i				
			while j <= sqrt_N: 					
				is_prime[j] = 0  
				j = j + i	
		i = i + 1

	isprime_mem_usage = sys.getsizeof(is_prime)

	#print'Initialising lists and values ..'
	sieve=[]
	primes = []
	next = []
	low = 0	
	s = 3
	n = 3
	print'Sieving ..'
	while low <= limit: 
		#Populate sieve 
		#print('---------------------')
		sieve = list(xrange(low,low + segment_size + 1))
		high = min(low + segment_size - 1, limit)
		
		#add new sieving primes <= sqrt(high)
		while s * s < high:
			if is_prime[s]: 
				primes.append(s)
				next.append(s * s - low)
			s = s + 2

		#sieve the current segment
		primes_size = len(primes)
		
		i=0		
		#primes_size = primes.size()		
		while i < primes_size:
			#print('i is: '+str(i))	
			j = next[i]
			#print('j = next['+str(i)+'] is: '+str(j))
			k = primes[i] * 2
			while j < segment_size:		
				sieve[j] = 0
				j = j + k
			next[i]= j - segment_size
			i = i + 1 

		if low == 0:		
			final_list=[2]

		while n <= high:
			if (sieve[n - low]): #n is a prime
				final_list.append(n)				
				count = count + 1
			n = n + 2

		low = low + segment_size
	
	next_mem_usage = sys.getsizeof(next)
	sieve_mem_usage = sys.getsizeof(sieve)
	primes_mem_usage = sys.getsizeof(primes)
	final_list_mem_usage = sys.getsizeof(final_list)
	
	return final_list, next_mem_usage, sieve_mem_usage, primes_mem_usage, final_list_mem_usage, isprime_mem_usage, primes

def csvfile_create(data,filepath):
	#create csv file using data
	with open(filepath,'wb') as csvfile:
		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
		wr.writerow(data)		
		csvfile.close()	

if __name__=='__main__':
	main()
