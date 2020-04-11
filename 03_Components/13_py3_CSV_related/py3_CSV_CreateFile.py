#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 06/05/2018.
#Programmed & tested in Python 3.4.3 only
#Prime list file should be a .CSV file with each prime separated by commas.
#Ensure that "prime_list_path" and "prime_list_filename" are edited for the location of prime list file used.

import sys
import math
import os
import itertools
import csv
import time

#python_version = sys.version

#print(python_version)

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version 1. 06/05/2018.")
print("Programmed & tested in python 3.4.3 only.")
print("---------------------------------------------------------------------")
#print("This program attemps to solve a Discrete Log Problem (DLP) specified by user, via Polig-Helman Algorithm via factorisation of (p-1) where p is a prime number")
#print("Results printed are three arrays ...")
print("Prime list file should be a .CSV file with each prime separated by commas.")
print("Ensure that \"prime_list_path\" and \"prime_list_filename\" are edited for the location of prime list file used.")
#print("The larger the prime file is that is used, the longer the factorisation will take!")
#print("It has been tested on Linux Mint v3.19 x64 using a prime list with primes upto 99,997")
print("---------------------------------------------------------------------")

def main():

	folder = "/home/mint/Desktop/"
	filename = "primes_upto_100000.csv"
	filepath = folder + filename
	print("file currently is:",filepath)

	csvfile_create(Primes_filepath)

def csvfile_create(data,filepath):
	#create csv file using data
	with open(filepath,'wb') as csvfile:
		wr = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_ALL)
		wr.writerow(data)		
		csvfile.close()	

if __name__=='__main__':
	main()

