#Copyright Nick Prowse 2026. Code Licenced under GNU GPL v3.
#Version 2. 11/10/2026.
#Programmed & tested in Python 3.4.3 only
#This program prints the G_list for values of g and p chosen by user, where p is a prime number. 
#It requires pathlib to be installed.
#It has been tested on Windows 11 Home x64.

import sys
import math
from pathlib import Path

#import gmpy2
#import os
#import itertools
#import csv
#import time

print("Copyright Nick Prowse 2026. Code Licenced under GNU GPL v3.")
print("Version 2. 11/10/2026.")
print("Programmed & tested in python 3.4.3 only.")
print("This program prints the G_list for values of g and p chosen by user")
print("where p is a prime number.")
print("It has been tested on Windows 11 Home x64")
print("---------------------------------------------------------------------")

version = "v2"

python_version = sys.version
print("python_version is:",python_version)

home_dir = Path.home()
desktop_dir = Path.home() / "Desktop"
#repo_dir = "\Git_Repos\PythonMathsAlgorithms_GNUv3\"

# 1. Get the absolute path of the executing script
SCRIPT_PATH = Path(__file__).resolve()

# 2. Navigate up to the repository root directory
# (If script is in repo/src/script.py, .parent is 'src', .parent.parent is 'repo')
REPO_ROOT = SCRIPT_PATH.parent.parent.parent
print(f"Repository Root: {REPO_ROOT}")

output_filename = "output_Glist_v"+str(version)+".txt"
output_path = desktop_dir / output_filename
#print("output_path is:",output_path)

def main():
	
	print('What is g?')
	g_initial = input()
	if not (g_initial.isdigit() and int(g_initial) > 0):
		print('You have not entered a positive integer for g. g is:',str(g_initial),'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = int(g_initial)

	print('What is p?')
	p_initial = input()
	if not (p_initial.isdigit() and int(p_initial) > 0):
		print('You have not entered a positive integer for p. p is:',str(p_initial),'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = int(p_initial)

	print("---------------------")
	print("g:",g,",p:",p)

	data="Output\n------------\n"

	#print("data:",data)
	txtfile_create_new(data,output_path)

	data_for_append = []
 
	if is_primitive_root(g, p):
		print("g is a primitive root mod p! Hence G_list is all numbers from 1 to p-1")
		sys.exit()

	if g < p:
		if isprime(p) == True:
			#if g != p:				
			#Want to calculate and store group G				
			print("Calculating G_list..")
			
			G_list = []	
			# 1. Initialize with the first element (g^1 mod p)
			current_power = g % p	
			
			for number in range(1, p):
				G_list.append(current_power)

				# 2. Optional status check
				if number % 100000000 == 0:
        				print(f"exponent is now: {number}")   
	
				# 3. Compute the next power efficiently in O(1) time
				current_power = (current_power * g) % p

				# 4. Fast termination: Cyclic groups always loop back to g^1 (or 1 if started at g^0)
				if current_power == g % p:
       					break

				#a = pow(g,number,p)
				#if a not in G_list:					
				#G_list.append(a)
				#else:
				#	break

			G_list.sort()
			print("G_list:",G_list)
			for element in G_list:			
				if not data_for_append:
					data_for_append = str(element)				
				else:
					data_for_append = data_for_append + ", " +str(element)					
				txtfile_append(data_for_append,output_path)
		else:
			print("p is not prime! Exiting..")
	else:	
		print("g is greater than or equal to p ! Exiting..")
	
def isprime(p):		
	#Checks for divisibility of factors upto sqrt(p)
	#this likely to be O(sqrt(n))

	#print("Running isprime(",str(p),").."
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2

	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	print("p",p,"is prime!")
	return True

def get_unique_prime_factors(n):
    """Finds all unique prime factors of a number n."""
    factors = set()
    # Check factor 2
    if n % 2 == 0:
        factors.add(2)
        while n % 2 == 0:
            n //= 2
            
    # Check odd factors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 2
        
    # If n is still greater than 1, then n itself is prime
    if n > 1:
        factors.add(n)
    return factors

def is_primitive_root(g, p):
	#Efficiently checks if g is a primitive root modulo p.
	#Time Complexity: O(sqrt(p) + log(p)) due to factorization.
	if g <= 1 or g >= p:
    		return False

	#Step 1: Get the unique prime factors of phi(p) which is p-1
	totient = p - 1
	prime_factors = get_unique_prime_factors(totient)
	print("prime factors of p-1:",prime_factors)

	# Step 2: Test powers
	for q in prime_factors:
		test_exponent = totient // q
		if pow(g, test_exponent, p) == 1:
			return False  # Failed the test; g loops too early
            
	return True  # Passed all tests; g is a primitive root

def csvfile_store_primes(csv_filename_var):

	#print 'Running generator..'
	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..		
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		primes=list(z1)
		csvfile.close()	
	return primes

def txtfile_create_new(data,filepath):
	#create text file using data
	with open(filepath,'wb') as txtfile:
		txtfile.write(bytes(data,'UTF'))
		txtfile.close()	

def txtfile_append(data,filepath):
	#create text file using data
	with open(filepath,'ab') as txtfile:
		txtfile.write(bytes(data,'UTF'))
		txtfile.close()	

def size_input_check(input_number):
	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number > 2 * pow(10,8):
		print("Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..")
		sys.exit()

if __name__=='__main__':
	main()

