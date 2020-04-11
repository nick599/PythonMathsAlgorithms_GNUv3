#Copyright Nick Prowse 2017. Code Licenced under Apache 2.
#Version 4. 04/11/2017.
#Programmed & tested in Python 2.76 only
#This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive using sieve of eratosthenes - using a segmented sieve - with upper limit on segment size - L1D_CACHE_SIZE.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

import sys
import math
import csv
import os.path
import time
import itertools
import numpy as np

print("Copyright Nick Prowse 2017. Code Licenced under Apache 2.")
print("Version 4. 04/11/2017.")
print("Programmed & tested in Python 2.76 only.")
print("---------------------------------------------------------------------")
print("This program creates a prime list in CSV format with comma delimiter for all primes upto N inclusive using sieve of eratosthenes - using a segmented sieve - with upper limit on segment size - L1D_CACHE_SIZE.")
print("It has been tested on Linux Mint v3.19 x64.")
print("Using Lists instead of sets for storage to minimise memory usage.")
print("---------------------------------------------------------------------")

def main():
	#store size of L1 CPU cache in bytes
	L1D_CACHE_SIZE = 32768 #32*1024 = 32Kbytes	
	
	#Program creates primefile for N=100, 1000, and 10000 fine.
	#However for N = 100000, primefile output is:
#"2","983063","983069","983083","983113","983119","983123","983131","983141","983149","983153","983173","983179","983189","983197","983209","983233","983239","983243","983261","983267","983299","983317","983327","983329","983347","983363","983371","983377","983407","983429","983431","983441","983443","983447","983449","983461","983491","983513","983519","983527","983531","983533","983557","983579","983581","983597","983617","983659","983699","983701","983737","983771","983777","983783","983789","983791","983803","983809","983813","983819","983849","983861","983863","983881","983911","983923","983929","983951","983987","983993","984007","984017","984037","984047","984059","984083","984091","984119","984121","984127","984149","984167","984199","984211","984241","984253","984299","984301","984307","984323","984329","984337","984341","984349","984353","984359","984367","984383","984391","984397","984407","984413","984421","984427","984437","984457","984461","984481","984491","984497","984539","984541","984563","984583","984587","984593","984611","984617","984667","984689","984701","984703","984707","984733","984749","984757","984761","984817","984847","984853","984859","984877","984881","984911","984913","984917","984923","984931","984947","984959","985003","985007","985013","985027","985057","985063","985079","985097","985109","985121","985129","985151","985177","985181","985213","985219","985253","985277","985279","985291","985301","985307","985331","985339","985351","985379","985399","985403","985417","985433","985447","985451","985463","985471","985483","985487","985493","985499","985519","985529","985531","985547","985571","985597","985601","985613","985631","985639","985657","985667","985679","985703","985709","985723","985729","985741","985759","985781","985783","985799","985807","985819","985867","985871","985877","985903","985921","985937","985951","985969","985973","985979","985981","985991","985993","985997","986023","986047","986053","986071","986101","986113","986131","986137","986143","986147","986149","986177","986189","986191","986197","986207","986213","986239","986257","986267","986281","986287","986333","986339","986351","986369","986411","986417","986429","986437","986471","986477","986497","986507","986509","986519","986533","986543","986563","986567","986569","986581","986593","986597","986599","986617","986633","986641","986659","986693","986707","986717","986719","986729","986737","986749","986759","986767","986779","986801","986813","986819","986837","986849","986851","986857","986903","986927","986929","986933","986941","986959","986963","986981","986983","986989","987013","987023","987029","987043","987053","987061","987067","987079","987083","987089","987097","987101","987127","987143","987191","987193","987199","987209","987211","987227","987251","987293","987299","987313","987353","987361","987383","987391","987433","987457","987463","987473","987491","987509","987523","987533","987541","987559","987587","987593","987599","987607","987631","987659","987697","987713","987739","987793","987797","987803","987809","987821","987851","987869","987911","987913","987929","987941","987971","987979","987983","987991","987997","988007","988021","988033","988051","988061","988067","988069","988093","988109","988111","988129","988147","988157","988199","988213","988217","988219","988231","988237","988243","988271","988279","988297","988313","988319","988321","988343","988357","988367","988409","988417","988439","988453","988459","988483","988489","988501","988511","988541","988549","988571","988577","988579","988583","988591","988607","988643","988649","988651","988661","988681","988693","988711","988727","988733","988759","988763","988783","988789","988829","988837","988849","988859","988861","988877","988901","988909","988937","988951","988963","988979","989011","989029","989059","989071","989081","989099","989119","989123","989171","989173","989231","989239","989249","989251","989279","989293","989309","989321","989323","989327","989341","989347","989353","989377","989381","989411","989419","989423","989441","989467","989477","989479","989507","989533","989557","989561","989579","989581","989623","989629","989641","989647","989663","989671","989687","989719","989743","989749","989753","989761","989777","989783","989797","989803","989827","989831","989837","989839","989869","989873","989887","989909","989917","989921","989929","989939","989951","989959","989971","989977","989981","989999","990001","990013","990023","990037","990043","990053","990137","990151","990163","990169","990179","990181","990211","990239","990259","990277","990281","990287","990289","990293","990307","990313","990323","990329","990331","990349","990359","990361","990371","990377","990383","990389","990397","990463","990469","990487","990497","990503","990511","990523","990529","990547","990559","990589","990593","990599","990631","990637","990643","990673","990707","990719","990733","990761","990767","990797","990799","990809","990841","990851","990881","990887","990889","990893","990917","990923","990953","990961","990967","990973","990989","991009","991027","991031","991037","991043","991057","991063","991069","991073","991079","991091","991127","991129","991147","991171","991181","991187","991201","991217","991223","991229","991261","991273","991313","991327","991343","991357","991381","991387","991409","991427","991429","991447","991453","991483","991493","991499","991511","991531","991541","991547","991567","991579","991603","991607","991619","991621","991633","991643","991651","991663","991693","991703","991717","991723","991733","991741","991751","991777","991811","991817","991867","991871","991873","991883","991889","991901","991909","991927","991931","991943","991951","991957","991961","991973","991979","991981","991987","991999","992011","992021","992023","992051","992087","992111","992113","992129","992141","992153","992179","992183","992219","992231","992249","992263","992267","992269","992281","992309","992317","992357","992359","992363","992371","992393","992417","992429","992437","992441","992449","992461","992513","992521","992539","992549","992561","992591","992603","992609","992623","992633","992659","992689","992701","992707","992723","992737","992777","992801","992809","992819","992843","992857","992861","992863","992867","992891","992903","992917","992923","992941","992947","992963","992983","993001","993011","993037","993049","993053","993079","993103","993107","993121","993137","993169","993197","993199","993203","993211","993217","993233","993241","993247","993253","993269","993283","993287","993319","993323","993341","993367","993397","993401","993407","993431","993437","993451","993467","993479","993481","993493","993527","993541","993557","993589","993611","993617","993647","993679","993683","993689","993703","993763","993779","993781","993793","993821","993823","993827","993841","993851","993869","993887","993893","993907","993913","993919","993943","993961","993977","993983","993997","994013","994027","994039","994051","994067","994069","994073","994087","994093","994141","994163","994181","994183","994193","994199","994229","994237","994241","994247","994249","994271","994297","994303","994307","994309","994319","994321","994337","994339","994363","994369","994391","994393","994417","994447","994453","994457","994471","994489","994501","994549","994559","994561","994571","994579","994583","994603","994621","994657","994663","994667","994691","994699","994709","994711","994717","994723","994751","994769","994793","994811","994813","994817","994831","994837","994853","994867","994871","994879","994901","994907","994913","994927","994933","994949","994963","994991","994997","995009","995023","995051","995053","995081","995117","995119","995147","995167","995173","995219","995227","995237","995243","995273","995303","995327","995329","995339","995341","995347","995363","995369","995377","995381","995387","995399","995431","995443","995447","995461","995471","995513","995531","995539","995549","995551","995567","995573","995587","995591","995593","995611","995623","995641","995651","995663","995669","995677","995699","995713","995719","995737","995747","995783","995791","995801","995833","995881","995887","995903","995909","995927","995941","995957","995959","995983","995987","995989","996001","996011","996019","996049","996067","996103","996109","996119","996143","996157","996161","996167","996169","996173","996187","996197","996209","996211","996253","996257","996263","996271","996293","996301","996311","996323","996329","996361","996367","996403","996407","996409","996431","996461","996487","996511","996529","996539","996551","996563","996571","996599","996601","996617","996629","996631","996637","996647","996649","996689","996703","996739","996763","996781","996803","996811","996841","996847","996857","996859","996871","996881","996883","996887","996899","996953","996967","996973","996979","997001","997013","997019","997021","997037","997043","997057","997069","997081","997091","997097","997099","997103","997109","997111","997121","997123","997141","997147","997151","997153","997163","997201","997207","997219","997247","997259","997267","997273","997279","997307","997309","997319","997327","997333","997343","997357","997369","997379","997391","997427","997433","997439","997453","997463","997511","997541","997547","997553","997573","997583","997589","997597","997609","997627","997637","997649","997651","997663","997681","997693","997699","997727","997739","997741","997751","997769","997783","997793","997807","997811","997813","997877","997879","997889","997891","997897","997933","997949","997961","997963","997973","997991","998009","998017","998027","998029","998069","998071","998077","998083","998111","998117","998147","998161","998167","998197","998201","998213","998219","998237","998243","998273","998281","998287","998311","998329","998353","998377","998381","998399","998411","998419","998423","998429","998443","998471","998497","998513","998527","998537","998539","998551","998561","998617","998623","998629","998633","998651","998653","998681","998687","998689","998717","998737","998743","998749","998759","998779","998813","998819","998831","998839","998843","998857","998861","998897","998909","998917","998927","998941","998947","998951","998957","998969","998983","998989","999007","999023","999029","999043","999049","999067","999083","999091","999101","999133","999149","999169","999181","999199","999217","999221","999233","999239","999269","999287","999307","999329","999331","999359","999371","999377","999389","999431","999433","999437","999451","999491","999499","999521","999529","999541","999553","999563","999599","999611","999613","999623","999631","999653","999667","999671","999683","999721","999727","999749","999763","999769","999773","999809","999853","999863","999883","999907","999917","999931","999953","999959","999961","999979","999983"


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

	#Store square root of N rounded to integer
	sqrt_N = int(math.sqrt(N))

	#Set segment_size to be max of CPU's L1 data cache size and sqrt_N
	#segment_size = math.max(L1D_CACHE_SIZE,sqrt_N)
	print('Calculating segment_size ..')
	segment_size = max(L1D_CACHE_SIZE,sqrt_N)

	#limit = N

	print('Running sieve ..')
	#primes = sieving(sqrt_N, segment_size, N)
	result = sieving(sqrt_N, segment_size, N)
	primes = result[0]
	next_mem_usage = result[1]
	sieve_mem_usage = result[2]
	primes_mem_usage = result[3]
	final_mem_usage = result[4]
	isprime_mem_usage = result[5]

	prime_list_path="/home/mint/Desktop/"
	prime_list_filename='primes_upto_'+str(N)+'.csv'
	primefile=prime_list_path + prime_list_filename
	
	print('Running checks on primefile ..')
	#Check if primefile already exists.
	if os.path.exists(primefile) is False: 
		print('Now creating file for primes in prime list upto '+str(N))
		csvfile_create(primes,primefile)
	else:
		print('Prime file already exists in that location. Existing prime file will be deleted before new one is created.')
		os.remove(primefile)
		csvfile_create(primes,primefile)
		print('Prime list for primes upto '+str(N)+' created.')

	print('Creating primefile ..')
	csvfile_create(primes,primefile)

	print'End memory used by is_prime list: '+str(isprime_mem_usage)
	print'End memory used by next list: '+str(next_mem_usage)
	print'End memory used by sieve list: '+str(sieve_mem_usage)
	print'End memory used by primes list: '+str(primes_mem_usage)
	print'End memory used by final_list: '+str(final_mem_usage)


def sieving(sqrt_N, segment_size, limit):
	#1) Then start crossing off the multiples of first prime 2 until we reach a multiple of 2 = m >= segment_size. 
	#2) when m >= segment_size, calculate index of that multiple in the segment using (m - segment_size), and store in a list
	#Repeat process 1) and 2) crossing off multiples of the next sieving primes using same process.
	#Once all multiples of the sieving primes have been crossed off in first segment, iterate over the sieve list and print out / count primes
	#in order to sieve the next segment sieve array is reset, and increment the lower offset by segment_size.
	#then start crossing-off multiples again, for each sieving prime retrieve the sieve index from list, and start crossing off multiples from there on.

	if limit < 2:
		count=0
	else:
		count=1

	s = 3
	n = 3

	#Now need to generate sieving primes less than sqrt_N - which are needed to cross off multiples
	#is_prime="" #This needs to be a vector of size sqrt_N + 1, with elements 1.
	is_prime = [1] * (sqrt_N + 1) #sqrt_N + 1 = 101
	#vector <char> is_prime[sqrt_N + 1,1]
	
	print'Running is_prime[] ..'
	i = 2
	while i * i <= sqrt_N: #N=10000. Hence sqrt_N=100. 1st loop i=2 hence i*i=4. 4 <= 100
		#print('i is: '+str(i))		
		if is_prime[i]: #is_prime[2] = 1
			j = i * i	#j = i*i = 4		
			while j <= sqrt_N: #j = 4	<= 100
				#for j in xrange(len(is_prime)): #len(is_prime) = 101 								
					#item =	is_prime[j]				
				is_prime[j] = 0
					#is_prime(j) = 0			
				#is_prime.append(0)
				j = j + i
		i = i + 1

	isprime_mem_usage = sys.getsizeof(is_prime)
	#print'Total memory used in is_prime[]: '+str(isprime_mem_usage)+' bytes.'

	#
	print'Initialising lists and values ..'
	sieve=[]
	primes = []
	next = []
	low = 0	
	print'Sieving ..'
	while low <= limit:
		#Populate sieve 
		#print('---------------------')
		#print('low is: '+str(low))		
		#print('limit is: '+str(limit))
		#print('low + segment_size + 1 is: '+str(low + segment_size + 1))
		sieve = list(xrange(low,low + segment_size + 1))
		
		#current segment = interval[low, high]
		#high = math.min(low + segment_size - 1, limit)
		high = min(low + segment_size - 1, limit)

		#add new sieving primes <= sqrt(high)
		while s * s < high:
			if is_prime[s]:
				primes.append(s)
				next.append(s * s - low)
			s = s + 2

		#sieve the current segment
		i=0		
		primes_size = len(primes)
		#primes_size = primes.size()		
		while i < primes_size:
			#print('i is: '+str(i))	
			j = next[i]
			#print('j = next['+str(i)+'] is: '+str(j))
			k = primes[i] * 2
			while j < segment_size:		
				#sieve[j]=0 -- want j'th element in sieve list to be 0 !!
				#for j in xrange(len(sieve)):
				sieve[j] = 0
					#sieve(j) = 0
				#sieve.append(0)
				j = j + k
			#next[i]= (j - segment size)  -- want i'th element in next list to be (j - segment_size) ! 
			#print('j is: '+str(j))
			#print('j - segment_size is: '+str(j - segment_size))	
			next[i]= j - segment_size
			i = i + 1 

		final_list=[2]
		while n <= high:
			if (sieve[n - low]): #n is a prime
				final_list.append(n)				
				count = count + 1
			n = n + 2

		low = low + segment_size
	
	next_mem_usage = sys.getsizeof(next)
	sieve_mem_usage = sys.getsizeof(sieve)
	primes_mem_usage = sys.getsizeof(primes)
	final_list_mem_usage = sys.getsizeof(final_list)
	print'Total memory used in sieve[]: '+str(sieve_mem_usage)+' bytes.'

	return final_list, next_mem_usage, sieve_mem_usage, primes_mem_usage, final_list_mem_usage, isprime_mem_usage


#	print('Now creating list of segments, sized <= square root of '+str(N))
#	s_evalsegments = time.clock()
#	segments=create_segments(N)
#	c_evalsegments = time.clock() - s_evalsegments
#	#print(segments)
#
#	#raw_input('Waiting for user..')
#
#	# Eval even integers ###################################################
#	#N=10000	
#	#100 segments of size 100 for N=10000
#	marked_nos=[]
#	print('Now populating marked_numbers with even numbers <= '+str(N))
#	s_evalevens = time.clock()	
#	for segment in segments:	
#		#There are math.ceil(math.sqrt(N)) segments				
#		#-- O(N) since 'x in s' and segments is a list'
#		#print'-----------------------------------'
#		#print'Segment is: '+str(segment)
#		#print'Segment[0] is: '+str(segment[0])
#		#print'Segment[1] is: '+str(segment[1])
#		#100 elements in each segment for N=10000 		
#		for element in segment:	
#		#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
#		#-- O(N) since 'x in s' and segments is a list'
#			#print'element is: '+str(element)
#			if (element == 2 or element == 3):
#				continue				
#				#primes.append(element)
#			else:
#				marked_nos = even_integers(element)
#	c_evalevens = time.clock() - s_evalevens
#
#	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)
#	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))
#
#	# Eval odd integers ###################################################
#	print('Now creating list of odd integers <= '+str(N))
#	#N=10000	
#	#100 segments of size 100 for N=10000
#	s_evalodds = time.clock()	
#	#There are math.ceil(math.sqrt(N)) segments 
#	#O(N) since 'x in s' and segments is a list'	
#	for segment in segments:	
#		#print'-----------------------------------'
#		#print'Segment is: '+str(segment)
#		#print'Segment[0] is: '+str(segment[0])
#		#print'Segment[1] is: '+str(segment[1])
#		#100 elements in each segment for N=10000 		
#		if (segment[0] == 2 and segment[1] == 3):
#			continue				
#				#primes.append(element)
#		else:
#			for element in segment:	
#			#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
#			#O(N) since 'x in s' and segments is a list'
#				#print'element is: '+str(element)
#			#if (element == 2 or element == 3):
#			#	continue				
#			#	#primes.append(element)
#			#else:
#				result1 = odd_integers(element)
#				odd_ints = result1[0]
#				c_oddintegers = result1[1]
#	c_evalodds = time.clock() - s_evalodds
#
#	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)+sys.getsizeof(odd_ints)
#	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))
#
#	# Eval marked numbers ###################################################
#	print('Now updating list of marked numbers <= '+str(N))
#	#N=10000	
#	#primes=[]
#	#100 segments of size 100 for N=10000
#	s_evalmarkednos = time.clock()	
#	for segment in segments:	
#		#There are math.ceil(math.sqrt(N)) segments 			#O(N) since 'x in s' and segments is a list'
#		#print'-----------------------------------'
#		#print'Segment is: '+str(segment)
#		#print'Segment[0] is: '+str(segment[0])
#		#print'Segment[1] is: '+str(segment[1])
#		#if (segment[0] == 2 or segment[1] == 3):
#		#	continue		
#		#	#primes.append(element)
#		#else:
#		#100 elements in each segment for N=10000 		
#		for element in segment:	
#			#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
#			#O(N) since 'x in s' and segments is a list'
#			#print'element is: '+str(element)
#			#if (element == 2 or element == 3):
#			#	continue		
#			#	#primes.append(element)
#			#else:
#			result2 = marked_numbers(marked_nos,odd_ints,element)
#			marked_nos = result2[0]
#			c_markednumbers = result2[1]
#	c_evalmarkednos = time.clock()- s_evalmarkednos	
#
#	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)+sys.getsizeof(odd_ints)
#	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))
#
#	# Eval Primes ###################################################
#	#N=10000	
#	primes=[]
#	#100 segments of size 100 for N=10000
#	print('Now creating list of primes <= '+str(N))
#	s_evalprimes=time.clock()	
#	for segment in segments:	
#		#There are math.ceil(math.sqrt(N)) segments 
#		#O(N) since 'x in s' and segments is a list'
#		#print'-----------------------------------'
#		#print'Segment is: '+str(segment)
#		#100 elements in each segment for N=10000 		
#		if (segment[0] == 2 or segment[1] == 3):
#			primes.append(element)
#		else:
#			for element in segment:	
#		#There are math.ceil(math.sqrt(N)) elements in each segment apart from the last segment		
#		#O(N) since 'x in s' and segments is a list'
#			#print'element is: '+str(element)
#			#if (element == 2 or element == 3):
#			#	primes.append(element)
#			#else:
#				result3 = primes_list(marked_nos, primes, odd_ints, element)
#				primes = result3[0]
#				c_primes = result3[1]
#	c_evalprimes = time.clock()- s_evalprimes
#
#	total_memory_used_inlists = sys.getsizeof(segments)+sys.getsizeof(marked_nos)+sys.getsizeof(odd_ints)+sys.getsizeof(primes)
#	print'Total memory used in lists: '+str(sys.getsizeof(total_memory_used_inlists))
#
#	# Now free memory in segments list
#	print('Resetting segments ..')
#	segments=""
#
#	# Now free memory in odd integers
#	print('Resetting odd_ints..')
#	odd_ints=""
#
#	# Now free memory in marked numbers
#	print('Resetting marked_nos..')
#	marked_nos=""
#
#	prime_list_path="/home/mint/Desktop/"
#	prime_list_filename='primes_upto_'+str(N)+'.csv'
#	primefile=prime_list_path + prime_list_filename
#	
#	#Check if primefile already exists.
#	if os.path.exists(primefile) is False: 
#		print('Now creating file for primes in prime list upto '+str(N))
#		csvfile_create(primes,primefile)
#	else:
#		print('Prime file already exists in that location. Existing prime file will be deleted before new one is created.')
#		os.remove(primefile)
#		csvfile_create(primes,primefile)
#		print('Prime list for primes upto '+str(N)+' created.')
#	
#	# Now free memory in primes list
#	print('Resetting primes list ..')
#	primes=""
#
#	#print'Even integers are now: '+str(marked_nos)
#	print'Odd integers are now: '+str(odd_ints)
#	print'Marked numbers are now: '+str(marked_nos)
#	print'Primes are now: '+str(primes)
#
#	print 'Time to evaluate segments: '+str(c_evalsegments)
#	print 'Time to create odd integers list: '+str(c_oddintegers) 
#	print 'Time to create marked numbers list: '+str(c_markednumbers)
#	print 'Time to create prime list: '+str(c_primes)
#
#	print'End memory used by segments: '+str(sys.getsizeof(segments))
#	#print'Memory used by even integers: '+str(sys.getsizeof(marked_nos))
#	print'End memory used by odd integers: '+str(sys.getsizeof(odd_ints))
#	print'End Memory used by marked numbers: '+str(sys.getsizeof(marked_nos))
#	print'End Memory used by primes: '+str(sys.getsizeof(primes))


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
