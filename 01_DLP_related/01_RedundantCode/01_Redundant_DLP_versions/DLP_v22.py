#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 22. 16/11/2017.
#Programmed & tested in Python 2.76 only
#This program attemps to solve a Discrete Log Problem (DLP) specified by user, via factorisation of (p-1) where p is a prime number. 
#Results printed are three arrays ...
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.
#The larger the prime file is that is used, the longer the factorisations will take!
#It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 9,999,997 and was able to solve a DLP with a prime of xxx in xxx seconds.

import sys
import math
import os
import itertools
import csv
import time

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 22. 16/11/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via factorisation of (p-1) where p is a prime number.")
print("Results printed are three arrays ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
print("The larger the prime file is that is used, the longer the factorisation will take!")
print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997 and was able to solve a DLP with a prime of xxx in xxx seconds")
print("---------------------------------------------------------------------")
	
def main():
	prime_list_path="/home/mint/Desktop/"
	prime_list_filename="primes_upto_100000.csv"
	primefile=prime_list_path + prime_list_filename
	print('primefile currently is: '+str(primefile))

	#print(sys.version_info)

	print('What is g?')
	g_initial = raw_input()
	if g_initial.isdigit() is False:
		print('You have not entered a positive integer for g. g is: '+str(g_initial)+'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = long(g_initial)

	print('What is h?')
	h_initial = raw_input()
	if h_initial.isdigit() is False:
		print('You have not entered a positive integer for h. h is: '+str(h_initial)+'. Please reenter.')
		sys.exit()

	#now convert h into a long:
	h = long(h_initial)

	print('What is p?')
	p_initial = raw_input()
	if p_initial.isdigit() is False:
		print('You have not entered a positive integer for p. p is: '+str(p_initial)+'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = long(p_initial)

	print("---------------------")
	print("g: "+str(g)+", h: "+str(h)+", p: "+str(p))

	floor_sqrt_p = int(math.floor(math.sqrt(p)))
	print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	#result=ghp_checks(g,h,p,floor_sqrt_p)
	count_notprime = 0
	result=ghp_checks(g, h, p, floor_sqrt_p, count_notprime) 

	if result == 0:
		sys.exit()

	#Check if g is a primitive root mod p
	count_primroot=0
	result=prim_root(g,p,count_primroot)
	if result[0] is False:
		print(str(g)+' is not a primitive root mod '+str(p)+'! Exiting ...')		
		#count_primroot
		sys.exit()
	else:
		print(str(g)+' is a primitive root mod '+str(p))	

	#define prime list
	print('Importing primes from csv file')
	primes=csvfile_store_primes(primefile)
	print('First ten primes are: '+str(primes[0:10]))

	#check if sqrt_p > largest element in primes
	print('checking if square root of p > largest element in primes...')
	sqrt_p = math.sqrt(p)
	largest_prime = primes[-1]
	if sqrt_p > largest_prime:
		print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
		sys.exit()

	#define counts for different types of results
	count_nosolns=0
	count_zi_bi_equal_1=0
	count_bi_equal_1_zi_ntequal_0_1=0
	count_x_equals_0=0
	count_Bi_equals_zi=0
	count_normal_soln=0

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print('Running dlp()..')
	result = dlp(g,h,p, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln)
	
	#result = dlp(g,h,p, primes)
	#count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln

	x=result[0]
	#y=result[1]
	print x, y

def ghp_checks(g,h,p,floor_sqrt_p, count_notprime):

	status=1
	
	#Need to check if p is prime
	print('Checking if p is prime ..')
	#print "Testing if "+str(p)+" is prime: "+str(isprime(p,floor_sqrt_p))
	a = isprime(p,floor_sqrt_p)
	#print("isprime(p) is: "+str(a))	
	if a<>0:
		print('The number entered for p: '+str(p)+' is not prime. Please choose a number that is prime for p.')
		status=0
		count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	print('Running simple checks on g..')
	if (g==0 or h==0 or p==0):
		print('One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.')
		status=0
		sys.exit()
	elif g==1:
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
	#elif h==1:
	#	print('h = 1 has trivial solutions for the dlp. Please choose another number.')
	#	status=0
	#	sys.exit()
	elif g<0:
		print('Number for g is negative. Please enter another number')
		status=0
		sys.exit()	
	
	return status

def isprime(p,floor_sqrt_p):
	#print('p is: '+str(p))	
	status=0
	if p % 2 == 0:
		status=1
	
	#floor_sqrt_p = int(math.floor(math.sqrt(p)))	
	
	n=3
	while n <= floor_sqrt_p:
		if p % n == 0:
			status=1
			break 
		else:
			status=0
		n = n + 2
	#print('status is: '+str(status))	
	#status=0 for prime
	#status=1 for not prime
	return status		

#def modulo(x,p):
#	r = x % p
#	return r

def prim_root(g,p, count_primroot):

	print('Checking if '+str(g)+' is a primitive root mod '+str(p)+' ..')
	status=True
	F_p_star=[]	
	for j in xrange(0,p-1): #eg for p=9: 0,1,2,3, .. ,7  
		#F_p_star[j]=(g**j)%p	
		if ((g**j)%p in F_p_star) and j<>0:
			status=False
			#print('Fail on 1st check')
			break
		else:
			F_p_star.append((g**j)%p)
	if status==False:
		count_primroot = count_primroot + 1
	return status, count_primroot

def euler_phi(n):
	#euler_phi(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.	
	#euler_phi(n) = sigma_{for d|n} (mu(d)/d), where mu is the mobius function.

	#euler_phi(9) = 6, since gcd of 9 with 1,2,4,5,7 and 8 is 1. 
	#euler_phi(9) = 9 * Pi_{for p|9} (1-1/p) = 9*(1-1/3) = 9-3 = 6

	status = True 
	floor_sqrt_n = math.floor(n)

	if isprime(n,floor_sqrt_n) is True:
		a = n - 1		
	elif n==1:	
		a = 1
	else:
		#eg n=4		
		result=factorise(n, primes)
		primes=result[0]
		powers=result[1]
		remainder=result[2]
		if remainder:
			print('Factorisation of '+str(n)+' gives a remainder of '+str(remainder)+' using specified prime list!')			
			a = 0			
			status = False 
			sys.exit()
		c = 1
		for i in xrange(0, len(primes) + 1):			
			b = primes[i] ** powers[i] 
			c = c * b
		a = c 
	return a, status

def dlp(g, h, p, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln):
	
	print('--------------------')

	#1st step: calculate p-1 from p
	p_minus_1 = p-1
	print('p-1 is: '+str(p-1))	

	#2nd step: factorise p_minus_1 into product of prime powers
	result=factorise(p_minus_1, primes)
	primes_list=list(result[0])
	powers=list(result[1])
	moduli=list(result[7])
	print('primes for factorisation of p-1 are:'+str(primes_list))
	print('powers for factorisation of p-1 are:'+str(powers))
	#print('values of each prime * respective power for factorisation of p-1 are:'+str(mult_primes_powers))

	#3: Calculate C - number of unique primes in factorisation (also is number of congruences to solve)
	C=0
	for prime in primes_list:
		C = C + 1		
	print('Number of primes in primes_list = C = '+str(C))

	#4: Need to create a list (with C elements) for each of: q_i, e_i, W, g_i, h_i, z_i, & V_i 
	C_list=list(xrange(1,C+1))
	print('C_list is: '+str(C_list))
	print('--------------------')

	#5: initialise lists
	qi=[]
	ei=[]
	Wi=[]
	gi=[]
	hi=[]
	zi=[]
	Bi=[]
	Vi=[]
	#Ui=[]

	#6: loop through each C calculating values & storing them
	i = 0
	for C in C_list:
		print('current C is:'+str(C))
		#modulo(x,p)
		print('i is: '+str(i))
		qi.append(primes_list[i])
		print('qi['+str(i)+'] is: '+str(qi[i]))
		ei.append(powers[i])
		print('ei['+str(i)+'] is: '+str(ei[i]))
		Wi.append(p_minus_1 / (qi[i]**ei[i]))
		#print('Wi['+str(i)+'] = p_minus_1 / (qi['+str(i)+']**ei['+str(i)+'])  is: '+str(Wi[i]))
		
		gi.append(g**Wi[i])
		#print('gi['+str(i)+'] = g**Wi['+str(i)+'] is: '+str(gi[i]))
		Bi.append(gi[i] % p)
		print('Bi['+str(i)+'] = gi['+str(i)+'] % p is: '+str(Bi[i]))
		
		hi.append(h**Wi[i])
		#print('hi['+str(i)+'] = h**Wi['+str(i)+'] is: '+str(hi[i]))
		zi.append(hi[i] % p)
		print('zi['+str(i)+'] = hi['+str(i)+'] % p is: '+str(zi[i]))
		
		#raw_input('Waiting for user..')

		#print('length(Bi) is: '+str(len(Bi)))
		#for var in xrange(0,len(Bi)+1):
			#print('var is: '+str(var))
	
		#7: Now Bi[i]**x = zi[i] mod p for each i
		# Need to solve for x for each.
		x=[] 
		
		print('Solving for x...')
		#print('Bi['+str(i)+'] is: '+str(Bi[i]))
		#print('zi['+str(i)+'] is: '+str(zi[i]))
		if Bi[i]==0 and zi[i]==1:
			print('i is: '+str(i))
			print('qi['+str(i)+'] is: '+str(qi[i]))
			print('ei['+str(i)+'] is: '+str(ei[i]))
			print 'No Solutions!!!'
			count_nosolns=count_nosolns + 1
			sys.exit()
		elif Bi[i]==0 and zi[i]==0:
			print('i is: '+str(i))
			print('qi['+str(i)+'] is: '+str(qi[i]))
			print('ei['+str(i)+'] is: '+str(ei[i]))
			print 'No Solutions!!!'
			count_nosolns=count_nosolns + 1
			sys.exit()
		elif Bi[i]==1 and zi[i]==0:
			print('i is: '+str(i))
			print('qi['+str(i)+'] is: '+str(qi[i]))
			print('ei['+str(i)+'] is: '+str(ei[i]))
			print 'No Solutions!!!'
			count_nosolns=count_nosolns + 1
			sys.exit()
		elif Bi[i]==1 and zi[i]==1:
			print('i is: '+str(i))
			print('qi['+str(i)+'] is: '+str(qi[i]))
			print('ei['+str(i)+'] is: '+str(ei[i]))
			print 'CHECK - Bi[i] and zi[i] both equal 1?!'
			count_zi_bi_equal_1=count_zi_bi_equal_1 + 1
			sys.exit()
		elif Bi[i]==1:
			print('i is: '+str(i))
			print('qi['+str(i)+'] is: '+str(qi[i]))
			print('ei['+str(i)+'] is: '+str(ei[i]))
			print 'CHECK - Bi[i]=1 and zi[i]!=0 and zi[i]!=1 ?!'
			count_bi_equal_1_zi_ntequal_0_1=count_bi_equal_1_zi_ntequal_0_1 + 1
			sys.exit()
		elif Bi[i]<>0 and zi[i]==1:
			x.append(0)
			print'added 0 to x[]'
			count_x_equals_0=count_x_equals_0 + 1
		elif Bi[i] == zi[i]:
			x.append(1)
			#moduli.append(qi[var]**ei[var])
			count_Bi_equals_zi=count_Bi_equals_zi + 1
		else:
			print('Running prop_234 to solve for x...')
			result = prop_234(Bi[i], zi[i], qi[i], ei[i], p)
			x.append(result)
			count_normal_soln=count_normal_soln + 1
		#moduli.append(qi[i]**ei[i])

		print('----------------------')
		i = i + 1


	print('x\'s are: '+str(x))

	#raw_input('Waiting for user..')

	return x, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln

def prop_234(Bi, zi, qi, ei, p):

	#Bi[var], zi[var], qi[var], ei[var], p

	#let x = x_0 +x_1*(q)+x_2*(q**2)+...+x_{e-1}q^(e-1), with 0 <= x_i < q, and determine successively x_1, x_2, ...
	
	#eg p=11251 has the property that 5**4 | p-1 = 11250, and g = 5448 has order 5**4 in F_11251
	#Hence q = 5, e = 4 
	# ==> x = x_0 + 5x_1 + 25x_2 + 125x_3, with 0 <= x_i < 5
	# ==> possible values for x_i: {0,1,2,3,4}

	#eg p=7 has the property that 3**1 | p-1 = 6, and g = 3 has order 1 in F_7
	#Hence q = 3, e = 1 
	# ==> x = x_0, with 0 <= x_i < 3
	# ==> possible values for x_i: ={0,1,2}
	
	#eg p=9 has the property that 2**3 | p-1 = 8, and g = 2 has order 3 in F_9
	#Hence q = 2, e = 3 
	# ==> x = x_0 + 5x_1 + 25x_2, with 0 <= x_i < 2
	# ==> possible values for x_i: ={0,1}

	#Need to determine largest divisor of p-1 from primes and powers, and return the prime and its power.
	#result=largest_divisor(p-1, primes_list, powers, mult_primes_powers)	
	#q=result[0]
	#print "q is: "+str(qi)
	#e=result[1]
	#print "e is: "+str(ei)

	print "-----------------------------------"

	# constuct list of q_powers from 0 to e-1
	q_powers=[]
	if ei>1:
		for k in xrange(0,ei):
			q_powers.append(qi**k)

	print "q_powers are: "+str(q_powers)
	print "length of q_powers is: "+str(len(q_powers))
	print "max q_power is: "+str(max(q_powers))

	#raw_input('Waiting for user..')

	#initialise xi
	xi=len(q_powers) * [0]

	#initialise g=Bi
	g=Bi	
	#print "g is: "+str(g)
	
	#initialise h=zi
	h=zi
	#print "h is: "+str(h)

	#evaluate x_i for qi and ei:
	for q_power in q_powers:
		print("q_power is: "+str(q_power))
		if q_power==1:
			#solving for x_0
			print("Solving for x_0 ..")
			#need to solve (g**q**(e-1))*x_0 = h**q**(e-1), mod q**(e-1)
			#eg g=3, h=5, p=101. Hence (3**5**1)*x_0 = 101**5**1, mod 5**1 
			print("qi is: "+str(qi))
			print("ei is: "+str(ei))
			moduli = p
			#moduli = qi**(ei - 1)			
			print("moduli is: "+str(moduli))
			#lhs= (g**moduli) % moduli
			lhs= (g**qi**(ei-1)) % p
			print "g is: "+str(g) 			# g=81
			print "h is: "+str(h) 			# h=9
			print("lhs is: "+str(lhs)) 		# lhs=1
			rhs= (h**qi**(ei-1)) % p
			print("rhs is: "+str(rhs)) 		# rhs=4
			for t in xrange(0, qi):
				if lhs**t==rhs:
					xi[0]=t  # xi[0]=0
					break
			print("xi[0] is: "+str(xi[0]))
			print("---------------------------")
		elif q_power==5:
			#solving for x_1
			print("Solving for xi[1] ..")
			#need to solve (g**q**(e-1))*x_1 = (h*(g**[-x_0]))**q**(e-2), mod q**(e-1)
			#eg g=3, h=5, p=101. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
			print "g is: "+str(g) # g=81
			print "h is: "+str(h) # h=9
			print("xi[0] is: "+str(xi[0])) # xi[0]=0
			#lhs= g**q**(e-1)%(q**(e-1))
			#print("lhs is: "+str(lhs))
			
			print("qi is: "+str(qi))
			print("ei is: "+str(ei))
			moduli = p
			#moduli = qi**(ei - 1)			
			print("moduli is: "+str(moduli))
			
			#b=-x_0
			if xi[0] > 0:
				#need to work out what g**[-x_0], mod q**(e-1) is!!!
				result = calc_modinverse(g, xi[0], p)
				rhs = result[0]
			elif xi[0]==0:
				#g**[x_0]=g**0=1, mod q**(e-1)
				#Hence h*(g**[-x_0]) = h, mod q**(e-1)
				#rhs= (h*g**(-x_0))**qi**(e-2)%(qi**(ei-1))
				#Thus rhs = (h)**qi**(e-2) % (q**(e-1))
				rhs = (h**qi**(ei-2)) % p
			else:
				print("xi[0] is negative !!! CHECK")				
				sys.exit()			
			print "lhs is: "+str(lhs)
			print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
			for t in xrange(0, qi):
				if lhs**t==rhs:
					xi[1]=t
		elif q_power==25:
			#solving for x_2 
			print("Solving for x_2 ..")
			#need to solve (g**q**(e-1))*x_2 = (h*(g**[-x_0-x_1*q]))**q**(e-3), mod q**(e-1)
		elif q_power==125:
			#solving for x_3
			print("Solving for x_3 ..")
		elif q_power==625:
			#solving for x_4
			print("Solving for x_4 ..")
		else:
			#solving for x_n .. ??
			print("q_power is: "+str(q_power))
			print("Solving for x_n ??..")
	raw_input('Waiting for user..')


	# Now need to contruct formulae for x = x_{0} +x_{1}*(q)+x_{2}*(q**2)+...+x_{e-1}q^(e-1)
	#print "e - 1 is: "+str(e-1)
	#for  in xrange(0, e+1): 
		#1st loop: x= x_0
		#2nd loop: x= x_0 + x_1(q)

	#	x = j

	#raw_input('Waiting for user..')

	#Use Euclids algorithm forward & reverse to find inverses where required
	
	euclid_f=[]
	euclid_r=[]
	#yi=[]
	#j = 0
	#for C in C_tuples:	
	#	euclid_f=euclid_forward(zi_list[j],Vi_list[j],p)
	#	euclid_r=euclid_reverse(euclid_f[0],euclid_f[1],p)
	#	yi[j]=euclid_r[0]	
	#	j = j + 1

	#Now x = yi mod qi for each record

	return x

def calc_modinverse(g, xi, p):

	return z

def egcd(a, b):
	if a == 0:
		return (b, 0, a)
	g, y, x = egcd(b % a, a)
	return (g, x - (b//a) * y, y)

def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('No Modular Inverse') 
	return x % m

#def largest_divisor(n, primes_new, powers_new, mult_primes_powers):

	#div_values=[]
	#print('i is:'+str(i))
	#for i in xrange(0,len(primes)+1):	
		#print('i is:'+str(i))		
		#div_values.append(mult_primes_powers[i])
		#div_values.append(primes[i],powers[i], primes[i]**powers[i])
	
#	print "mult_primes_powers are: "/+str(mult_primes_powers)
#	l_div=max(mult_primes_powers)
#	print "Largest divisor (q**e) is: "+str(l_div)	
#	l_div_index=mult_primes_powers.index(l_div)
#	prime=primes_new[l_div_index]
	#print "Prime of largest divisor is: "+str(prime)
#	power=powers_new[l_div_index]
	#print "Power of largest divisor is: "+str(power)

	#max_div_value = max(div_values[2])
	#min_div_value = min(div_values[2])

	#if max_div_value==min_div_value:
	#	l_div=max_div_value
	#else:
				
		#continue

	#a="" #value to check
	#b=""
	#for j in xrange(0, len(div_values)+1):
	#	a = div_value[0]
	#	

#	return prime, power, l_div

#def order_element_modulo(a, p):
#	#m=0
#	#while N_remainder > 1 and not N_remainder % i:	
#	#	m += 1		
#	#	N_remainder //= i
#	
#	n=0
#	while (a**n) % p <> 1: 
#		n = n + 1
#	return n

def MaxPower(i,N_remainder):
	m=0
	while N_remainder > 1 and not N_remainder % i:	
		m += 1		
		N_remainder //= i
	return m


def max_element_below_or_equal_target(List,target):
	#bool1=False
	if target in List:
		return List.index(target)#, bool1
	elif target > List[-1]:
		#Target value is not in list. Return index of last number in list.
		#bool1=True
		return List.index(List[-1])#, bool1
	elif target < List[-1]:
		#Target value is less than largest prime in list
		# start from 2 and increase until last number is found that is less than target.
		i=0
		while List[i] < target:
			i = i + 1 
		return i#, bool1
	else:
		print 'List[-1] is: '+str(List[-1])
		print 'target is: '+str(target)	
		print "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))
		return "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))


def csvfile_store_primes(csv_filename_var):

	with open(csv_filename_var,'r') as csvfile:
		# Want to limit highest prime imported from csv to be <= math.sqrt(N)
		# Need to get index of the highest prime <= math.sqrt(N)
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
		print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		primes=list(z1)
		csvfile.close()	
	return primes

def factorise(N,list):		
	#Create lists to hold prime factors of N, corresponding powers and any remainder
	s_before_lists = time.clock()	
	prime_factors = []
	powers = []
	remainder=()

	c_lists = time.clock() - s_before_lists

	#initialise N_remainder
	N_remainder = N
	i=2	

	#call calc_primes_powers_remainder
	#print('Calculating prime factors, powers and initial remainder...')
	s_before_factorisations = time.clock()	
	#N=5 - gets listed as remainder instead of factor!!!	
	result2=calc_primes_powers_remainder(list,N_remainder)

	c_factorisations = time.clock() - s_before_factorisations

	prime_factors=result2[0] 
	powers=result2[1]
	remainder=result2[2]
	c_pps=result2[3]
	c_nrem=result2[4]
	mult_primes_powers=result2[5]

	return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem, mult_primes_powers

def calc_primes_powers_remainder(isliced_primes, N_remainder):

	prime_factors=[]
	powers=[]
	mult_primes_powers=[]
	remainder=()

	#Check if there are elements in prime list
	s_primefactors_powers = time.clock()
	if not isliced_primes:	
		#There are no elements in isliced_primes list		
		print("There are no elements in isliced_primes list??")		
		N_remainder=[]
		#remainder=[]
		
	else:
		#There are elements in primes list
		# N_remainder is not in isliced_primes:
		for prime in isliced_primes:
			#print("prime is now: "+str(prime))			
			prime_int=int(prime)
			#for N_remainder not in one:
			while N_remainder <> 1:
				if N_remainder % prime_int == 0:		
					#prime is a factor		
					#prime^m divides N_remainder, m integer
					m = MaxPower(prime_int,N_remainder)		
					prime_factors.append(prime_int)
					powers.append(m)
					mult_primes_powers.append(prime_int**m)
					N_remainder = N_remainder/(prime_int**m)
					break
				else:
					break
	c_primefactors_powers = time.clock() - s_primefactors_powers
	
	#Check if there are elements in N_remainder list
	s_nremainder = time.clock()
	if not N_remainder:	
		#There are no elements in N_remainder list		
		N_remainder=()
	else:
		#There are elements in N_remainder list
		if N_remainder <> 1:
			print('There is a remainder of: '+str(N_remainder))
		
		#check if N_remainder is also a prime
		if N_remainder > long(isliced_primes[-1]) and math.sqrt(N_remainder) <= isliced_primes[-1]:
			#N_remainder is prime since its square root is less than largest prime in prime list file, and all those primes have been checked earlier.			
			#print('Appending last prime factor and power..')
			prime_factors.append(N_remainder)
			powers.append(1)
			mult_primes_powers.append(N_remainder)
	
		elif N_remainder > long(isliced_primes[-1]) and math.sqrt(N_remainder) > isliced_primes[-1]:	
			#print('Appending remainder..')
			#remainder.append(N_remainder)
			#remainder.add(N_remainder)
			remainder=(N_remainder)
	c_nremainder = time.clock() - s_nremainder
	
	#Now set N_remainder to ''
	N_remainder=()
		
	#Return factors of N using factors() list
	#print("prime_factors: "+str(prime_factors)+", powers: "+str(powers)+", remainder: "+str(remainder))
	return prime_factors, powers, remainder, c_primefactors_powers, c_nremainder, mult_primes_powers

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


		#qi_list[i] = primes_list[i]
		#qi_list[i] = primes_list(i)
		#Wi_list.append(p_minus_1 % (qi_list[i]**ei_list[i]))
		#Wi_list[i] = p_minus_1 % (qi_list[i]**ei_list[i]) 	
		#gi_list[i] = g**Wi_list[i]
		#hi_list[i] = h**Wi_list[i]
		#zi_list[i] = hi_list[i] % p
		
		#print('qi is:'+str(qi_list[i]))
		#print('ei is:'+str(ei_list[i]))
		#print('Wi is:'+str(Wi_list[i]))
		#print('gi is:'+str(gi_list[i]))
		#print('hi is:'+str(hi_list[i]))
		#print('zi is:'+str(zi_list[i]))
		#print('Vi is:'+str(Vi_list[i]))

#Now zi_list[i] * yi_list[i] congruent to Vi mod p, where zi, Vi, p are known and yi are unknown

#8: Take first congruence; x = qi * t + yi for some t unknown.
	#k = 0
	#for C in C_tuples:
	#	print('congruence '+str(k)+' is: x = '+str(qi_list[k])+'* t + '+str(yi_list[k]))
		
	#9: Substitute first congruence in all other congruences.
	#Now 	q1 * t + y1 = y2 mod q2
	#...................................
	#	q1 * t + y1 = yC mod qC
	# where t are unknown.

	#q_to_e=result[2]
	#print "q_to_e is: "+str(q_to_e)

	# largest divisor = q**e
	# Does order = q**e? or does order = e ???

