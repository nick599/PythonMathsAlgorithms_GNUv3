#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 17/04/2018.
#Programmed & tested in Python 2.76 only
#This program works out the chinese remainder of two lists specified by user in ranges.
#It has been tested on Linux Mint v3.19 x64
#Testing results .... of xxx in xxx seconds.

import sys
import math
try:
	from math import gcd as bltin_gcd
except ImportError:
	from fractions import gcd
import os
import itertools
import csv
import time

print "Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3."
print "Version 1. 17/04/2018."
print "Programmed & tested in Python 2.76 only"
print "This program works out the chinese remainder of two lists specified by user in ranges."
print "It has been tested on Linux Mint v3.19 x64"
print "Testing results .... of xxx in xxx seconds."
print "---------------------------------------------------------------------"
	
def main():
	
	result = chinese_remainder(x, x_moduli)
	print "result is: "+str(result)
	
def chinese_remainder(x, x_moduli):
	print "Running chinese remainder("+str(x)+","+str(x_moduli)+").."	
	#print "x are: "+str(x)
	#print "x_moduli are: "+str(x_moduli)
	#cong=[]
	cong_x=[]
	cong_moduli=[]
	for number in xrange(0,len(x)):
		#print('--------------------')
		#print "number is: "+str(number)		
		#store values in 1st congruence	
		a= x[number]
		b= x_moduli[number]
		if b<>1:		
			if not cong_x:
				#cong has no elements
				#Add values in first congruence			
				#print "Appending info from 1st congruence"
				cong_x.append(a)
				x_new = a		
				cong_moduli.append(b)
				M = b			
				#cong.append(1)
			else:
				#print('--------------------')
				#cong_x has elements
				#print "Working on congruence number: "+str(number+1)
				#print "cong_x["+str(number-1)+"] is: "+str(cong_x[number-1])
				#print "cong_moduli["+str(number-1)+"] is: "+str(cong_moduli[number-1])
				#Subtract current cong_x[number-1] from current x[number]
				#print "Subtracting cong_x["+str(number-1)+"] from current x["+str(number)+"].."
				c = x[number] - cong_x[-1]
				#print "c now is: "+str(c)				#c=
			
				#print "cong_moduli["+str(number-1)+"] to use in inverse is: "+str(cong_moduli[number-1]) 
				#number=
				#print "x_moduli[number] to use in inverse is: "+str(b)			#moduli=

				#now want to find (cong_moduli[number-1]**-1) mod(b)		
				f = calc_modinverse(cong_moduli[-1], 1, b)
				#print "inverse (f) is: "+str(f) 			#inverse=

				#now take c and times it by the inverse, f, and reduce mod b
				#print "c*f is: "+str(c*f)
				#print "b is: "+str(b)
				k = (c*f) % b			
				#print "k is: "+str(k)

				#now take value of k and use it to work out new value of x
				#print "cong_x[-1] is: "+str(cong_x[-1])
				#print "cong_x[number-1] is: "+str(cong_x[number-1])
				#print "cong_moduli[-1] * k is: "+str((cong_moduli[-1] * k))
				#print "cong_moduli[number-1] * k is: "+str((cong_moduli[number-1] * k))
				x_new = cong_x[number-1] + (cong_moduli[number-1] * k)
				#print "x_new is: "+str(x_new)
				cong_x.append(x_new)
			
				#now work out value of M
				M = cong_moduli[-1] * b
				#print "M is now: "+str(M)
				cong_moduli.append(M)
	return x_new, M

def calc_modinverse(g, power, p):
	#print "----------------"
	#print "Running calc_modinverse().."					#O(1)
	#print "g is: "+str(g)
	#print "power is: "+str(power)
	#raw_input("Waiting for user..")	

	#print "p is: "+str(p) #p = 1 ?????

	floor_sqrt_p = math.floor(math.sqrt(p))					#O(2)

	#this only works for p being prime!	
	if isprime(p) == True:							#O(1)	#Subtotal O(2n+4)
		result = pow(g, (p-2), p)						#O(n+2)	#Subtotal O(2n+3)
		#print str(g)+"**(-1) mod "+str(p)+" is: "+str(result)
		c = pow(result, power, p)						#O(n+1)
		#print "c is: "+str(c)	
		#print str(g)+"**(-"+str(power)+") mod "+str(p)+" is: "+str(c)
	else:
		#p is not prime!
		#print "p: "+str(p)+" is not prime!"
		c = modinv(g, p)						#O(n)
		#return x % m
		#print "inverse is: "+str(c)		

		#raw_input("Waiting for user..")	
	return c

def isprime(p):		#this is O(sqrt(n))
	
	#print "Running isprime("+str(p)+").."
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	return True

def egcd(a, b):							#O(n)
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:						#O(1)	#Subtotal: O(2)
		return (b, 0, a)				#O(1)
	g, y, x = egcd(b % a, a)				
	#print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
	return (g, x - (b//a) * y, y)

def modinv(a, m):						#### O(n+5) ###
	#print("Running modinv("+str(a)+","+str(m)+")")		
	#print "a is: "+str(a)
	#print "m is: "+str(m)	
	#egcd(a, m)
	g, x, y = egcd(a, m)					#O(n)
	if g != 1:							#O(1)	#Subtotal: O(2)
		raise Exception('No Modular Inverse') 			#O(1)
	#print(str(a)+"**(-1) mod "+str(m)+" is: "+str(x % m))	
	return x % m						#O(1)

if __name__=='__main__':
	n = [3,5,7]
	a = [2,3,2]
	print chinese_remainder(n,a)
	#main()
