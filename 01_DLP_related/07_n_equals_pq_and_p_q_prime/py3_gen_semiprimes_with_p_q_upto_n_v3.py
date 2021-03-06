#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 3. 04/10/2018.
#Programmed & tested in Python 3.4.3 only
#This program loops through all numbers upto a upper bound U given by user, and creates a list of all numbers n <= U, where n=pq and p,q are both prime.
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997.

import sys
import math
import os
#import itertools
import csv
import time

#python_version = sys.version

#print(python_version)

version = 3

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version:",version,". 04/10/2018.")
print("Programmed & tested in python 3.4.3 only.")
#print("---------------------------------------------------------------------")
#print("This program loops through all numbers upto a upper bound U given by user, and creates a list of all numbers n <= U, where n=pq and p,q are both prime.")
#print("Prime list file should be a .CSV file with each prime separated by commas.")
#print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
#print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997")
print("---------------------------------------------------------------------")
	
folder = "/home/mint/Desktop/"
#prime_filename = "primes_upto_10000.csv"
#primefile_path = folder + prime_filename
#print("primefile_path is:",primefile_path)

output_filename = "output_semiprimes_v"+str(version)+".txt"
output_path = folder + output_filename
print("output_path is:",output_path)

def main():

	data="Output\n------------\n"

	sample_range=[10000]
	#sample_range=[100000]
	#sample_range=[1000000]
	#sample_range=[10000,100000,1000000]
	output_files=["output_v"+str(version)+"_"+str(sample_range[0])+".txt"]

	#print("data:",data)
	#Check if output file(s) already exist
	if os.path.isfile(output_path): 
		#file already exists - remove it			
		print(output_path,"already exists. Removing file..")		
		os.remove(output_path)
		txtfile_create_new(data,output_path)
	else:
		#file does not exist - create	
		txtfile_create_new(data,output_path)

	#Check if output file(s) already exist
	if os.path.isfile(output_files[0]): 
		#file already exists - remove it			
		print(output_files[0],"already exists. Removing file..")		
		os.remove(output_files[0])
		print("Creating file..")
		txtfile_create_new(data,output_files[0])
	else:
		#file does not exist - create	
		print("Creating file..")
		txtfile_create_new(data,output_files[0])

	#primes = csvfile_store_primes(primefile_path)
	
	#print("What is the upper bound U?")
	#U_initial = input()
	#if U_initial.isdigit() is False:
	#	print("Upper bound is not a number. Exiting..")
	#	sys.exit()

	#U = int(U_initial)
	

	for number in sample_range:
		s_before_loop = time.time()
		n_semiprime_list=[]
		n_non_semiprime_list=[]
		n_p_q_list=[]
		n_non_semiprime_list_for_append=[]
		n_semiprime_list_for_append = []
		n_p_q_list_for_append = []
		for num in range(1, number + 1):
			if num % 200000 == 0:		
				print("num processing:",num)
			factors = factorise(num)
			if len(factors)==2:
				#print("factors[1]:",factors[1])
				#input("Waiting for user..") 
				concat_n_p_q = []
				if isprime(factors[0]) == True and isprime(factors[1]) == True:
					#print("num:",num)
					n_semiprime_list.append(num)
					concat_n_p_q.append(num)
					#print("n_list is now:",n_list)
					concat_n_p_q.append(factors[0])
					#print("factors[1]:",factors[1])
					#input("Waiting for user..")
					concat_n_p_q.append(factors[1]) 				
					#print("concat_p_q:",concat_p_q)
					n_p_q_list.append(concat_n_p_q)
					if not n_p_q_list_for_append:					
						n_p_q_list_for_append = str(concat_n_p_q)
					else:
						n_p_q_list_for_append = n_p_q_list_for_append + "," + str(concat_n_p_q)

					if not n_list_for_append:					
						n_semiprime_list_for_append = str(num)
					else:
						n_semiprime_list_for_append = n_semiprime_list_for_append + "," + str(num)

					#print("p_q_list is now:",p_q_list)
					#input("Waiting for user..")
			elif len(factors)==1 or len(factors)>=3:
				#number is not a semiprime
				n_non_semiprime_list.append(num)
			else:
				print(number," is not a semiprime nor a non-semiprime!!!")
				print("factors: ",factors)				
				input("Waiting for user..")
		
		c_after_loop = time.time() - s_before_loop
		
		#txtfile_append(p_q_list_for_append,output_files[sample_range.index(number)])
		print("n_p_q_list_for_append output_path:",output_files[0])
		txtfile_append(n_p_q_list_for_append,output_files[0])
		print("number:",number,", len p_q_list:",len(n_p_q_list),", c_after_loop:",c_after_loop)
		
		print("output_path for list of semiprimes:",output_path)
		print("len n_list:",len(n_list))
		data="number:"+str(number)+", len n_p_q_list:"+str(len(n_p_q_list))+", c_after_loop:"+str(c_after_loop)+"\n"
		txtfile_append(n_list_for_append,output_path)
		#txtfile_append(data,output_path)
		
		#output_files[]
		
		
		#print("p_q_list:",n_list)
		#print("len p_q_list:",len(p_q_list))

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

def txtfile_append(data,filepath):
	#print("data:",data)

	#create text file using data
	with open(filepath,'a') as txtfile:
		txtfile.write(data)
		#txtfile.write(bytes(data,'UTF'))
		txtfile.close()	

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print("Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	factors = []					#O(1)		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]			#O(1)
	length, cycle = 11,3				#O(1)
	f, factors, next = 2, [], 0			#O(1)
	while f*f <= N:					#O(n)
		while N % f == 0:				#O(n)
			#f is a factor. Add factor f to fs
			factors.append(f)				#O(1)
			N /= f						#O(1)
		f += gaps[next]				#O(1)
		next += 1				#O(1)
		if next == length:			#O(1)
			next = cycle				#O(1)
	if N > 1: 
		#print("N to be appended as factor:",int(N))
		#print("N to be appended as factor:",N)
		factors.append(int(N))
		#input("Waiting for user..")
 
	return factors		#O(1)
	
def calc_primefactors_nopowers(factors):
	#used in euler_phi()
	#Worst: O(n+13)	#Best: O(18)

	#print("Running calc_primefactors.."
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#O(1)
	fac_list = []						#O(1)
	for factor in factors:					#O(n)	#Worst: O(n**2 + 2n)	#Best: O(???)
		if factor not in fac_list:					#O(n)	#Worst: O(n+1)	#Best: O(6)
			prime_factors.append(factor)				#O(1)
			fac_list.append(factor)					#O(1)
		else:								#O(1)	#Subtotal: O(4)
			fac_list.append(factor)						#O(1)	
			
	return prime_factors
	
def calc_primefactors_powers(factors, N):
	#used in prim_root()	
	#print("Running calc_primefactors_powers("+str(factors)+", "+str(N)+").."
	
	#Now want to find max powers m for each factor in factors. can do this by counting unique factors			
	prime_factors=[]
	fac_list = []
	for factor in factors:		
		if factor not in fac_list:
			prime_factors.append(factor)
			fac_list.append(factor)					
		else:
			fac_list.append(factor)
			
	powers = []
	for prime_factor in prime_factors:
		count = 0
		while N % prime_factor == 0:
			count = count + 1
			N = N / prime_factor		
		else:
			powers.append(count)
				
	return prime_factors, powers
	
def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number > 2 * pow(10,8):
		print("Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..")
		sys.exit()

def txtfile_create_new(data,filepath):
	#create text file using data
	with open(filepath,'w') as txtfile:
		txtfile.write(data)
		#txtfile.write(bytes(data,'UTF'))
		txtfile.close()

if __name__=='__main__':
	main()

#def ghp_checks(g, p, h, floor_sqrt_p):

	#print("Running ghp_checks().."

#	status=1
	
	#Need to check if p is prime
#	a = isprime(p)	
	#return True for prime, False for not prime
#	if a == False:
#		print("The number entered for p: ",p," is not prime. Please choose a number that is prime for p.")
#		status=0
		#count_notprime = count_notprime + 1
#		sys.exit()

	#Simple Checks for g, h & p:
#	if (g==0 or h==0 or p==0):
#		print("One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.")
#		status=0
#		sys.exit()
#	elif g==1:
#		print("g = 1 has trivial solutions for the dlp. Please choose another number.")
#	elif g<0:
#		print("Number for g is negative. Please enter another number")
#		status=0
#		sys.exit()	
	
#	return status

#def egcd(a, b):
#	#print("Running egcd("+str(a)+","+str(b)+")")
#	if a == 0:
#		return (b, 0, 1)
#	g, y, x = egcd(b % a, a)
#	return (g, x - (b//a) * y, y)

#def modinv(a, m):
	#print("Running modinv("+str(a)+","+str(m)+")")	
#	g, x, y = egcd(a, m)
#	if g != 1:
#		raise Exception('No Modular Inverse') 
#	return x % m



#def prim_root(g,p,primes):

	#print("Running prim_root("+str(g)+", "+str(p)+", primes).."

#	status = True
#	check = 0	
#	ep = euler_phi_primesused(p)
	#return a	
	#ep=result[0]
	
#	factors = factorise(ep)	
#	result2 = calc_primefactors_powers(factors, ep)
	#return prime_factors, powers, c_calc_powers		
#	prime_factors = result2[0]
#	powers = result2[1]
#	power=1

	#Do we need to check prim roots now???
#	for prime in prime_factors:		
#		if status==True:
#			power=1
#			power_index = 0
#			while power < powers[power_index]:
#				if pow(g,int(ep / pow(powers[power_index],power)),p) == 1:
#					status=False	
#					break
#				power = power + 1
#			power_index = power_index + 1

#	return status, prime_factors, powers

#def euler_phi_primesused(n):				
	
	#when n is not prime
	# Worst: O(sqrt(n)+8)  
	# Best:	O(4) when n=1

	#when n is prime
	#O(sqrt(n)+5) 
	
	#print("Running euler_phi_primesused("+str(n)+", primes).."

#	if n==1:					#O(1)	#subtotal O(3)
#		a = 1					#O(1)				
#		return a				#O(1)		
			
#	elif isprime(n)==True:
#		return n-1
#	else:							#subtotal O(???)
		#euler_phi(p**k) = (p-1)*p**(k-1) for prime p 
		#euler_phi(m*n) = euler_phi(m)*euler_phi(n) for coprime m & n
		#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.
		
		#n = p_1**(k_1)*p_2**(k_2)*p_3**(k_3)... , where p_i are prime factors of n, and k_i are corresponding powers.
		#n, and P_i are known 
		#need primes from factorise()!
				
#		factors = factorise(n)					#O(sqrt(size(n)))
#		prime_factors = calc_primefactors_nopowers(factors) 	#O(???)		#Best operations: ??? 
									#**CHECK** This should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		
		#len_prime_factors = len(prime_factors)

		#initialise ep
#		ep=n
		
#		for prime in prime_factors:			#O(prime_factors)
			#now calculate first (1-1/p) for p|n
#			term = 1 - 1 / float(prime)
			#recalculate ep
#			ep = ep * term
			
#		ep = int(ep)
#		return ep				#O(1)
		
#def check_answer(g, p, h, x):
#	status=True	
#	if pow(g,x,p) != h:
#		status=False
		
#	return status	

#def chinese_remainder(x, x_moduli):
	#print("Running chinese remainder("+str(x)+","+str(x_moduli)+").."	
#	cong_x=[]
#	cong_moduli=[]
#	x_new = 0
#	M = 0
#	a = 0
#	b = 0
#	for number in range(0,len(x)):		
		#store values in 1st congruence	
#		a= x[number]
#		b= x_moduli[number]
#		if b!=1:		
#			if not cong_x:
				#cong has no elements. Add values in first congruence			
#				cong_x.append(a)
#				x_new = a		
#				cong_moduli.append(b)
#				M = b			
#			else:
				#cong_x has elements. Subtract current cong_x[number-1] from current x[number]
#				c = x[number] - cong_x[-1]
				#now want to find (cong_moduli[number-1]**-1) mod(b)		
#				f = calc_modinverse(cong_moduli[-1], 1, b)
				#now take c and times it by the inverse, f, and reduce mod b
#				k = (c*f) % b			
				#now take value of k and use it to work out new value of x
#				x_new = cong_x[number-1] + (cong_moduli[number-1] * k)
#				cong_x.append(x_new)
				#now work out value of M
#				M = cong_moduli[-1] * b
#				cong_moduli.append(M)
#	return x_new, M

#def polig_helman(primes_list, powers, g, p, h, p_minus_1, gi, h_power_values):

	#p_minus_1 = p-1

	#3: initialise lists and values
#	hi=[]
#	x=[] 
#	x_moduli=[]
#	x_status = True

	#4: loop through each C calculating values & storing them
	#print("looping through C_list")
#	for prime in primes_list:
#		i = primes_list.index(prime)		

#		hi.append(pow(h,h_power_values[i],p))
		
		#7: Now Bi[i]**x = zi[i] mod p for each i. Need to solve for x for each.
		#now x = a mod (qi**ei) is a solution where a is unknown

#		init_moduli = p			
		
#		if gi[i] == 1 and hi[i] == 1:
#			x_status = False
#			break
			
#		elif gi[i] == 1 and hi[i] != 1:
#			x_status = False
#			break
#		else:
			#need to check all x s.t 0 <= x < qi**ei 
			#start with init_moduli. If an exponent is not found then consider prime powers from qi**ei to qi**1 in turn
			
#			result = exponent_g_n(gi[i], hi[i], init_moduli)
			#return x, status, moduli		
#			status = result[1]			
			#status = False for no exponent found

#			if status == False:
				#Exponent is not found for init moduli. Hence consider prime powers from qi**ei to qi**1 in turn
			
				#ei_init = ei[i]
#				ei_init = powers[i]
#				while ei_init >= 1:
					#moduli = pow(qi[i],ei_init)
#					moduli = pow(primes_list[i],ei_init)
#					result = exponent_g_n(gi[i], hi[i], moduli)
#					status = result[1]			
					#status = False for no exponent found
#					if status == True:
#						x_moduli.append(moduli)
#						break
#					else:				
#						ei_init = ei_init - 1	
#			else:
				#Exponent & Moduli found
#				x.append(result[0])
#				x_moduli.append(result[2])
				
#			i = i + 1

	#unique_hi_values = []
	#for hi_value in hi:
	#	if hi_value not in unique_hi_values: 						
	#		unique_hi_values.append(hi_value)

	#for unique_hi_value in unique_hi_values:
	#	if unique_hi_value in hi:		

	#print("x:",x, "x_moduli:",x_moduli, "x_status:",x_status)
#	return x, x_moduli, x_status, hi

	#return x, x_moduli, x_status, unique_hi_values, hi

#def exponent_g_n(generator, h_value, p):

	#print("Running exponent_g_n("+str(generator)+", "+str(h_value)+", "+str(p)+")")	
#	n = 1
#	x = 0
#	moduli = 0
#	status = False
#	while n < p:
#		if pow(generator, n, p) == h_value:
#			x = n
#			status = True
#			for number in range(x + 1, 2*p):
#				if pow(generator, number, p)== h_value:
#					moduli = number - x
#					break
#			break
#		n = n + 1

#	if status == False:
#		x = "No exponent found"
#		moduli = 0

#	return x, status, moduli 

#def calc_modinverse(g, power, p):
	#print("Running calc_modinverse(",g,", ",power,", ",p,")..")	
	
	#this only works for p being prime!	
#	if isprime(p) == True:	
#		result=pow(g,p-2,p)
#		c = pow(result,power,p)
#	else:
		#p is not prime!
#		c = modinv(g, p)	
#	return c

#def csvfile_store_primes(csv_filename_var):

	#print 'Running generator..'
#	with open(csv_filename_var,'r') as csvfile:
#		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..		
#		z1=(int(x) for row in csv.reader(csvfile) for x in row)
#		primes=list(z1)
#		csvfile.close()	
#	return primes

#def csvfile_create_new(data,filepath):
	#create csv file using data
#	with open(filepath,'w') as csvfile:
#		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
#		wr.writerow(data)		
#		csvfile.close()	

#def csvfile_append(data,filepath):
#	#create csv file using data
#	with open(filepath,'a') as csvfile:
#		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
#		wr.writerow(data)		
#		csvfile.close()	

	

