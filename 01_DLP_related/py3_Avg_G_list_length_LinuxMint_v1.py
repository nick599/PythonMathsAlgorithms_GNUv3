#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 14/05/2018.
#Programmed & tested in Python 3.4.3 only
#This program prints the G_list for values of g and p chosen by user, where p is a prime number. 
#It has been tested on Linux Mint v3.19 x64.

import sys
import math
import os
#import itertools
#import csv
#import time

#python_version = sys.version

#print(python_version)

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version 1. 14/05/2018.")
print("Programmed & tested in python 3.4.3 only.")
print("This program prints the G_list for values of g and p chosen by user")
print("where p is a prime number.")
print("It has been tested on Linux Mint v3.19 x64")
print("---------------------------------------------------------------------")

version = 15

folder = "/home/mint/Desktop/"
output_filename = "output_Glist_v"+str(version)+".txt"
output_path = folder + output_filename
#print("output_path is:",output_path)

def main():
	
	print('What is g?')
	g_initial = input()
	if g_initial.isdigit() is False:
		print('You have not entered a positive integer for g. g is: '+str(g_initial)+'. Please reenter.')
		sys.exit()

	#now convert g into a long:
	g = int(g_initial)

	print('What is p?')
	p_initial = input()
	if p_initial.isdigit() is False:
		print('You have not entered a positive integer for p. p is: '+str(p_initial)+'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = int(p_initial)

	print("---------------------")
	print("g:",g,", p: ",p)

	data="Output\n------------\n"

	#print("data:",data)
	txtfile_create_new(data,output_path)

	data_for_append = []

	if g < p:
		if isprime(p) == True:
			#if g != p:				
			#Want to calculate and store group G				
			#print("Calculating G_list..")
			G_list = []				
			for number in range(1, p):
				a = pow(g,number,p)
				if a not in G_list:					
					G_list.append(a)
				else:
					break
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

