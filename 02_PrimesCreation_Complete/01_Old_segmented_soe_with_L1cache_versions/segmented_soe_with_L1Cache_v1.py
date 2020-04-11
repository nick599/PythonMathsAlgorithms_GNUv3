#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 1. 02/11/2017.
#Programmed & tested in Python 2.76 only
#This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive using sieve of eratosthenes - using a segmented sieve.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
import math
import csv
import os.path
import time
import itertools
import numpy

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 1. 02/11/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive using sieve of eratosthenes - using a segmented sieve.")
print("It has been tested on Linux Mint v3.19 x64.")
print("Using Lists instead of sets for storage to minimise memory usage.")
print("---------------------------------------------------------------------")

def main():
	#store size of L1 CPU cache in bytes
	L1D_CACHE_SIZE = 32768 #32*1024 = 32Kbytes	
	
	print('What is the largest number you want primes to go upto in the prime list?')	
	N_initial = raw_input()
	if N_initial.isdigit() is False:
		print('You have not entered an integer. Please reenter.')
		sys.exit()

	#now convert type for N into a long:
	N = long(N_initial)
	
	#Simple Checks for N:
	if N==0:
		print('Number entered is 0. Please choose another number.')
		sys.exit()
	if N==1:
		print('1 is not a prime. Please choose another number.')
		sys.exit()
	if N<0:
		print('Number entered is negative. Please enter another number')
		sys.exit()

	#store square root of N, and set segment_size to be same as CPU's L1 data cache size
	sqrt_N = math.sqrt(N)
	segment_size = L1D_CACHE_SIZE

	#Now need to generate sieving primes less than sqrt_N - which are needed to cross off multiples
	


	#1) Then start crossing off the multiples of first prime 2 until we reach a multiple of 2 = m >= segment_size. 


		#2) when m >= segment_size, calculate index of that multiple in the segment using (m - segment_size), and store in a list


	#Repeat process 1) and 2) crossing off multiples of the next sieving primes using same process.

	

	#Once all multiples of the sieving primes have been crossed off in first segment, iterate over the sieve list and print out / count primes


	#in order to sieve the next segment sieve array is reset, and increment the lower offset by segment_size.


	#then start crossing-off multiples again, for each sieving prime retrieve the sieve index from list, and start crossing off multiples from there on.

 





	print('Now creating list of segments, sized <= square root of '+str(N))
	s_evalsegments = time.clock()
	segments=create_segments(N)
	c_evalsegments = time.clock() - s_evalsegments
	#print(segments)

	#raw_input('Waiting for user..')

	total_memory_used_inlists = sys.getsizeof(segments)
	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))+' bytes.'

	# Eval even integers ###################################################
	#N=10000	
	#100 segments of size 100 for N=10000
	marked_nos=[]
	print('Now populating marked_numbers with even numbers <= '+str(N))
	s_evalevens = time.clock()	
	for segment in segments:	
		#There are math.ceil(math.sqrt(N)) segments				
		#-- O(N) since 'x in s' and segments is a list'
		#print'-----------------------------------'
		#print'Segment is: '+str(segment)
		#print'Segment[0] is: '+str(segment[0])
		#print'Segment[1] is: '+str(segment[1])
		#100 elements in each segment for N=10000 		
		for element in segment:	
		#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
		#-- O(N) since 'x in s' and segments is a list'
			#print'element is: '+str(element)
			if (element == 2 or element == 3):
				continue				
				#primes.append(element)
			else:
				marked_nos = even_integers(element)
	c_evalevens = time.clock() - s_evalevens

	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)
	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))

	# Eval odd integers ###################################################
	print('Now creating list of odd integers <= '+str(N))
	#N=10000	
	#100 segments of size 100 for N=10000
	s_evalodds = time.clock()	
	#There are math.ceil(math.sqrt(N)) segments 
	#O(N) since 'x in s' and segments is a list'	
	for segment in segments:	
		#print'-----------------------------------'
		#print'Segment is: '+str(segment)
		#print'Segment[0] is: '+str(segment[0])
		#print'Segment[1] is: '+str(segment[1])
		#100 elements in each segment for N=10000 		
		if (segment[0] == 2 and segment[1] == 3):
			continue				
				#primes.append(element)
		else:
			for element in segment:	
			#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
			#O(N) since 'x in s' and segments is a list'
				#print'element is: '+str(element)
			#if (element == 2 or element == 3):
			#	continue				
			#	#primes.append(element)
			#else:
				result1 = odd_integers(element)
				odd_ints = result1[0]
				c_oddintegers = result1[1]
	c_evalodds = time.clock() - s_evalodds

	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)+sys.getsizeof(odd_ints)
	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))

	# Eval marked numbers ###################################################
	print('Now updating list of marked numbers <= '+str(N))
	#N=10000	
	#primes=[]
	#100 segments of size 100 for N=10000
	s_evalmarkednos = time.clock()	
	for segment in segments:	
		#There are math.ceil(math.sqrt(N)) segments 			#O(N) since 'x in s' and segments is a list'
		#print'-----------------------------------'
		#print'Segment is: '+str(segment)
		#print'Segment[0] is: '+str(segment[0])
		#print'Segment[1] is: '+str(segment[1])
		#if (segment[0] == 2 or segment[1] == 3):
		#	continue		
		#	#primes.append(element)
		#else:
		#100 elements in each segment for N=10000 		
		for element in segment:	
			#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
			#O(N) since 'x in s' and segments is a list'
			#print'element is: '+str(element)
			#if (element == 2 or element == 3):
			#	continue		
			#	#primes.append(element)
			#else:
			result2 = marked_numbers(marked_nos,odd_ints,element)
			marked_nos = result2[0]
			c_markednumbers = result2[1]
	c_evalmarkednos = time.clock()- s_evalmarkednos	

	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)+sys.getsizeof(odd_ints)
	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))

	# Eval Primes ###################################################
	#N=10000	
	primes=[]
	#100 segments of size 100 for N=10000
	print('Now creating list of primes <= '+str(N))
	s_evalprimes=time.clock()	
	for segment in segments:	
		#There are math.ceil(math.sqrt(N)) segments 
		#O(N) since 'x in s' and segments is a list'
		#print'-----------------------------------'
		#print'Segment is: '+str(segment)
		#100 elements in each segment for N=10000 		
		if (segment[0] == 2 or segment[1] == 3):
			primes.append(element)
		else:
			for element in segment:	
		#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
		#O(N) since 'x in s' and segments is a list'
			#print'element is: '+str(element)
			#if (element == 2 or element == 3):
			#	primes.append(element)
			#else:
				result3 = primes_list(marked_nos, primes, odd_ints, element)
				primes = result3[0]
				c_primes = result3[1]
	c_evalprimes = time.clock()- s_evalprimes

	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)+sys.getsizeof(odd_ints)+sys.getsizeof(primes)
	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))

	# Now free memory in segments list
	print('Resetting segments ..')
	segments=""

	# Now free memory in odd integers
	print('Resetting odd_ints..')
	odd_ints=""

	# Now free memory in marked numbers
	print('Resetting marked_nos..')
	marked_nos=""

	prime_list_path="/home/mint/Desktop/"
	prime_list_filename='primes_upto_'+str(N)+'.csv'
	primefile=prime_list_path + prime_list_filename
	
	#Check if primefile already exists.
	if os.path.exists(primefile) is False: 
		print('Now creating file for primes in prime list upto '+str(N))
		csvfile_create(primes,primefile)
	else:
		print('Prime file already exists in that location. Existing prime file will be deleted before new one is created.')
		os.remove(primefile)
		csvfile_create(primes,primefile)
		print('Prime list for primes upto '+str(N)+' created.')
	
	# Now free memory in primes list
	print('Resetting primes list ..')
	primes=""

	#print'Even integers are now: '+str(marked_nos)
	print'Odd integers are now: '+str(odd_ints)
	print'Marked numbers are now: '+str(marked_nos)
	print'Primes are now: '+str(primes)

	print 'Time to evaluate segments: '+str(c_evalsegments)
	print 'Time to create odd integers list: '+str(c_oddintegers) 
	print 'Time to create marked numbers list: '+str(c_markednumbers)
	print 'Time to create prime list: '+str(c_primes)

	print'End memory used by segments: '+str(sys.getsizeof(segments))
	#print'Memory used by even integers: '+str(sys.getsizeof(marked_nos))
	print'End memory used by odd integers: '+str(sys.getsizeof(odd_ints))
	print'End Memory used by marked numbers: '+str(sys.getsizeof(marked_nos))
	print'End Memory used by primes: '+str(sys.getsizeof(primes))


def create_segments(N):
	#Step 1a
	#Divide the range 2 through N into segments S, where size(S) <= math.sqrt(N)
	#Store list of 2 through N 	
	N_range=list(xrange(2,N))
	
	#Calc and store segment_size & segment_count
	#segment_size_decimal = math.sqrt(N)
	#print 'segment_size_decimal is: '+str(segment_size_decimal)
	segment_size = int(math.ceil(math.sqrt(N)))
	print 'segment_size is: '+str(segment_size)
	segments=list(split_every(segment_size,N_range))
	return segments

#def prime_list_create(N):
	

def split_every(n, iterable):
	i=iter(iterable)
	piece=list(itertools.islice(i,n))
	while piece:
		yield piece
		piece = list(itertools.islice(i,n))

def even_integers(N):
	#Step 1a
	#Find the primes upto S, using 'regular' sieve
	
	#Step 2a
	#Initialise marked_numbers
	marked_nos=[]

	#Step 2b
	#Populate marked_numbers with even numbers >= 4 upto including N
	j=4	
	#print('Appending even numbers <= '+str(N)+' to marked_numbers list')
	#print('Populating marked_numbers tuple with 4 <= even numbers <= '+str(N)+'...')
	s_evenintegers=time.clock()
	while j<=N:
		#a = marked_numbers + (j,)
		#marked_numbers = a[1:]
		#marked_numbers=marked_numbers+(j,)
		#marked_numbers.add(j)
		marked_nos.append(j)
		j+=2
	c_evenintegers=time.clock()-s_evenintegers
	#print'Memory used by even integers: '+str(sys.getsizeof(marked_numbers))
	return marked_nos

def odd_integers(N):
	odd_integers=[]
	n=3
	#Step 2 
	#create list of all positive odd_integers from 2 upto including N
	#eg N=10000
	#print('Appending odd integers <= '+str(N)+' to odd_integers list')
	#print('creating odd_integers tuple for odd_integers upto '+str(N)+'...')
	#- This takes O(N) operations
	s_oddintegers=time.clock()	
	while n<=N:
		#b = odd_integers + (n,)
		#odd_integers = b[1:]
		#odd_integers=odd_integers+(n,)
		#odd_integers.add(n)
		odd_integers.append(n)
		n+=2
	c_oddintegers=time.clock()-s_oddintegers
	#small_set=set(itertools.islice(odd_integers, 10))
	#print('small_set is: '+str(small_set))
	#small_list=list(itertools.islice(odd_integers, 10))	
	#print('small_list is: '+str(small_list))
	#print('slice of odd_integers[0:10]: '+str(odd_integers[0:10])+' ...')
	#print'Memory used by odd integers: '+str(sys.getsizeof(odd_integers))
	return odd_integers, c_oddintegers
	
def marked_numbers(marked_nos, odd_integers, N):
	#Step 3
	#initialise p
	p=3
		
	#Step 4
	#enumerate multiples of p by counting to N from 2p in increments of p, and store them in marked_numbers list.
	#print('Updating marked numbers list for odd_integers <= '+str(N)+'...')
	#======Total time complexity for step 3 is O(N^4) !!!======
	s_markednumbers=time.clock()
	#print("type of odd_integers is: "+str(type(odd_integers))) #list
	#print(odd_integers[0])
	#print("odd_integers[0] is: "+str(odd_integers[0]))
	for odd_integer in odd_integers:  
	#--- This takes upto O(N) operations, average O(1) operations due to "x in s" and is a set.
		floor_sqrt_oddint = math.sqrt(odd_integer)	
		#print('odd_integer now is: '+str(odd_integer))		
		#if floor_sqrt_oddint in marked_numbers:
			#no need to add since it & its multiples would be already in marked_numbers			
			#print('no need to add '+str(odd_integer)+' since it & its multiples are already in marked_numbers')	
			#break
		#else:
		if floor_sqrt_oddint not in marked_nos:
			if odd_integer not in marked_nos:
			#--- This takes upto O(N) operations, average O(1) operations due to "x not in s" and is a set.
				#next marked number to be added
				p=odd_integer
				#print('next odd_integer to try is: '+str(p))
				#every time marked_numbers function is called it takes O(N^2) operations
				marked_numbers=marked_numbers_update(p, N, marked_nos) 
				#print('multiples of '+str(p)+' added to marked_numbers')		
				#print('marked_numbers are now: '+str(marked_numbers))
				#increment p
				p=p+1
	
			#elif odd_integer not in marked_numbers: 
			#--- This takes upto O(N) operations, average O(1) operations due to "x not in s" and is a set.
				#next marked number to be added
			#	p=odd_integer
				#p=odd_integer**2
				#print('next odd_integer to try is: '+str(p))
			#	marked_numbers=marked_numbers_update(p, N, marked_numbers) #every time function is called it takes O(N^2) operations
			#	print('multiples of '+str(p)+' added to marked_numbers')		
				#print('marked_numbers are now: '+str(marked_numbers))
				#increment p
			#	p=p+1	

			#print('marked_numbers for N='+str(N)+' are now: '+str(marked_numbers))
	c_markednumbers=time.clock() - s_markednumbers	
	#print'Memory used by marked numbers: '+str(sys.getsizeof(marked_numbers))
	return marked_nos, c_markednumbers		

def primes_list(marked_nos, primes, odd_integers, N):
	#Step 4
	#Total time complexity for step 4 is between O(N) and O(N^2)
	
	#create list of primes
	primes=[]
	s_primes=time.clock()
	#Add first prime
	primes.append(2)

	#print('creating primes list for primes upto '+str(N)+'...')
	for odd_integer in odd_integers: 		#This takes O(N) operations
		if odd_integer not in marked_nos: 	#This takes average of O(1) operations (worst case O(N)) due to "x not in s" & marked_numbers is a set.
			#print('Appending '+str(odd_integer)+' to primes list..')
			primes.append(odd_integer)
	c_primes=time.clock() - s_primes
	#print'Memory used by primes: '+str(sys.getsizeof(primes))

	return primes, c_primes

def marked_numbers_update(p, N, marked_nos):  
#Whole function takes O(N^2) operations
	n=2	
	#chunk=[]
	while n*p <= N:  					#This takes O(N) operations
		#print('n is now: '+str(n))
		#append new marked numbers to marked_numbers	
		if n*p not in marked_nos:  			#This takes O(N) operations
			marked_nos.append(n*p)
			#marked_numbers.add(n*p) 
			#print('marked_numbers is now: '+str(marked_numbers))
		#increment n
		n=n+1			
	return marked_nos

	#===========================
	#--- TO DO --- ADD CHUNKING! - ie split marked_numbers into chunks of 1000 so not all memory is in use ----

	#number_chunks = int(math.ceil(N / 1000))
	#i=0			
	#for i in xrange(0,number_chunks)  
	#	chunk[i].append(marked_numbers(1:(1000-1)))
	#	i = i+1
			
	#=========================== 


def csvfile_create(data,filepath):
	#create csv file using data
	with open(filepath,'wb') as csvfile:
		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
		wr.writerow(data)		
		csvfile.close()	

if __name__=='__main__':
	main()

	#with open(primefile,'r') as csvfile:
			#primes_data=csvfile.read().replace('\n','').split(',')
			#primes_data=csvfile.read().replace('\n','')
		
			#check if last character in primes_data is a ','
			#print('Last character in primes_data is currently: '+str(primes_data[-1]))
		
			#if primes_data[-1]==',':
				#print('Last character in primes_data is currently: '+str(primes_data[-1]))
				#raw_input('Waiting for user..')
				#primes_data=primes_data[:-1]
				#primes_data=primes_data.rstrip('/')
				#print('Last character in primes_data is now: '+str(primes_data[-1]))
			#Now use .split() to store primes in elements  
			#primes_data_final=primes_data.split(',')
			#primes=primes_data_final
			#csvfile.close()

	#result=marked_numbers_update(p, N, marked_numbers)
	#print('marked_numbers is now: '+str(result[0]))

#segment_count_decimal = float(N) / segment_size
	#segment_count_decimal = float(N) % segment_size
	#print float(N) / segment_size
	#print float(N) % segment_size
	#print 'segment_count_decimal is: '+str(segment_count_decimal)
	#segment_count = int(math.ceil(float(N) / segment_size))
	#print 'segment_count is: '+str(segment_count)

	#Calculate N values in last segment 
	#difference = int(math.ceil(N - (segment_size_decimal * segment_count_decimal))) 
	#print 'Number of elements in last segment are: '+str(difference)

	#lastsegment_start ="" 
	#if difference <> 0:
		#Calculate i value last segment starts from
	#	lastsegment_start = N - difference
	#	print 'Last segment starts at: '+str(lastsegment_start)

	#set initial_segment
	#initial_segment_size = segment_size - 1

	#initialise S
	#S=[]

	#store S[0]
	#S[0]=N_range[0:initial_segment_size]
	#print "S[0] is: "+str(S[0])

	#print "N_range[0:10] is: "+str(N_range[0:10])
	#print "N_range[10:20] is: "+str(N_range[10:20])

	#Store segments in S except last segment
	#for i in xrange(0,segment_count-1):
	#	print "i is: "+str(i)		
	#	#S[i]=N_range[i:segment_size]
	#	start_range = i * segment_size #i=1, segment_size=10. Hence
	#	end_range = (i+1) * segment_size
	#	print "start_range is: "+str(start_range)
	#	#print "type of start_range is: "+str(type(start_range))
	#	print "end_range is: "+str(end_range)
	#	#print "type of end_range is: "+str(type(end_range))
	#	#print "(i*segment_size+1):() is: "+str(i*segment_size+1)+"):(("+str((i+1)*segment_size)
	#	#print "N_range[0:9] is: "+str(N_range[0:9])	
	#	#print "N_range[10:19] is: "+str(N_range[10:19])
	#	
	#	#========================================================
	#	
#
#		#Segment=N_range[start_range:end_range]
#		#S[i]=N_range[start_range:end_range]		
#		print "S["+str(i)+"] is: "+str(S[i])
#		#S[i]=N_range[(i*segment_size+1):((i+1)*segment_size)]
#		i=i+1
#		#========================================================
#		#S[0]=N_range[0:segment_size]
#		#S[1]=N_range[(1*segment_size+1):(2*segment_size)]
#		#S[2]=N_range[(2*segment_size+1):(3*segment_size)]
	
	#Store last segment
#	S[segment_count]=N_range[lastsegment_start:difference]
