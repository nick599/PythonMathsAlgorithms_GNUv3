#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 22/04/2018.
#Programmed & tested in Python 2.76 only
#This program creates a prime list of Safe Primes (2*p+1) in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
#import math
import csv
import os.path

print "Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3."
print "Version 1. 22/04/2018."
print "Programmed & tested in Python 2.76 only."
print "This program creates a prime list of Twin Primes () in CSV format with comma delimiter for all primes upto N inclusive based on an input file presuming containing files of length N."
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
	
	Primes_filename = "primes_upto_100000.csv"
	Primes_filepath = desktop_path + Primes_filename
	
	primes = csvfile_store_primes(Primes_filepath)

	if N % 2 == 0:
		#N is even
		number = N/2
	else:
		#N is odd
		number = (N-1)/2 - 1

	print "number is: "+str(number)+" .."	

	Twin_prime_candidates = []
	Twin_primes = []
	print "Looping through list of primes in "+str(desktop_path)+" .."
	for prime in primes:
		Twin_prime_candidates = []
		if primes.index(prime) +1 <= number:
			#candidate = prime + 2
			if isprime(prime + 2) == True:
				#prime + 2 is a prime
				Twin_prime_candidates.append(prime)
				Twin_prime_candidates.append(prime + 2)
				Twin_primes.append(Twin_prime_candidates)
					
				#twin_primes_to_add = "("+str(prime)+", "+str(prime+2)+")"
				#Twin_primes.append(twin_primes_to_add)

	print 'len Twin_primes is: '+str(len(Twin_primes))
	print 'First 10 Twin_primes are: '+str(Twin_primes[0:10])
	print 'Last 10 Twin_primes are: '+str(Twin_primes[-10:])

	#next_mem_usage_Kb = round(float(result[1])/ 1024, 1)
	#sieve_mem_usage_Kb = round(float(result[2]) / 1024, 1)
	#primes_mem_usage_Kb = round(float(result[3]) / 1024, 1)
	#final_mem_usage_Kb = round(float(result[4]) / 1024, 1)
	#isprime_mem_usage_Kb = round(float(result[5]) / 1024, 1)
	#primes = result[6]

	Twinprimes_filename = 'Twin_primes_upto_'+str(N)+'.csv'
	Twinprimes_filepath = desktop_path + Twinprimes_filename
	#print 'First 10 primes are: '+str(primes[0:10])
	#print 'Last 10 primes are: '+str(primes[-10:])
	
	print "Running checks on twin primes file .."
	#Check if primefile already exists.
	if os.path.exists(Twinprimes_filename) is True: 
		print "Twin primes file already exists in that location. Existing Twin primes file will be deleted before new one is created."
		os.remove(Twinprimes_filename)
		
	print "Now creating file for Twin primes upto "+str(N)		
	csvfile_create(Twin_primes, Twinprimes_filepath)
	print str(Twinprimes_filename)+" created."

	#next_mem_usage = sys.getsizeof(next)
	#sieve_mem_usage = sys.getsizeof(sieve)
	#primes_mem_usage = sys.getsizeof(primes)
	#final_list_mem_usage = sys.getsizeof(final_list)
	
	#print'End memory used by is_prime list: '+str(isprime_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by last next list: '+str(next_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by last sieve list: '+str(sieve_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by primes list: '+str(primes_mem_usage_Kb)+' Kbytes.'
	#print'End memory used by final_list: '+str(final_mem_usage_Kb)+' Kbytes.'


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
