# 26/04/2018
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
	test_range_fivethousand = range(1,5001)
	#test_range_tenthousand = range(1,10001)
	#test_range_fiftythousand = range(1,50001)
	#test_range_hundredthousand = range(1,100001)
	#test_range_million = range(1,1000001)
	p_values_hundred = primes[0:101]
	p_values_thousand = primes[0:1001]
	p_values_fivethousand = primes[0:5001]
	#p_values_tenthousand = primes[0:10001]
	#p_values_fiftythousand = primes[0:50001]
	#p_values_hundredthousand = primes[0:100001]

	sample_range = range(1,51)

	print("----------------------------------")	

	time_values = []
	tot_time = 0
	
	for x in sample_range:	
		result = quotient_testing(test_range_hundred,p_values_hundred)
		#return c_quotient_tot_time
		tot_time = tot_time + result
		time_values.append(result) 

	len_test_range = len(sample_range)
	min_tot_time = min(time_values)
	min_tot_time = round(min_tot_time,5)
	max_tot_time = max(time_values)
	max_tot_time = round(max_tot_time,5)
	mean_tot_time = tot_time / len_test_range 
	mean_tot_time = round(mean_tot_time,4)
	print("mean_tot_time_hundred_quotient:",mean_tot_time)
	print("max_tot_time_hundred_quotient:",max_tot_time)
	print("min_tot_time_hundred_quotient:",min_tot_time)

	print("----------------------------------")	

	time_values = []
	tot_time = 0
	
	for x in sample_range:	
		result = quotient_testing(test_range_thousand,p_values_thousand)
		#return c_modulo_tot_time
		tot_time = tot_time + result
		time_values.append(result) 

	len_test_range = len(sample_range)
	min_tot_time = min(time_values)
	min_tot_time = round(min_tot_time,5)
	max_tot_time = max(time_values)
	max_tot_time = round(max_tot_time,5)
	mean_tot_time = tot_time / len_test_range 
	mean_tot_time = round(mean_tot_time,4)
	print("mean_tot_time_thousand_quotient:",mean_tot_time)
	print("max_tot_time_thousand_quotient:",max_tot_time)
	print("min_tot_time_thousand_quotient:",min_tot_time)

	print("----------------------------------")	

	#sample_range=range(1,51)
	time_values = []
	tot_time = 0
	
	for x in sample_range:	
		if x % 5 == 0:
			print("Test:",x)
		result = quotient_testing(test_range_fivethousand,p_values_fivethousand)
		#return c_quotient_tot_time
		tot_time = tot_time + result
		time_values.append(result) 

	len_test_range = len(sample_range)
	min_tot_time = min(time_values)
	min_tot_time = round(min_tot_time,5)
	max_tot_time = max(time_values)
	max_tot_time = round(max_tot_time,5)
	mean_tot_time = tot_time / len_test_range 
	mean_tot_time = round(mean_tot_time,4)
	print("mean_tot_time_fivethousand_quotient:",mean_tot_time)
	print("max_tot_time_fivethousand_quotient:",max_tot_time)
	print("min_tot_time_fivethousand_quotient:",min_tot_time)

def quotient_testing(test_range,p_values):
	s_quotient_before = time.clock()
	for num in test_range:
		for p in p_values:		
			result = num // p

	c_quotient_tot_time = time.clock() - s_quotient_before 
	#c_quotient_tot_time_rounded = round(c_quotient_tot_time,4)
	#print("c_quotient_tot_time_hundred_rounded:",c_quotient_tot_time_rounded)
	return c_quotient_tot_time

def modulo_testing(test_range,p_values):
	s_modulo_before = time.clock()
	for num in test_range:
		for p in p_values:		
			result = num % p

	c_modulo_tot_time = time.clock() - s_modulo_before 
	#c_modulo_tot_time_rounded = round(c_modulo_tot_time,4)
	#print("c_modulo_tot_time_hundred_rounded:",c_modulo_tot_time_rounded)
	return c_modulo_tot_time

def divmod_testing(test_range,p_values):
	s_divmod_before = time.clock()
	for num in test_range:
		for p in p_values:		
			result = divmod(num, p)
			a_dblslash_p = result[0]
			a_mod_p = result[1]

	c_divmod_tot_time = time.clock() - s_divmod_before 
	#c_divmod_tot_time_rounded = round(c_divmod_tot_time,4)
	#print("c_divmod_tot_time_hundred_rounded:",c_divmod_tot_time_rounded)
	return c_divmod_tot_time
	
def percent_slashes_testing(test_range,p_values):
	s_percent_slashes_before = time.clock()
	for num in test_range:
		for p in p_values:		
			a_dblslash_p = num // p
			a_mod_p = num % p

	c_percent_slashes_tot_time = time.clock() - s_percent_slashes_before 
	#c_percent_slashes_tot_time_rounded = round(c_percent_slashes_tot_time,4)
	#print("c_percent_slashes_tot_time_hundred:",c_percent_slashes_tot_time_rounded)
	return c_percent_slashes_tot_time

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



