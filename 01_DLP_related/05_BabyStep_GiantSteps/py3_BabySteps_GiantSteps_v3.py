#Source: http://stackoverflow.com/questions/1832617/calculate-discrete-logarithm/ 
#Code Licenced under GNU GPL v3.
#Version 3. 02/09/2019.
#Programmed & tested in Python 3.4.3 only
#This program tries to solve the DLP for a,b,p, and optional N. 
#It has been tested on Linux Mint v3.19 x64.

import sys
import math
import os
#import itertools
#import csv
#import time

print("Source: http://stackoverflow.com/questions/1832617/calculate-discrete-logarithm/")
print("Code Licenced under GNU GPL v3")
print("Version 3. 02/09/2019.")
print("Programmed & tested in python 3.4.3 only.")
print("This program tries to solve the DLP a**x = b mod p, for positive integers a & b, prime p, and optional N.")
print("It has been tested on Linux Mint v3.19 x64.")
print("---------------------------------------------------------------------")

version = 1

folder = "/home/mint/Desktop/"
#prime_filename = "primes_upto_10000.csv"
#primefile_path = folder + prime_filename
#print("primefile_path is:",primefile_path)

output_filename = "output_BabySteps_GiantSteps_v"+str(version)+".txt"
output_path = folder + output_filename
print("output_path is:",output_path)

def main():
	#a = 100001
	#b = 54696545758787
	#p = 70606432933607

	print('What is a?')
	a_initial = input()
	if a_initial.isdigit() is False:
		print('You have not entered a positive integer for a. a is: '+str(a_initial)+'. Please reenter.')
		sys.exit()

	#now convert a into a long:
	a = int(a_initial)

	print('What is b?')
	b_initial = input()
	if b_initial.isdigit() is False:
		print('You have not entered a positive integer for b. b is: '+str(b_initial)+'. Please reenter.')
		sys.exit()

	#now convert b into a long:
	b = int(b_initial)

	print('What is p?')
	p_initial = input()
	if p_initial.isdigit() is False:
		print('You have not entered a positive integer for p. p is: '+str(p_initial)+'. Please reenter.')
		sys.exit()

	#now convert p into a long:
	p = int(p_initial)

	data="a: "+str(a)+", b: "+str(b)+", p: "+str(p)+"\n"
	txtfile_create_new(data,output_path)
	data="Output\n------------\n"
	txtfile_append(data,output_path)
	data_for_print="a: "+str(a)+", b: "+str(b)+", p: "+str(p)
	print(data_for_print)	

	result = baby_steps_giant_steps(a,b,p)

	if pow(a,x,p) != b:
		print("CHECK ANSWER! - ",a,"**",x,"% ",p,"!=",b)

	data="Result: "+str(result)+"\n"
	txtfile_append(data,output_path)
	data_for_print="x: "+str(result)+", a: "+str(a)+", b: "+str(b)+", p: "+str(p)+", N: "+str(N)
	print(data_for_print)

def baby_steps_giant_steps(a,b,p,N = None):
	#Solving the DLP a**x = b mod p for x where p is prime, and a & b positive integers

    #a = 100001
	#b = 54696545758787
	#p = 70606432933607

	if not N:
		N = 1 + int(math.sqrt(p)) #N = order in F_p^*
		print("N calculated as:",N)
	else: 
		print("N supplied:",N)

	size_input_check(N)

	
	print("a:",a)
	print("b:",b)
	print("p:",p)

	#initialise baby_steps table	
	baby_steps = {}
	baby_step = 1

	print("==================================")
	for r in range(N+1):
		baby_steps[baby_step] = r
		old_baby_step = baby_step
		baby_step = baby_step * a % p		
		if r % 2000000 == 0:		
			print("baby_steps[current_baby_step]:",r,", old_baby_step: ",old_baby_step,", current_baby_step:",baby_step)

	print("==================================")
	#print("baby_steps:",baby_steps)

	#now take the giant steps
	giant_stride = pow(a,(p-2)*N,p) #only works when p is prime!
	giant_step = b
	print("giant_stride:",giant_stride,"giant_step_initial:",giant_step)
	print("==================================")
	for q in range(N+1):
		if giant_step in baby_steps:
			#print("q * N + baby_steps[giant_step]:",q * N + baby_steps[giant_step])
			return q * N + baby_steps[giant_step]
		else:
			giant_step = giant_step * giant_stride % p
			if q % 2000000 == 0:
				print("q:",q,", giant_step * giant_stride % p:",giant_step)
			
	return "No Match"

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
		print("Number attempted",input_number,"is too large for this program. Try a number <= 2x10^8. Exiting to avoid memory issues..")
		sys.exit()

if __name__=='__main__':
	result=baby_steps_giant_steps(100001,54696545758787,70606432933607)	
	data="x: "+str(result)+"\n"
	#txtfile_append(data,output_path)
	data_for_print="x: "+str(result)
	print(data_for_print)

