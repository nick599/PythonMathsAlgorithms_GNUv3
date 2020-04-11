# 24/04/2018
# Version 1
# Licenced under GNU GPL v3
# python3

#import sys
#import math
#import os
#import itertools
import csv
import time

def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	print("primefile currently is: ",primefile)

	primes = csvfile_store_primes(primefile)

	test_range_hundred = range(1,101)
	test_range_thousand = range(1,1001)
	test_range_tenthousand = range(1,10001)
	test_range_hundredthousand = range(1,100001)
	#test_range_million = range(1,1000001)
	p_values_hundred = primes[0:101]
	p_values_thousand = primes[0:1001]
	p_values_tenthousand = primes[0:10001]
	p_values_hundredthousand = primes[0:100001]

	s_divmod_before = time.clock()
	for num in test_range_hundred:
		for p in p_values_hundred:		
			result = divmod(num, p)
			a_dblslash_p = result[0]
			a_mod_p = result[1]

	c_divmod_tot_time = time.clock() - s_divmod_before 
	c_divmod_tot_time_rounded = round(c_divmod_tot_time,4)
	print("c_divmod_tot_time_hundred_rounded:",c_divmod_tot_time_rounded)

	s_percent_slashes_before = time.clock()
	for num in test_range_hundred:
		for p in p_values_hundred:		
			a_dblslash_p = num // p
			a_mod_p = num % p

	c_percent_slashes_tot_time = time.clock() - s_percent_slashes_before 
	c_percent_slashes_tot_time_rounded = round(c_percent_slashes_tot_time,4)
	print("c_percent_slashes_tot_time_hundred:",c_percent_slashes_tot_time_rounded)

	c_ratio_tot_time_hundred = float(c_divmod_tot_time) / c_percent_slashes_tot_time 
	c_ratio_tot_time_hundred = round(c_ratio_tot_time_hundred,3)
	print("c_ratio_tot_time_hundred:",c_ratio_tot_time_hundred)

	print("----------------------------------")	

	s_divmod_before = time.clock()
	for num in test_range_thousand:
		for p in p_values_thousand:		
			result = divmod(num, p)
			a_dblslash_p = result[0]
			a_mod_p = result[1]

	c_divmod_tot_time = time.clock() - s_divmod_before 
	c_divmod_tot_time = round(c_divmod_tot_time,4)
	print("c_divmod_tot_time_thousand:",c_divmod_tot_time)

	s_percent_slashes_before = time.clock()
	for num in test_range_thousand:
		for p in p_values_thousand:		
			a_dblslash_p = num // p
			a_mod_p = num % p

	c_percent_slashes_tot_time = time.clock() - s_percent_slashes_before 
	c_percent_slashes_tot_time_rounded = round(c_percent_slashes_tot_time,4)
	print("c_percent_slashes_tot_time_thousand:",c_percent_slashes_tot_time_rounded)
	
	c_ratio_tot_time_thousand = float(c_divmod_tot_time) / c_percent_slashes_tot_time
	c_ratio_tot_time_thousand = round(c_ratio_tot_time_thousand,3)
	print("c_ratio_tot_time_thousand:",c_ratio_tot_time_thousand)

	print("----------------------------------")	

	s_divmod_before = time.clock()
	for num in test_range_tenthousand:
		for p in p_values_tenthousand:		
			result = divmod(num, p)
			a_dblslash_p = result[0]
			a_mod_p = result[1]

	c_divmod_tot_time = time.clock() - s_divmod_before 
	c_divmod_tot_time_rounded = round(c_divmod_tot_time,4)
	print("c_divmod_tot_time_tenthousand_rounded:",c_divmod_tot_time_rounded)

	s_percent_slashes_before = time.clock()
	for num in test_range_tenthousand:
		for p in p_values_tenthousand:		
			a_dblslash_p = num // p
			a_mod_p = num % p

	c_percent_slashes_tot_time = time.clock() - s_percent_slashes_before 
	c_percent_slashes_tot_time_rounded = round(c_percent_slashes_tot_time,4)
	print("c_percent_slashes_tot_time_tenthousand_rounded:",c_percent_slashes_tot_time_rounded)
	
	c_ratio_tot_time_tenthousand = float(c_divmod_tot_time) / c_percent_slashes_tot_time
	c_ratio_tot_time_tenthousand = round(c_ratio_tot_time_tenthousand,3)
	print("c_ratio_tot_time_tenthousand:",c_ratio_tot_time_tenthousand)

	#print "What is a?"
	#a_initial=input("What is a?\n")
	#m_initial=input("What is m?\n")

	#Check if a is a digit
	#if a_initial.isdigit() == False:
	#	print(a," is not a number! Exiting..")

	#Check if a is a digit
	#if m_initial.isdigit() == False:
	#	print(m," is not a number! Exiting..")

def csvfile_store_primes(csv_filename_var):		### O(max{n,len(z1),1?}) ### 
		
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)			#O(n) - Potentially y rows and x items in each row, 
											# however only 1 row in csvfile being used. Hence x*y=x items to store
		primes=list(z1)								#O(len(z1))
		csvfile.close()								#O(1 ???)
	return primes

if __name__=='__main__':
	main()



