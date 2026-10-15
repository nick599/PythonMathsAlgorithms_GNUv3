#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 22/04/2018.
#Programmed & tested in Python 2.76 only
#This program checks the peak memory usage of a function.
#It has been tested on Linux Mint v3.19 x64.
#Using Lists instead of sets for storage to minimise memory usage

#import sys
#import math
#import csv
#import os.path

from memory_profiler import memory_usage ######### Needs memory profiler module #########
#from guppy import hpy
import factorial

print "Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3."
print "Version 1. 22/04/2018."
print "Programmed & tested in Python 2.76 only."
print "This program checks the peak memory usage of a function."
print "It has been tested on Linux Mint v3.19 x64."
print "Using Lists instead of sets for storage to minimise memory usage."
print "---------------------------------------------------------------------"

def main():
	test_range=xrange(1,1001)
	for num in test_range:
		factorial.factorial(num)
	
	######### Needs memory profiler #########	
	#mem_data = memory_usage(proc=factorial, timestamps=True, include_children=True, multiprocess=True)
	min_mem = min(memory_usage(proc=factorial))
	max_mem = max(memory_usage(proc=factorial))

	#print "mem_data is: "+str(mem_data)
	print "Minimum memory used: {0} MiB".format(str(min_mem))
	print "Maximum memory used: {0} MiB".format(str(max_mem))

if __name__=='__main__':
	main()
