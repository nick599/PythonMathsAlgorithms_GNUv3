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

	test_range_thousand = range(1,1001)
	test_range_tenthousand = range(1,1001)
	p_values_hundred = primes[0:101]
	p_values_thousand = primes[0:1001]

	s_divmod_before = time.clock()
	for num in test_range_thousand:
		for p in p_values_hundred:		
			modinv_with_divmod(num, p)

	c_divmod_tot_time = time.clock() - s_divmod_before 
	print("c_divmod_tot_time_thousand:",c_divmod_tot_time)

	s_percent_slashes_before = time.clock()
	for num in test_range_thousand:
		for p in p_values_hundred:		
			modinv_with_percent_slashes(num, p)

	c_percent_slashes_tot_time = time.clock() - s_percent_slashes_before 
	print("c_percent_slashes_tot_time_thousand:",c_percent_slashes_tot_time)

	s_divmod_before = time.clock()
	for num in test_range_tenthousand:
		for p in p_values_thousand:		
			modinv_with_divmod(num, p)

	c_divmod_tot_time = time.clock() - s_divmod_before 
	print("c_divmod_tot_time_tenthousand:",c_divmod_tot_time)

	s_percent_slashes_before = time.clock()
	for num in test_range_tenthousand:
		for p in p_values_thousand:		
			modinv_with_percent_slashes(num, p)

	c_percent_slashes_tot_time = time.clock() - s_percent_slashes_before 
	print("c_percent_slashes_tot_time_tenthousand:",c_percent_slashes_tot_time)
	
	#print "What is a?"
	#a_initial=input("What is a?\n")
	#m_initial=input("What is m?\n")

	#Check if a is a digit
	#if a_initial.isdigit() == False:
	#	print(a," is not a number! Exiting..")

	#Check if a is a digit
	#if m_initial.isdigit() == False:
	#	print(m," is not a number! Exiting..")

	#convert a & m to integers
	#a = int(a_initial)
	#m = int(m_initial)

	
	#modinv(a_initial, m_initial)

def modinv_with_divmod(a, m):
	#print("Running modinv(",a,",",m,")")	
	#print("a is:",a)
	#print("m is:",m)	
	g, x, y = egcd_with_divmod(a, m)
	if g != 1:
		#raise Exception('No Modular Inverse')
		return 0 
	#print(a,"**(-1) mod ",m," is: ",x % m)	
	return x % m

def egcd_with_divmod(a, b):
	#print("Running egcd(",a,",",b,")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:
		#print("STOPPING since a is 0. Result: (",b,", 0, ",a,")")
		return (b, 0, 1)
	else:
		g, y, x = egcd_with_divmod(divmod(b,a)[1], a)
		#g, y, x = egcd_with_divmod(b % a, a)
		return (g, x - (divmod(b,a)[0]) * y, y)
		#return (g, x - (b//a) * y, y)

def modinv_with_percent_slashes(a, m):
	#print("Running modinv(",a,",",m,")")	
	#print("a is:",a)
	#print("m is:",m)	
	g, x, y = egcd_with_percent_slashes(a, m)
	if g != 1:
		#raise Exception('No Modular Inverse')
		return 0		 
	#print(a,"**(-1) mod ",m," is: ",x % m)	
	return x % m

def egcd_with_percent_slashes(a, b):
	#print("Running egcd(",a,",",b,")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:
		#print("STOPPING since a is 0. Result: (",b,", 0, ",a,")")
		return (b, 0, 1)
	else:
		g, y, x = egcd_with_percent_slashes(b % a, a)
		return (g, x - (b//a) * y, y)

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



