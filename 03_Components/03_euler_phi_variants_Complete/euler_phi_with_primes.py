import math
#import csv

def main():

	#For if statements: O(T) - complexity of test, O(B1) - complexity of block, else: O(B2) - complexity of block,
	#Subtotal is O(T) + max(O(B1),O(B2)) 	


	print 'Enter number to be tested: '			
	n_initial = raw_input()					#1 op
	if n_initial.isdigit() is False:			#1 op
		print('You have not entered a positive integer for n. n is: '+str(n_initial)+'. Please reenter.')
		sys.exit()						#1 op

	#now convert n_initial into a long:
	n = long(n_initial)					#1 op

	ep = euler_phi_primesused(n)				#O(???)
	#return ep
	#result = euler_phi_primesused(n)
	#ep = result[0]
	#status = result[1]

	#print "ep is: "+str(ep)+", status is: "+str(status)

	print "euler_phi_primesused("+str(n)+" , primes) is: "+str(ep)	#1 op

def euler_phi_primesused(n):				
	
	#when n is not prime
	# Worst: O(sqrt(n)+8)  
	# Best:	O(4) when n=1

	#when n is prime
	#O(sqrt(n)+5) 
	
	#print "Running euler_phi_primesused("+str(n)+", primes).."
	
	#print "isprime_result is: "+str(isprime_result)

	#left_isprime_result=left()

	#status = True 					
	#floor_sqrt_n = math.floor(math.sqrt(n))

	#print "isprime(n) is: "+str(isprime(n)
	#print "isprime(n,floor_sqrt_n) is: "+str(isprime(n,floor_sqrt_n))
	#status=1 for not prime
	#status=0 for prime

	if n==1:					#O(1)	#subtotal O(2 ???)
		a = 1					#1 op storage, O(1 ???)
		#status = False				
		return a				#1 op
		#return a, status			
			
	else:							#subtotal O(max{sqrt(size(n)), factors*(fac_list + 2), prime_factors * 5, ??? - len(prime_factors)})
		#euler_phi(p**k) = (p-1)*p**(k-1) for prime p 
		#euler_phi(m*n) = euler_phi(m)*euler_phi(n) for coprime m & n

		#euler_phi(n) = n * Pi_{for p|n} (1-1/p), where product is over distinct prime numbers dividing n.
		#n = p_1**(k_1)*p_2**(k_2)*p_3**(k_3)... , where p_i are prime factors of n, and k_i are corresponding powers.
		#n, and P_i are known 
		#need primes from factorise()!
				
		factors = factorise(n)					#O(sqrt(size(n)))
		prime_factors = calc_prime_factors(factors)		#O(factors*(fac_list + 2))	#Best operations: ??? 
									#For large n this should be significantly less operations than factorise() takes
									#ie <= O(sqrt(size(n)))
		
		#print "prime factors are: "+str(prime_factors)
		
		len_prime_factors = len(prime_factors)		#1 ops calc, 1 op storage, O(1)

		#initialise ep
		ep = n						#1 op storage, O(1 ???)
		#print "ep initialised as: "+str(ep)

		for prime in prime_factors:			#O(prime_factors)	#subtotal O(prime_factors * 5)
			#now calculate first (1-1/p) for p|n
			#print "prime is: "+str(prime)
			#print "1 / float(prime) is: "+str(1 / float(prime))
			#print "1 / prime is: "+str(1 / prime)
			#term = 1 - 1 / float(prime)			
			#print "term is: "+str(term)
		
			#recalculate ep
			ep = ep * (1 - 1 / float(prime))		#4 ops calc, 1 op storage, O(???)
			#ep = ep * term					
			#print "ep is now: "+str(ep)

		ep = int(ep)					#1 op calc, 1 op storage,  O(1 ???)
		#print "final ep is: "+str(ep)

		#status = True				
		return ep					#1 op

def factorise(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print "Running factorise("+str(N)+").."	

	#Create lists to hold prime factors of N and corresponding powers
	factors = []					#O(1)
	
	#print "Calculating prime factors and powers"
	#s_before_factorisations = time.clock()	
	#N=5 - gets listed as remainder instead of factor!!!	
		
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
	if N > 1: factors.append(N)
		
	#c_factorisations = time.clock() - s_before_factorisations	#O(1)

	#print "factors are: "+str(factors)
	#print "c_factorisations are: "+str(c_factorisations)

	return factors		#O(1)
	#return factors, c_factorisations		#O(1)


def calc_prime_factors(factors):
	#O(factors*(fac_list + 2)) + O(2)	#Best: O(???)
	#O(factors*(fac_list + 2))

	#print "Running calc_powers.."
	#print "factors is: "+str(factors)

	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]					#1 op storage O(1 ???)
	fac_list = []						#1 op storage O(1 ???)
	
	for factor in factors:					#O(factors)	#Subtotal: 	#O(factors*(max{O(fac_list + 2),O(2)}) 
												#O(factors*(fac_list + 2))
										#Best: 4 operations
		#print "------------------"	
		#print "factor is: "+str(factor)		
		if factor not in fac_list:				#O(fac_list)	#Subtotal: O(fac_list + 2)	#Best: O(6)
			#factor is not in fac_list - add factor to prime_factors
			prime_factors.append(factor)				#1 op storage, O(1)
			#print "Added "+str(factor)+" to prime_factors"
			fac_list.append(factor)					#1 op storage, O(1)
			#print str(factor)+" added to fac_list"
				
		else:							#O(1)		#Subtotal: O(2)
			##store factor
			fac_list.append(factor)					#1 op storage, O(1)
			#print str(factor)+" added to fac_list"

	return prime_factors

if __name__=='__main__':
	main()

#def csvfile_store_primes(csv_filename_var):		### O(max{n,len(z1),1?}) ### 
		
#	with open(csv_filename_var,'r') as csvfile:
#		# Strip quotes, eol chars etc, and convert strings to integers
#		#Use generator to get number of primes to use in prime file..
#		#print 'Running generator..'
#		z1=(int(x) for row in csv.reader(csvfile) for x in row)			#O(n) - Potentially y rows and x items in each row, 
											# however only 1 row in csvfile being used. Hence x*y=x items to store
#		primes=list(z1)								#O(len(z1))
#		csvfile.close()								#O(1 ???)
#	return primes
