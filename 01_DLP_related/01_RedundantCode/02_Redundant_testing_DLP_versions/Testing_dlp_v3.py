#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 3. 07/12/2017.
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
print("Version 3. 07/12/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program attemps to test dlp.py for solving the Discrete Log Problem (DLP) for set inputs of g, h, and p, via factorisation of (p-1) where p is a prime number.")
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

	#define prime list
	#print('Importing primes from csv file')
	primes=csvfile_store_primes(primefile)
	#print('First ten primes are: '+str(primes[0:10]))

	#print(sys.version_info)

	g_values = xrange(2,51)
	h_values = xrange(1,51)
	#p_values = primes

	total_g_values=len(g_values)
	print("total_g_values: "+str(total_g_values))

	total_h_values=len(h_values)
	print("total_h_values: "+str(total_h_values))

	total_primes=len(primes)
	print("total_primes: "+str(total_primes))
	
	Grand_total_values = len(primes)*len(list(g_values))*len(list(h_values))
	print("Grand_total_values: "+str(Grand_total_values))

	#percent_thresholds=[]	
	#percent_thresholds[1]=total_values / 10
	#for x in xrange(2,11):
	#	percent_thresholds[x] = x * percent_thresholds[1]
	#print("percent_thresholds: "+str(percent_thresholds))

	#define counts for different types of results
	count_nosolns=0
	count_zi_bi_equal_1=0
	count_bi_equal_1_zi_ntequal_0_1=0
	count_x_equals_0=0
	count_Bi_equals_zi=0
	count_normal_soln=0
	count_needlargerprimelist=0
	count_notprime=0
	
	#define lists for different types of results
	answers_to_be_checked=[]

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	print("======================================")

	print('Running dlp()..')

	for p in primes:
		#print("======================================")
		print "p is: "+str(p)		
		for h in h_values:
			for g in g_values:			
				#print "p: "+str(p)+", h: "+str(h)+", g: "+str(g)				
				result = dlp(g,h,p, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_notprime)
				#return x_final, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, x_moduli_final, answers_to_be_checked
				#print "result is: "+str(result)
				#print "result[0] is: "+str(result[0])
				#print "result[8] is: "+str(result[8])
				#print "type of result[8] is: "+str(type(result[8]))
				
				answers_to_be_checked.append(result[8])

	print("======================================")
	print "Answers to be checked: "+str(answers_to_be_checked)

def ghp_checks(g,h,p,floor_sqrt_p, count_notprime):

	#print("-----------------------------")
	status=1
	
	#print("Running ghp_checks()..")

	#Need to check if p is prime
	#print('Checking if p is prime ..')
	#a = 1 for not prime
	a = isprime(p,floor_sqrt_p)	
	if a==1:
		print('The number entered for p: '+str(p)+' is not prime. Please choose a number that is prime for p.')
		status=0
		count_notprime = count_notprime + 1
		sys.exit()

	#Simple Checks for g, h & p:
	#print('Running simple checks on g..')
	if (g==0 or h==0 or p==0):
		print('One or more numbers entered for g, h and p are 0. Please choose numbers that are not 0.')
		status=0
		sys.exit()
	elif g==1:
		print('g = 1 has trivial solutions for the dlp. Please choose another number.')
	elif g<0:
		print('Number for g is negative. Please enter another number')
		status=0
		sys.exit()	
	
	return status

def chinese_remainder(x, x_moduli):
	#print "x are: "+str(x)
	#print "x_moduli are: "+str(x_moduli)
	cong=[]
	cong_x=[]
	cong_moduli=[]
	x_new=0
	M=0
	for number in xrange(0,len(x)):
		#print('--------------------')
		#print "number is: "+str(number)		
		#store values in 1st congruence	
		a= x[number]
		b= x_moduli[number]
		#print "x["+str(number)+"] is: "+str(x[number])
		#print "x_moduli["+str(number)+"] is: "+str(x_moduli[number])
		#print "cong currently is: "+str(cong)

		if not cong:
			#cong has no elements
			#Add values in first congruence			
			#print "Appending info from 1st congruence"
			cong_x.append(a)
			x_new = a		
			cong_moduli.append(b)
			M = b			
			cong.append(1)
		else:
			#print('--------------------')
			#cong has elements
			#print "Working on congruence number: "+str(number+1)
			#print "cong_x["+str(number-1)+"] is: "+str(cong_x[number-1])
			#print "cong_moduli["+str(number-1)+"] is: "+str(cong_moduli[number-1])
			#Subtract current cong_x[number-1] from current x[number]
			#print "Subtracting cong_x["+str(number-1)+"] from current x["+str(number)+"].."
			c = x[number] - cong_x[number-1]
			#print "c now is: "+str(c)				#c=
			
			#print "cong_moduli["+str(number-1)+"] to use in inverse is: "+str(cong_moduli[number-1]) 
			#number=
			#print "x_moduli[number] to use in inverse is: "+str(b)			#moduli=

			#now want to find (cong_moduli[number-1]**-1) mod(b)		
			f = calc_modinverse(cong_moduli[number-1], 1, b)
			#print "inverse is: "+str(f) 			#inverse=

			#now take c and times it by the inverse, f, and reduce mod b
			k = (c*f) % b			
			#print "k is: "+str(k)

			#now take value of k and use it to work out new value of x
			x_new = cong_x[number-1] + (cong_moduli[number-1] * k)
			#print "x_new is: "+str(x_new)
			cong_x.append(x_new)
			
			#now work out value of M
			M = cong_moduli[number-1] * b
			#print "M is now: "+str(M)
			cong_moduli.append(M)
	return x_new, M

def isprime(p,floor_sqrt_p):
	
	#print('Running isprime..')
	#print('p is: '+str(p))	
	status=0
	if p == 2:
		status=0
		#prime	
	elif p % 2 == 0:
		status=1
		#not prime
	
	#n=1
	n=3
	if status == 0 and p<>2:
		#print "floor_sqrt_p is: "+str(floor_sqrt_p)
		while n <= floor_sqrt_p:
			#print "n is: "+str(n)			
			if p % n == 0:
				status=1
				break 
			else:
				status=0
			n = n + 2
	
	#print('status is: '+str(status))	
	#status= 0 for prime
	#status= 1 for not prime
	return status		

def prim_root(g,p,primes):

	#print "Running prim_root.."	
	#print('Checking if '+str(g)+' is a primitive root mod '+str(p)+' ..')
	status=True
	result = euler_phi(p, primes)		
	ep=result[0]
	status_ep=result[1]
	#print "euler_phi("+str(p)+") is: "+str(ep)

	result=factorise(ep, primes)	
	prime_factors=result[0]
	powers=result[1]
	moduli=result[2]

	#print "prime_factors are: "+str(prime_factors)
	#print "powers are: "+str(prime_factors)
	power=1

	for prime in prime_factors:		
		if status==True:
			#print "================="
			#print "prime is: "+str(prime)
			power=1
			power_index = 0
			#print "power_index is: "+str(power_index)
			while power < powers[power_index]:
				#print "------------------"
				#print "power is: "+str(power)			
				if g**(ep / powers[power_index]**power) % p == 1:
					status=False	
					#print "Status is False!"				
					break
				power = power + 1
			power_index = power_index + 1

	return status, prime_factors, powers, moduli

def euler_phi(n, primes):
	
	#euler_phi(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.	
	
	#print "Running euler_phi()..."
	status = True 
	#floor_sqrt_n = math.floor(math.sqrt(n))	

	#print "isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#if isprime(n,floor_sqrt_n) == 1:
	#	#status=1 for not prime
	#	#p is not prime!		
	#	print str(n)+" is not prime!"
	#	sys.exit()		
	#elif n==1:	
	#	a = 1
	#else:
	#	a = n - 1

	##### We are presuming n=p is already prime!! ########
	a = n - 1	
	return a, status

#def check_answer(g, h, p, x, answers_to_be_checked):
#	if g**x % p <> h:
		#print "CHECK ANSWER!!!"
#		answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))
		
#	return answers_to_be_checked

#def dlp(g, h, p, primefile, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked):	

def dlp(g, h, p, primes, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, count_needlargerprimelist, answers_to_be_checked, count_notprime):

	#print('--------------------')

	floor_sqrt_p = math.sqrt(p)
	#floor_sqrt_p = int(math.floor(math.sqrt(p)))
	#print('floor_sqrt_p is: '+str(floor_sqrt_p))

	#Run checks on g, h & p	
	#count_notprime = 0
	result=ghp_checks(g, h, p, floor_sqrt_p, count_notprime) 

	if result == 0:
		sys.exit()

	#check if sqrt_p > largest element in primes
	#print('checking if square root of p > largest element in primes...')
	sqrt_p = math.sqrt(p)
	largest_prime = primes[-1]
	count_needlargerprimelist=0
	if sqrt_p > largest_prime:
		print('Square root of p - '+str(sqrt_p)+' is greater than largest prime in list - '+str(largest_prime)+'. Consider using a larger prime list. Exiting..')
		count_needlargerprimelist = count_needlargerprimelist + 1
		sys.exit()

	#Check if g is a primitive root mod p
	count_primroot=0
	result=prim_root(g,p,primes)
	status=result[0]
	prime_factors=result[1]
	powers=result[2]
	moduli=result[3]

	if result is False:
		print(str(g)+' is not a primitive root mod '+str(p)+'! Exiting ...')		
		sys.exit()
	else:
		#print(str(g)+' is a primitive root mod '+str(p))	
		count_primroot = count_primroot + 1

	#define counts for different types of results
	count_nosolns=0
	count_zi_bi_equal_1=0
	count_bi_equal_1_zi_ntequal_0_1=0
	count_x_equals_0=0
	count_Bi_equals_zi=0
	count_normal_soln=0
	count_primroot_sub=0

	#dlp is:  g**x congruent to h mod p, where g, h and p are known, p prime.

	#1st step: calculate p-1 from p
	p_minus_1 = p-1
	#print('p-1 is: '+str(p-1))	

	#2nd step: factorise p_minus_1 into product of prime powers
	#result=factorise(p_minus_1, primes)
	primes_list=prime_factors

	#print('=============================')

	#print('primes for factorisation of p-1 are:'+str(prime_factors))
	#print('powers for factorisation of p-1 are:'+str(powers))
	
	#print('=============================')

	#3: Calculate C - number of unique primes in factorisation (also is number of congruences to solve)
	C=0
	for prime in primes_list:
		C = C + 1		
	#print('Number of primes in primes_list = C = '+str(C))

	#4: Need to create a list (with C elements) for each of: q_i, e_i, W, g_i, h_i, z_i, & V_i 
	C_list=list(xrange(1,C+1))
	#print('C_list is: '+str(C_list))

	#5: initialise lists
	qi=[]
	ei=[]
	Wi=[]
	gi=[]
	hi=[]
	zi=[]
	Bi=[]
	Vi=[]

	#6: loop through each C calculating values & storing them
	x=[] 
	x_moduli=[]
	i = 0
	for C in C_list:
		#print('========================')
		#print('current C is:'+str(C))
		#print('i is: '+str(i))
		qi.append(primes_list[i])
		#print('qi['+str(i)+'] is: '+str(qi[i]))
		ei.append(powers[i])
		#print('ei['+str(i)+'] is: '+str(ei[i]))
		Wi.append(p_minus_1 / (qi[i]**ei[i]))		
		
		gi.append(g**Wi[i])
		#print('gi['+str(i)+'] is: '+str(gi[i]))
		Bi.append(gi[i] % p)
		#print('Bi['+str(i)+'] = gi['+str(i)+'] % p is: '+str(Bi[i]))
		
		hi.append(h**Wi[i])
		#print('hi['+str(i)+'] is: '+str(hi[i]))
		zi.append(hi[i] % p)
		#print('zi['+str(i)+'] = hi['+str(i)+'] % p is: '+str(zi[i]))
	
		#7: Now Bi[i]**x = zi[i] mod p for each i
		# Need to solve for x for each.
		#x=[] 
		#x_moduli=[]
		
		#print('Solving for x...')
		if Bi[i]==0 and zi[i]==1:
			#print('i is: '+str(i))
			#print('qi['+str(i)+'] is: '+str(qi[i]))
			#print('ei['+str(i)+'] is: '+str(ei[i]))
			#print 'No Solutions!!!'
			count_nosolns = count_nosolns + 1
			#sys.exit()
		elif Bi[i]==0 and zi[i]==0:
			#print('i is: '+str(i))
			#print('qi['+str(i)+'] is: '+str(qi[i]))
			#print('ei['+str(i)+'] is: '+str(ei[i]))
			#print 'No Solutions!!!'
			count_nosolns = count_nosolns + 1
			#sys.exit()
		elif Bi[i]==1 and zi[i]==0:
			#print('i is: '+str(i))
			#print('qi['+str(i)+'] is: '+str(qi[i]))
			#print('ei['+str(i)+'] is: '+str(ei[i]))
			#print 'No Solutions!!!'
			count_nosolns = count_nosolns + 1
			#sys.exit()
		elif Bi[i]==1 and zi[i]==1:
			#print('i is: '+str(i))
			#print('qi['+str(i)+'] is: '+str(qi[i]))
			#print('ei['+str(i)+'] is: '+str(ei[i]))
			#print 'CHECK - Bi[i] and zi[i] both equal 1?!'
			count_zi_bi_equal_1 = count_zi_bi_equal_1 + 1
			#sys.exit()
		elif Bi[i]==1:
			#print('i is: '+str(i))
			#print('qi['+str(i)+'] is: '+str(qi[i]))
			#print('ei['+str(i)+'] is: '+str(ei[i]))
			#print 'CHECK - Bi[i]=1 and zi[i]!=0 and zi[i]!=1 ?!'
			count_bi_equal_1_zi_ntequal_0_1 = count_bi_equal_1_zi_ntequal_0_1 + 1
			#sys.exit()
		elif Bi[i]<>0 and zi[i]==1:
			#result = prim_root(Bi[i],p,primes)
			#result = factorise(Bi[i],p)
			#status = result[0]
			#prime_factors = result[1]
			#powers = result[2]
			#prime_factors = result[0]
			#powers = result[1]

			#if status is False:
			#	print(str(Bi[i])+' is not a primitive root mod '+str(p)+'! Exiting ...')		
			#	sys.exit()
			#else:
				#print(str(Bi[i])+' is a primitive root mod '+str(p))	
			#	x.append(0)
				#print'added 0 to x[]'
			#	count_primroot_sub = count_primroot_sub + 1

			diff = a_exp_x_eq_r(Bi[i],p,1)			
			x_moduli.append(diff)			
			#print str(diff)+" appended to x_moduli"
			count_x_equals_0=count_x_equals_0 + 1
			#raw_input("Waiting for user")
		elif Bi[i] == zi[i]:
			x.append(1)
			#print str(1)+" appended to x"
			#this is where one needs to calculate the moduli!!!			
			diff = a_exp_x_eq_r(Bi[i],p, zi[i])
			x_moduli.append(diff)
			#print str(diff)+" appended to x_moduli"			
			count_Bi_equals_zi=count_Bi_equals_zi + 1
			#raw_input("Waiting for user")		
		else:
			#print('Checks done and trivial solutions not found.') 
			#print('Running prop_234 to solve for x...')
			result = prop_234(Bi[i], zi[i], qi[i], ei[i], p)
			x.append(result[0])
			#print str(result[0])+" appended to x"
			x_moduli.append(result[1])
			#print str(result[1])+" appended to x_moduli"
			count_normal_soln=count_normal_soln + 1
		#print('----------------------')
		i = i + 1

	#print('x\'s are: '+str(x))

	#now need to combine x's and x_moduli via CRT
	#print('========================')
	#print('Running chinese remainder..')
	result=chinese_remainder(x, x_moduli)
	x_final=result[0]
	x_moduli_final=result[1]

	#print "x_final is: "+str(x_final)
	if g**x_final % p <> h:
		#print "CHECK ANSWER!!!"
		answers_to_be_checked.append("g: "+str(g)+" h: "+str(h)+" p: "+str(p)+" x: "+str(x))

	#if not answers_to_be_checked:
	#	#answers_to_be_checked is empty
	#	answers_to_be_checked.append("empty")

	return x_final, count_nosolns, count_zi_bi_equal_1, count_bi_equal_1_zi_ntequal_0_1, count_x_equals_0, count_Bi_equals_zi, count_normal_soln, x_moduli_final, answers_to_be_checked


def a_exp_x_eq_r(a,p,r):
	x=1
	x_values=[]
	count=0
	while count < 3:
		#print "count is: "+str(count)		
		if a**x % p == r:
			#print "a**x % p is: "+str(r)
			x_values.append(x)
			#print str(x)+" appended to x_values"
			count=count+1
			if count==2:
				#x_values.append(x)
				#print str(x)+" appended to x_values
				diff = x_values[1] - x_values[0]				
				#diff = answer2 - answer1
				#print "diff is: "+str(diff)
				break
		x = x + 1
	return diff

def prop_234(Bi, zi, qi, ei, p):
	#Bi[var], zi[var], qi[var], ei[var], p
	#let x = x_0 +x_1*(q)+x_2*(q**2)+...+x_{e-1}q^(e-1), with 0 <= x_i < q, and determine successively x_1, x_2, ...

	#print "-----------------------------------"

	# constuct list of q_powers from 0 to e-1
	q_powers=[]
	if ei>0:
		for k in xrange(0,ei):
			q_powers.append(qi**k)

	#print "q_powers are: "+str(q_powers)

	#initialise g=Bi
	g=Bi	
	
	#initialise h=zi
	h=zi

	#now want to calculate xi using function	
	xi = calc_xi(q_powers, g, h, qi, ei, p)
	
	#print "xi are: "+str(xi)

	#print "---------------------------"
	
	#print "q_powers are: "+str(q_powers)	
	for q_power in q_powers: 
		#print "q_power is: "+str(q_power)
		#print "index of q_power is: "+str(q_powers.index(q_power))
		#print "xi[(q_powers.index(q_power))] is: "+str(xi[(q_powers.index(q_power))])		
		if q_power==1: 
			#print "Adding "+str(xi[q_powers.index(q_power)])+" to x"
			x = xi[q_powers.index(q_power)] 
			
		else:
			#print "Adding "+str(xi[(q_powers.index(q_power))])+"*"+str(q_power)+" to x, and reducing mod "+str(qi**ei)
			x = (x + xi[q_powers.index(q_power)]*q_power) % (qi**ei)
	M = qi ** ei
	#print("x is: "+str(x)+" mod "+str(M))		
	return x, M

def calc_xi(q_powers, g, h, qi, ei, p):
	#initialise xi, cumul_q_powers, cumul_xi_q_powers
	xi = len(q_powers) * [0]
	cumul_q_powers=[]
	cumul_xi_q_powers=[]

	#Loop through each q_power until xi are calculated
	for q_power in q_powers:
		if q_power==1:
			#solving for x_0
			#print("---------------------------")
			#print("q_power is: "+str(q_power))
			#print("Solving for xi[0] ..")
			#print("qi is: "+str(qi)) #qi = 
			#print("ei is: "+str(ei)) #ei = 
			lhs= (g**qi**(ei-1)) % p
			#print "g is: "+str(g) 			# g=
			#print "h is: "+str(h) 			# h=
			#print("lhs is: "+str(lhs)) 		# lhs=
			rhs= (h**qi**(ei-1)) % p
			#print("rhs is: "+str(rhs)) 		# rhs=
			for t in xrange(0, qi):
				if lhs**t % p ==rhs:
					xi[0]=t  # xi[0]=
					#print "xi[0] is: "+str(t)
					break

			cumul_xi_q_powers.append(xi[0])
			cumul_q_powers.append(1)
			#print "cumul_xi_q_powers after append: "+str(cumul_xi_q_powers)
			#print "cumul_q_powers after append: "+str(cumul_q_powers)
		else:
			#solving for x_n (n!=0)
			#print("---------------------------")
			#print("q_power is: "+str(q_power))
			xi_number = q_powers.index(q_power)
			#print("Solving for xi["+str(xi_number)+"] ..")
			#print "cumul_xi_q_powers before append: "+str(cumul_xi_q_powers)
			#print "cumul_q_powers before append: "+str(cumul_q_powers)
			
			#print "g is: "+str(g) # g=
			#print "h is: "+str(h) # h=
			#print("xi["+str(xi_number-1)+"] is: "+str(xi[xi_number-1])) # xi[0]=0
			
			#print("qi is: "+str(qi))	#qi = 
			#print("ei is: "+str(ei))	#ei = 
			
			#print "cumul_xi_q_powers is: "+str(cumul_xi_q_powers)
			#print "cumul_q_powers is: "+str(cumul_q_powers)
			
			z=0
			for cumul_xi_q_power in cumul_xi_q_powers:
				z = z + cumul_xi_q_power
				
			#print "sum_cumul_xi_q_power is now: "+str(z)

			if xi[xi_number-1] >= 0:
				#need to work out what g**-[x_0+x_1*q_power+x_2*q_power**2 + ...], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
				#print("xi["+str(xi_number-1)+"] >= 0")
				#print("Calculating modular inverse of "+str(g)+"**"+str(-z)+", mod "+str(p))
				#print("Calculating modular inverse of "+str(g)+"**"+str(-xi[xi_number-1])+", mod "+str(p))				
				b = calc_modinverse(g, z, p)
				#b = calc_modinverse(g, xi[xi_number-1], p) #b = 5
				#print("inverse is: "+str(b)) #b = 5
				
				#(ei - xi_number - 1)

				#print "(h * b)**qi**(ei - xi_number - 1) % p is: "+str((h * b)**qi**(ei - xi_number - 1) % p)
				rhs = (h * b)**qi**(ei - xi_number - 1) % p

				#print("(h * b)**qi**(ei-2) % p is: "+str((h * b)**qi**(ei-2)))
				#rhs = (h * b)**qi**(ei-2) % p				

				#print("rhs is: "+str(rhs))
			else:
				#print("xi["+str(xi_number-1)+"] is negative !!! CHECK")				
				sys.exit()			
			#print "lhs is: "+str(lhs)
			#print "rhs is: "+str(rhs)

			#print("rhs is: "+str(rhs))
			#print "qi is: "+str(qi)
			for t in xrange(0, qi):
				#print "t is now: "+str(t)					
				#print(str(lhs)+"**"+str(t)+" % "+str(p)+" is: "+str(lhs**t % p))
				if lhs**t % p ==rhs:
					xi[xi_number]=t
					#print "xi["+str(xi_number)+"] is: "+str(t)					
					break
			cumul_xi_q_powers.append(q_power * xi[xi_number])
			#print("Appended "+str(q_power * xi_number)+" to cumul_xi_q_powers")
			cumul_q_powers.append(q_power)
			#print("Appended "+str(q_power)+" to cumul_q_powers")
			#print("xi["+str(xi_number)+"] is: "+str(xi[xi_number]))
			#print "xi are now:"+str(xi)
			#print "cumul_xi_q_powers after append: "+str(cumul_xi_q_powers)
			#print "cumul_q_powers after append: "+str(cumul_q_powers)
	return xi

def calc_modinverse(g, power, p):
	#print "----------------"
	#print "g is: "+str(g)
	#print "power is: "+str(power)
	#print "p is: "+str(p)
	
	#floor_sqrt_p = math.floor(p)

	#this only works for p being prime!	
	result=g**(p-2)% p
	#print str(g)+"**(-1) mod "+str(p)+" is: "+str(result)
	
	c = result**power % p
	
	#print str(g)+"**(-"+str(power)+") mod "+str(p)+" is: "+str(c)
	return c

def MaxPower(i,N_remainder):
	m=0
	while N_remainder > 1 and not N_remainder % i:	
		m += 1		
		N_remainder //= i
	return m

def max_element_below_or_equal_target(List,target):
	if target in List:
		return List.index(target)
	elif target > List[-1]:
		#Target value is not in list. Return index of last number in list.
		return List.index(List[-1])
	elif target < List[-1]:
		#Target value is less than largest prime in list
		# start from 2 and increase until last number is found that is less than target.
		i=0
		while List[i] < target:
			i = i + 1 
		return i
	else:
		print 'List[-1] is: '+str(List[-1])
		print 'target is: '+str(target)	
		print "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))
		return "Other Error - Troubleshoot! list.index(target) is: "+str(list.index(target))+", target is: "+str(list.index(target))

def csvfile_store_primes(csv_filename_var):

	with open(csv_filename_var,'r') as csvfile:
		# Strip quotes, eol chars etc, and convert strings to integers
		#Use generator to get number of primes to use in prime file..
		#print 'Running generator..'
		z1=(int(x) for row in csv.reader(csvfile) for x in row)
		primes=list(z1)
		csvfile.close()	
	return primes

def factorise(N,list):		
	#print("Running factorise()...")
	
	#Create lists to hold prime factors of N, corresponding powers and any remainder
	s_before_lists = time.clock()	
	prime_factors = []
	powers = []
	remainder=()

	c_lists = time.clock() - s_before_lists

	#initialise N_remainder
	N_remainder = long(N)
	i=2	

	#call calc_primes_powers_remainder
	#print('Calculating prime factors, powers and initial remainder...')
	s_before_factorisations = time.clock()	
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
			#print "type(N_remainder) is: "+str(type(N_remainder))
			#print "type(prime_int) is: "+str(type(prime_int))
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
			remainder=(N_remainder)
	c_nremainder = time.clock() - s_nremainder
	
	#Now set N_remainder to ''
	N_remainder=()
		
	#Return factors of N using factors() list
	return prime_factors, powers, remainder, c_primefactors_powers, c_nremainder, mult_primes_powers

def size_input_check(input_number):

	#if size of number >= 2*10^8 then return message about memory & exit
	if input_number>2*(10**8):
		print('Number to attempt to factorise is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..')
		sys.exit()

if __name__=='__main__':
	main()

#def egcd(a, b):
#	print("Running egcd("+str(a)+","+str(b)+")")
#	print "a is: "+str(a)
#	print "b is: "+str(b)	
#	if a == 0:
#		return (b, 0, a)
#	g, y, x = egcd(b % a, a)
#	print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
#	return (g, x - (b//a) * y, y)

#def modinv(a, m):
#	### This needs further work! ###
#	print("Running modinv("+str(a)+","+str(m)+")")	
#	print "a is: "+str(a)
#	print "m is: "+str(m)	
#	#egcd(a, m)
#	g, x, y = egcd(a, m)
#	if g != 1:
#		raise Exception('No Modular Inverse') 
#	print("x mod m is: "+str(x % m))	
#	return x % m

#def number_checks(number):
#
#	#Simple Checks for N:
#	#print('Running simple checks for number...')
#	if number==0:
#		print('Number entered is 0. Please choose another value for N')
#		sys.exit()
#	if number==1:
#		print('1 doesn\'t have a prime power factorisation. Please choose another number.')
#		sys.exit()
#	if number<0:
#		print('Number entered is negative. Please enter another number')
#		sys.exit()

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


#Use Euclids algorithm forward & reverse to find inverses where required
	
	#euclid_f=[]
	#euclid_r=[]
	#yi=[]
	#j = 0
	#for C in C_tuples:	
	#	euclid_f=euclid_forward(zi_list[j],Vi_list[j],p)
	#	euclid_r=euclid_reverse(euclid_f[0],euclid_f[1],p)
	#	yi[j]=euclid_r[0]	
	#	j = j + 1

	#Now x = yi mod qi for each record

#=================================

#evaluate x_i for qi and ei:
	#for q_power in q_powers:
	#	#print("q_power is: "+str(q_power))
	#	if q_power==1:
	#		#solving for x_0
	#		print("---------------------------")
	#		print("q_power is: "+str(q_power))
	#		print("Solving for xi[0] ..")
	#		#need to solve (g**q**(e-1))*x_0 = h**q**(e-1), mod q**(e-1)
	#		#eg g=3, h=5, p=101. Hence (3**5**1)*x_0 = 101**5**1, mod 5**1 
	#		print("qi is: "+str(qi)) #qi = 5
	#		print("ei is: "+str(ei)) #ei = 2
	#		moduli = p		
	#		print("moduli is: "+str(moduli))
	#		lhs= (g**qi**(ei-1)) % p
	#		print "g is: "+str(g) 			# g=81
	#		print "h is: "+str(h) 			# h=9
	#		print("lhs is: "+str(lhs)) 		# lhs=1
	#		rhs= (h**qi**(ei-1)) % p
	#		print("rhs is: "+str(rhs)) 		# rhs=4
	#		for t in xrange(0, qi):
	#			if lhs**t % p ==rhs:
	#				xi[0]=t  # xi[0]=0
	#				break

	#		print "xi are:"+str(xi)
	#		if not xi[0]:
	#			print("xi[1] not found!!!")
	#			sys.exit()
	#		print("xi[0] is: "+str(xi[0]))
			#print("---------------------------")
	#	elif q_power==qi:
			#solving for x_1
	#		print("---------------------------")
	#		print("q_power is: "+str(q_power))
	#		print("Solving for xi[1] ..")
			#need to solve (g**q**(e-1))*x_1 = (h*(g**[-x_0]))**q**(e-2), mod q**(e-1)
			#eg g=3, h=5, p=101. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
	#		print "g is: "+str(g) # g=81
	#		print "h is: "+str(h) # h=19
	#		print("xi[0] is: "+str(xi[0])) # xi[0]=0
			
	#		print("qi is: "+str(qi))	#qi = 5
	#		print("ei is: "+str(ei))	#ei = 2
			#moduli = p			
	#		print("moduli is: "+str(p))
			
			#b=-x_0
	#		if xi[0] > 0:
				#need to work out what g**[-x_0], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
	#			print("xi[0] > 0")
	#			print("Calculating modular inverse of "+str(g)+"**"+str(-xi[0])+", mod "+str(p))				
	#			b = calc_modinverse(g, xi[0], p) #b = 5
				#print("inverse is: "+str(b)) #b = 5
	#			rhs = (h * b)**qi**(ei-2) % p #rhs = (19 * 5) % 101 = 95 % 101				
				#print("rhs is: "+str(rhs))
	#		elif xi[0]==0:
				#g**[x_0]=g**0=1, mod p
				#Hence h*(g**[-x_0]) = h, mod p
	#			print("xi[0] = 0")
				#rhs= (h*g**(-x_0))**qi**(e-2)% p
				#Thus rhs = (h)**qi**(e-2) % p
	#			print("h**qi**(ei-2) % p is: "+str(h**qi**(ei-2)))
	#			rhs = (h**qi**(ei-2)) % p
	#			print("rhs is: "+str(rhs))	
	#		else:
	#			print("xi[0] is negative !!! CHECK")				
	#			sys.exit()			
	#		print "lhs is: "+str(lhs)
	#		print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
	#		print "qi is: "+str(qi)
	#		for t in xrange(0, qi):
	#			print "t is now: "+str(t)					
	#			print(str(lhs)+"**"+str(t)+" % "+str(p)+" is: "+str(lhs**t % p))
	#			if lhs**t % p ==rhs:
	#				xi[1]=t
					#print "xi[1] is: "+str(t)					
	#				break
	#		if not xi[1]:
	#			print("xi[1] not found!!!")
	#			sys.exit()
	#		print("xi[1] is: "+str(xi[0]))
	#	elif q_power==qi**2:
			#solving for x_2 
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for xi[2] ..")
			#need to solve (g**q**(e-1))*x_2 = (h*(g**[-x_0-x_1*q]))**q**(e-3), mod p
			#eg g=3, h=5, p=113. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
	#		print "g is: "+str(g) # g=81
	#		print "h is: "+str(h) # h=19
	#		print("xi[0] is: "+str(xi[0])) # xi[0]=1		
	#		print("xi[1] is: "+str(xi[1])) # xi[1]=1			
	#		print("qi is: "+str(qi))	#qi = 2
	#		print("ei is: "+str(ei))	#ei = 4			
	#		print("moduli is: "+str(p))	#moduli = 113
			
			#b=-x_0
	#		if xi[0]+xi[1]*qi > 0:
				#need to work out what g**[-x_0], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
	#			print("xi[0]+xi[1]*qi > 0")
	#			print("Calculating modular inverse of "+str(g)+"**"+str(-(xi[0]+xi[1]*qi))+", mod "+str(p))				
	#			b = calc_modinverse(g, xi[0]+xi[1]*qi, p) #b = 35
				#print("b is: "+str(b)) #b = 65
	#			rhs = (h * b)**qi**(ei-3) % p #rhs = (40 * 35) % 113 = 18 % 113				
				#rhs = (h * b)**qi**(ei-3)
				#print("rhs is: "+str(rhs))

	#		elif xi[0]+xi[1]*qi ==0:
				#g**[x_0]=g**0=1, mod p
				#Hence h*(g**[-x_0]) = h, mod p
	#			print("xi[0]+xi[1]*qi = 0")
				#rhs= (h*g**(-x_0))**qi**(e-2)% p
				#Thus rhs = (h)**qi**(e-2) % p
	#			print("h**qi**(ei-3) % p is: "+str(h**qi**(ei-3)))
	#			rhs = (h**qi**(ei-3)) % p
	#			print("rhs is: "+str(rhs))	
	#		else:
	#			print("xi[0]+xi[1]*qi is negative !!! CHECK")				
	#			sys.exit()			
	#		print "lhs is: "+str(lhs)
	#		print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
	#		for t in xrange(0, qi):
				#print "t is now: "+str(t)					
	#			if lhs**t % p ==rhs:
	#				xi[2]=t
	#				print "xi[2] is: "+str(t)					
	#				break
	#	elif q_power==qi**3:
			#solving for x_3
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for x_3 ..")

			#need to solve (g**q**(e-1))*x_2 = (h*(g**[-x_0-x_1*q]))**q**(e-3), mod p
			#eg g=3, h=5, p=113. Hence (3**5**1)*x_1 = 5*[(3)**(5-x_0)]**5**0
	#		print "g is: "+str(g) # g=81
	#		print "h is: "+str(h) # h=19
	#		print("xi[0] is: "+str(xi[0])) # xi[0]=1		
	#		print("xi[1] is: "+str(xi[1])) # xi[1]=1			
	#		print("xi[2] is: "+str(xi[1])) # xi[2]=1			
	#		print("qi is: "+str(qi))	#qi = 2
	#		print("ei is: "+str(ei))	#ei = 4			
	#		print("moduli is: "+str(p))	#moduli = 113
			
			#b=-x_0
	#		if xi[0]+xi[1]*qi+xi[2]*qi**2 > 0:
				#need to work out what g**[-x_0], mod p is!!!
				#result = calc_modinverse(g, xi[0], p)
				#rhs = result[0]
	#			print("xi[0]+xi[1]*qi+xi[2]*qi**2 > 0")
	#			print("Calculating modular inverse of "+str(g)+"**"+str(-(xi[0]+xi[1]*qi+xi[2]*qi**2))+", mod "+str(p))				
	#			b = calc_modinverse(g, xi[0]+xi[1]*qi+xi[2]*qi**2, p) #b = 35
				#print("b is: "+str(b)) #b = 65
	#			rhs = (h * b)**qi**(ei-4) % p #rhs = (40 * 35) % 113 = 18 % 113				
				#rhs = (h * b)**qi**(ei-4)
				#print("rhs is: "+str(rhs))

	#		elif xi[0]+xi[1]*qi+xi[2]*qi**2 ==0:
				#g**[x_0]=g**0=1, mod p
				#Hence h*(g**[-x_0]) = h, mod p
				#rhs= (h*g**(-x_0))**qi**(e-2)% p
				#Thus rhs = (h)**qi**(e-2) % p
	#			print("h**qi**(ei-4) % p is: "+str(h**qi**(ei-4)))
	#			rhs = (h**qi**(ei-4)) % p
	#			print("rhs is: "+str(rhs))	
	#		else:
	#			print("xi[0]+xi[1]*qi+xi[2]*qi**2 is negative !!! CHECK")				
	#			sys.exit()			
	#		print "lhs is: "+str(lhs)
	#		print "rhs is: "+str(rhs)

			#raw_input('Waiting for user..')

			#print("rhs is: "+str(rhs))
	#		for t in xrange(0, qi):
				#print "t is now: "+str(t)					
	#			if lhs**t % p ==rhs:
	#				xi[3]=t
	#				print "xi[3] is: "+str(t)					
	#				break
	#	elif q_power==qi**4:
	#		#solving for x_4
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for x_4 ..")
	#	else:
			#solving for x_n .. ??
	#		print "-----------------------------------"
	#		print("q_power is: "+str(q_power))
	#		print("Solving for x_n ??..")
	#raw_input('Waiting for user..')


# Now need to contruct formulae for x = x_{0} +x_{1}*(q)+x_{2}*(q**2)+...+x_{e-1}q^(e-1)
	#print "e - 1 is: "+str(e-1)
	#for  in xrange(0, e+1): 
		#1st loop: x= x_0
		#2nd loop: x= x_0 + x_1(q)
		#3rd loop: x= x_0 + x_1(q) + x_2(q**2)
	#	x = j

	#initialise x
	#x=0	

#def a_exp_x_eq_1(a,p):
#	x=1
#	x_values=[]
#	count=0
#	while count < 3:
#		#print "count is: "+str(count)		
#		if a**x % p ==1:
#			#print "a**x % p is: "+str(a)
#			x_values.append(x)
#			#print str(x)+" appended to x_values"
#			count=count+1
#			if count==2:
#				#x_values.append(x)
#				#print str(x)+" appended to x_values
#				diff = x_values[1] - x_values[0]				
#				#diff = answer2 - answer1
#				#print "diff is: "+str(diff)
#				break
#		x = x + 1
#	return diff

#def prim_root_old(g,p):
#
#	print('Checking if '+str(g)+' is a primitive root mod '+str(p)+' ..')
#	status=True
#	F_p_star=[]	
#	for j in xrange(0,p-1): #eg for p=9: 0,1,2,3, .. ,7  
#		#F_p_star[j]=(g**j)%p	
#		if ((g**j)%p in F_p_star) and j<>0:
#			status=False
#			break
#		else:
#			F_p_star.append((g**j)%p)
#	return status
