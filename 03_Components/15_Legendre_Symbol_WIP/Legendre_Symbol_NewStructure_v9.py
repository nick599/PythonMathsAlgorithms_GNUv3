print("Legendre_Symbol_factorisations_v7.py")
print("Copyright Nick Prowse 2026. Code Licenced under GNU GPL v3.")
print("Version 8. 12/10/2026.")
print("Programmed & tested in Python 3 only")
print("This program works out the Legendre Symbol of two numbers g & p specified by user.")
print("It has been tested on Windows 11 Home x64")
print("Testing results .... of xxx in xxx seconds.")
print("---------------------------------------------------------------------")

#Copyright Nick Prowse 2026. Code Licenced under GNU GPL v3.
#Version 8. 12/10/2026.
#Programmed & tested in Python 3 only
#This program works out the Legendre Symbol of two numbers g & p specified by user.
#It has been tested on Windows 11 Home x64
#Testing results .... of xxx in xxx seconds.

#py3 files with factorisation algorithms
import sys
import os
import math
try:
	from pathlib import Path
except:
	import path
import itertools
import csv
import time

# Add the absolute path of the target folder(s) to Python's search path
factorise_folder_path = os.path.abspath('/03_Components/01_Factorising')

# 1. Get the path to the current directory (current_folder)
Current_dir = os.path.dirname(os.path.abspath(__file__))
print("Current_dir:",Current_dir)

# 2. Navigate up to the parent directory (parent_folder)
Parent_dir = os.path.dirname(Current_dir)
print("Parent_dir:",Parent_dir)
Parent_dir = Path(Parent_dir)

Parent_2up_dir = os.path.dirname(Parent_dir)
print("Parent_2up_dir:",Parent_2up_dir)
Parent_2up_dir = Path(Parent_2up_dir)

# 3. Construct the absolute path to subdirectories
Factorising_dir = Parent_dir / "01_Factorising"
print("Factorising_dir:",Factorising_dir)

PrimalityTesting_dir = Parent_2up_dir / "05_PrimalityTesting"
print("PrimalityTesting_dir:",PrimalityTesting_dir)

# 4. Append them to sys.path so Python can see it
sys.path.append(str(Factorising_dir))
sys.path.append(str(PrimalityTesting_dir))

# 5. Import the file (without the .py extension)
#py3 files with factorisation algorithms
import w235_primefactors_powers_v5
#import w235_primefactors_no_powers_v5
import Diff_of_Squares_v12_OnHold

#Remainder TO DO!
#import TrialDivision ###
#import Pollards_rho
#import Pollards_p_minus_1
#import Williams_p_plus_1
#import ECM
#import SIQS
#import MPQS
#import GNFS

#Primality testing
import isprime_trialdivision_v3
#import AKS_primality_test_v12_Win11
	
def main(g, p):
	
	result = leg_s_g_p_new(g, p)

	print("legendre_symbol_g_p is:",str(result))
	
def leg_s_g_p_new(g,p):

	print('Running leg_s_g_p_new(',g,',',p,')...')

	#outputs the legendre symbol (g over p) for inputs g and p 
	#legendre_g_p(g over p) == -1 when g is a quadratic residue mod p and g % p !=0 
	#legendre_g_p(g over p) == 1 when g is a non-quadratic residue mod p
	#legendre_g_p(g over p) == 0 when g % p = 0

	#power=int((p-1)/2)
	#print('power:',power)

	#legendre_symbol_g_p=pow(g,power,p)

	a = 0

	while g != 1 and g != -1 and g != 0: 

		print("~~~~~~~~~~~~~~~~~~~~~~~")
		a = a + 1 
		print("g is now:",g)
		print("p is now:",p)
		print("number of loops:",a)

		#Check if p and g are prime

		if p > 0:
			result_p = isprime(p)
		elif p < 0: 
			result_p = isprime(-p)
		
		if g > 0:
			result_g = isprime(g)
		elif g < 0:
			result_g = isprime(-g)		

		if result_p == False:
			print("p:",p,"is not prime! Legendre symbol undefined!")
			break
		elif g == 1:
			print("g = 1")
			legendre_symbol_g_p = 1
			g = 1
		elif g % p == 0:
			print("g % p == 0")
			legendre_symbol_g_p = 0
			g = 0
		elif g == -1:
			print("g == -1")
			if p % 4 == 1:
				print("g=-1 and p mod 4 = 1")			
				legendre_symbol_g_p = 1
				g = 1
			elif p % 4 == 3:
				print("g=-1 and p mod 4 = 3")
				legendre_symbol_g_p = -1
				g = -1			
		elif g == 2:
			print("g == 2")
			if p % 8 == 1 or p % 8 == -1:
				print("g=2 and p mod 8 = +-1")
				legendre_symbol_g_p = 1
				g = 1
			elif p % 8 == 3 or p % 8 == -3:
				print("g=2 and p mod 8 = +-3")
				legendre_symbol_g_p = -1
				g = -1
			else:
				print("g = 2 and ",p,"mod 8 not 1, -1, 3, or -3")
				legendre_symbol_g_p = (-1)**((p**2-1)/8)
				g = legendre_symbol_g_p

		elif g == 3 and p != 3:
			if p % 12 == 1 or p % 12 == 11:
				print("g = 3 and",p,"mod 12 = 1 or 11")
				legendre_symbol_g_p = 1
				g = 1
			elif p % 12 == 5 or p % 12 == 7:
				print("g = 3 and ",p,"mod 12 = 5 or 7")
				legendre_symbol_g_p = -1
				g = -1
			else:
				print("g = 3 and ",p,"mod 12 not 5 or 7")
				legendre_symbol_g_p = (-1)**math.floor((p+1)/6)
				g = legendre_symbol_g_p
		elif g==5:
			if p % 5 == 1 or p % 5 == 4:
				print("g = 5 and",p,"mod 5 = 1 or 11")
				legendre_symbol_g_p = 1
			elif p % 5 == 2 or p % 5 == 3:
				print("g = 5 and ",p,"mod 5 = 2 or 3")
				legendre_symbol_g_p = -1
				g = -1
		elif g > p:
			print("g > p")
			g = g % p
			print("revised g:",g)

		elif abs(g) > p and g < 0:
			print("abs(g) > p and g < 0")
			g = -(-g % p)
			print("revised g:",g)

		elif abs(g) < p and g < 0:
			print("abs(g) < p and g < 0")
			g = g + p
			print("revised g:",g)

		#Check for g being square number
		elif isSquare(g) == True:
			result_sqr = math.sqrt(g) % p
			if result_sqr != 0:
				print("g:",g,"is square and p does not divide sqrt(",g,")")
				legendre_symbol_g_p = 1
				g = 1
			if result_sqr == 0:
				print("g:",g,"is square and p divides sqrt(",g,")")
				legendre_symbol_g_p = 0
				g = 0
		
		#Check for factors of 2
		elif g % 2 == 0:
			#2 is a factor
			print("2 is a factor of g:",g)
								
			i = 2
			remainder = int(g / 2)
			print("remainder is:",remainder)
			power = 1
			#divisible by a factor of 2
				
			while remainder % 2 == 0:
				remainder = remainder / 2	
				power = power + 1
			
			print("power of 2 is:",power)

			if power >= 2:
				#divisible by a square of 2
				g = g % 4
				print("revised g:",g)
				
				input("TO DO - divisible by a square of 2 - waiting for user")

				#print("1 --- Legendre_symbol evaluated for:",g,"as:",leg_symbol[2])
				#break
			elif power == 1:
				#Only has one factor of 2
				if p % 8 == 1 or p % 8 == -1:
					print("g=2 and p mod 8 = +-1")
					legendre_symbol_g_p = 1
					g = 1
				elif p % 8 == 3 or p % 8 == -3:
					print("g=2 and p mod 8 = +-3")
					legendre_symbol_g_p = -1
					g = -1
				else:
					print("g = 2 and ",p,"mod 8 not 1, -1, 3, or -3")
					legendre_symbol_g_p = (-1)**((p**2-1)/8)
					g = legendre_symbol_g_p
				
				#input("TO DO - only has one factor of 2 - waiting for user")

		#Check for factors of 3
		elif g % 3 == 0:
			#3 is a factor
			print("3 is a factor of g:",g)
			
			if g == 3:
				print("g = 3")
				if p != 3:
					print("g = 3 and p != 3")
					#Check mod 12 rules
					if p % 12 == 5 or p % 12 == 7:
						print("Using mod 12 rule")
						g = -1
						legendre_symbol_g_p = 1

					elif p % 12 == 1 or p % 12 == 11:
						print("Using mod 12 rule")
						g = 1
						legendre_symbol_g_p = 1
					else:
						legendre_symbol_g_p = (-1)**math.floor((p+1)/6)

			elif g > 3:
				remainder = int(g / 3)
				print("remainder is:",remainder)
				power = 1
				#divisible by a factor of 3
				
				while remainder % 3 == 0:
					remainder = remainder / 3		
					power = power + 1

				print("power is:",power)

				if power == 1:
					print("divisible by a factor of 3 once")
					#power is 1
					if p != 3:
						#Check mod 12 rules
						print("g = 3 and p != 3. Check mod 12 rules")
						if p % 12 == 5 or p % 12 == 7:
							#print("Using mod 12 rule")
							g = -remainder
							legendre_symbol_g_p = -remainder

						elif p % 12 == 1 or p % 12 == 11:
							#print("Using mod 12 rule")
							g = remainder
							legendre_symbol_g_p = remainder
						else:
							legendre_symbol_g_p = (-1)**math.floor((p+1)/6)

					print("legendre_symbol_g_p:",legendre_symbol_g_p)
					#input("Waiting for user - TO DO")


				elif power % 2 == 0:
					#power is even
					print("divisible by a factor of 3 multiple times")
					#Check if p divides 3**power
					if pow(3,power,p) == 0:
						#p divides 3**power
						print("p divides 3**power")
						#numerator of legendre symbol becomes 0
						legendre_symbol_g_p = 0

					else:
						#p does not divide 3**power
						print("p does not divide 3**power")
						#numerator of legendre symbol is divided by 3**power 
						g = g / 3**power
						print("revised g:",g)

				elif power % 2 == 1:
					#power is odd and not 1, ie power >= 3
					print("Reducing g:",g,"by",int(3**(power-1)))
					g = int(g / 3**(power-1))
					print("revised g:",g)

					#input("Waiting for user - TO DO")
	
				#print("revised g:",g)
				#print("1 --- Legendre_symbol evaluated for g as:",g)
				#break

		#Check for factors of 5
		elif g % 5 == 0:
			#5 is a factor
			print("5 is a factor of g:",g)
			
			if g == 5:
				if p != 5:
					#Check mod 5 rules
					if p % 5 == 1 or p % 5 == 4:
						print("revised g:",g,"using mod 5 rule")
						g = 1
					elif p % 5 == 2 or p % 5 == 3:
						print("revised g:",g,"using mod 5 rule")
						g = -1

			elif g > 5:
				temp = g
				power = 1
				#divisible by a factor of 5
				while temp % 5 == 0 and temp > 1:
					temp //= 5				
					power += 1

				print("power is:",power)

				print("revised g:",g)
				input("TO DO - waiting for user")

				if power == 1:
					#Only has one factor of 5
					input("TO DO - only has one factor of 5 - waiting for user")


				elif power % 2 == 0:
					#power is even
					print("divisible by a factor of 5 multiple times")
					#Check if p divides 5**power
					if pow(5,power,p) == 0:
						#p divides 5**power
						print("p divides 5**power")
						#numerator of legendre symbol becomes 0
						legendre_symbol_g_p = 0

					else:
						#p does not divide 5**power
						print("p does not divide 5**power")
						#numerator of legendre symbol is divided by 5**power 
						g = g / 5**power
						print("revised g:",g)

				elif power % 2 == 1:
					#power is odd
					input("Waiting for user - TO DO")

				input("TO DO - waiting for user")

		#2, 3 and 5 are not factors of g and g is not square
		#check for g & p being distinct primes and g > 2
		elif result_g and result_p and g > 2:
			print("g, p are prime and g > 2. Use quadratic reprocity law")
			#quadratic reprocity law
			power_n = ((g-1)/2)*((p-1)/2) 
			numerator = (-1)**(power_n)

			if numerator == 1:
				temp = g
				g = p
				p = temp
			elif numerator == -1:
				temp = g
				g = -p
				p = temp
			
			print("revised g:",g)
			print("revised p:",p)

			#print("1 ~~~ Revised legendre_symbol after mod 4 rule:",leg_symbol)

		#2, 3 and 5 are not factors of g, g is not square, and quadratic reprocity rule doesn't apply
		#factorise g
		else:
			if g > 0:
				print("2, 3 and 5 are not factors of:",g,". g:",g," is not square, and quadratic reprocity rule doesn't apply")
			
				print("Running factorise_powers(",g,")")
				result = factorise_powers(g)
			elif g < 0:
				print("2, 3 and 5 are not factors of:",-g,". g:",-g," is not square, and quadratic reprocity rule doesn't apply")
				print("Running factorise_powers(",-g,")")
				result = factorise_powers(-g)

			#return prime_factors, powers, round(c_calc_primefactors,8), round(c_calc_powers,8), round(total_calc_time,8)
			prime_factors=result[0]
			powers=result[1]
			print("prime_factors:",prime_factors,"powers:",powers)

			powers_new=[]
			for power in powers:
				if power >=2:
					powers_new.append(power % 2)
				else:
					powers_new.append(power)

			print("powers mod 2:",powers_new)

			leg_symbols=[]
			c=0
			for power in powers_new:
				leg_temp=[]
				if power==1:
					#print("c:",c)
					#print("power:",power)
					#factor_temp=prime_factors[c]
					#print("factor_temp:",factor_temp)		
					leg_temp.append(prime_factors[c])
					leg_temp.append(p)
					leg_temp.append(0) #placeholder for evaluated leg_symbol
					leg_symbols.append(leg_temp)
				c=c+1

			print("subsidary legendre_symbols to calculate:",leg_symbols)
		
			#check if 2 is numerator in any legendre symbol
			#if yes calc (2/p) legendre symbol
			if leg_symbols[0][0] == 2:
				if p % 8 == 1 or p % 8 == -1:
					print("g=2 and p mod 8 = +-1")
					leg_symbols[0][2]=1
				elif p % 8 == 3 or p % 8 == -3:
					print("g=2 and p mod 8 = +-3")
					leg_symbols[0][2]=-1
				print("Revised legendre_symbols to calculate after consideration of first subsidary:",leg_symbols)

			#now evaluate each subsidary leg_symbol
			for leg_symbol in leg_symbols:
				eval=False
				if leg_symbol[2]!=0:
					print("leg_symbol[2]!=0")
					eval=True
					break
				elif leg_symbol[2]==0:
					leg_symbol, eval = subs_legendre_symbol(leg_symbol,eval)


			#loop through all subsidary leg_symbols and calculate final legendre symbol
			print("-------------------------------------------")
			legendre_symbol_g_p=1
			for leg_symbol in leg_symbols:
				legendre_symbol_g_p=legendre_symbol_g_p * leg_symbol[2]

			print("legendre_symbol_g_p after product:",legendre_symbol_g_p)

	if g == 1 or g == -1 or g == 0:
		return g
	else:
		return g,p

def subs_legendre_symbol(leg_symbol,eval):
				print("-------------------------------------------")
				print("Working on subsidary legendre_symbol:",leg_symbol)
				a=0
				while eval==False:				
					a=a+1
					print("a:",a)
					if not (leg_symbol[0] == -1 or leg_symbol[0] == 1 or leg_symbol[0] == 0):
						print("leg_symbol[0] now:",leg_symbol[0])
						if leg_symbol[1] >=2:
							#Check for factors of 2
							if leg_symbol[1] % 2 == 0:
								#2 is a factor
								print("2 is a factor of leg_symbol[1]")
								
								i = 2
								power = 1
								while i*i < leg_symbol[1]:
									power = power + 1
								print("power of 2 is:",power)

								if power % 2 == 0:
									#divisible by a square of 2
									if 2 % leg_symbol[1] == 0:
										leg_symbol[2] = 1
										print("1 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
										eval=True
										break
								elif power % 2 == 1:
									#not divisible by a square of 2
									input("TO DO not divisible by a square of 2 - waiting for user")

							#2 is a not a factor of leg_symbol[1]
							#Check if leg_symbol[1] is a square number
							if isSquare(leg_symbol[1]):
								leg_symbol[2] = 1
								print("2 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
								eval=True
								break

							#2 is a not a factor of leg_symbol[1] and leg_symbol[1] is not square
							#mod 4 rule
							elif isprime(leg_symbol[0]) and leg_symbol[0] > 2:
								if leg_symbol[0] % 4 == 1 or leg_symbol[1] % 4 == 1:
									temp=leg_symbol[0]
									leg_symbol[0]=leg_symbol[1]
									leg_symbol[1]=temp
								#elif leg_symbol[1] % 4 == 1:
								#	temp=leg_symbol[0]
								#	leg_symbol[0]=leg_symbol[1]
								#	leg_symbol[1]=temp
								elif leg_symbol[0] % 4 == 3:
									if leg_symbol[1] % 4 == 3:
										temp=leg_symbol[0]
										leg_symbol[0]=-leg_symbol[1]
										leg_symbol[1]=temp
								print("1 ~~~ Revised legendre_symbol after mod 4 rule:",leg_symbol)

					diff = leg_symbol[0] - leg_symbol[1]
					#print("Diff:",diff)

					if leg_symbol[0] == 1 or leg_symbol[0] == -1:
						print("b = 1 ============================")
						#print("Leg_symbol[0] == 1 or leg_symbol[0] == -1")
						#print("Leg_symbol[0]:",leg_symbol[0])
						leg_symbol[2] = leg_symbol[0]
						print("3 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						break
					elif diff == 1:
						print("b = 2 ============================")
						#print("Diff = 1")
						#print("Leg_symbol[0]:",leg_symbol[0])
						leg_symbol[2] = 1
						print("3 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						break
					elif diff == -1:
						print("b = 3 ============================")
						#print("diff = -1")
						#print("Leg_symbol[0]:",leg_symbol[0])
						leg_symbol[2] = -1
						print("4 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						break
					elif leg_symbol[0] > 1 and leg_symbol[1] > 1 and leg_symbol[0] > leg_symbol[1]:
						print("b = 4 ============================")
						#print("Leg_symbol[0] > 1 and leg_symbol[1] > 1 and leg_symbol[0] > leg_symbol[1]")
						print("Leg_symbol[0]:",leg_symbol[0])
						print("Leg_symbol[1]:",leg_symbol[1])

						#mod reduce leg_symbol[0]
						leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
						print("2 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)
						
						diff = leg_symbol[0] - leg_symbol[1]
						#print("Diff:",diff)
						
						if leg_symbol[0] == 1 or leg_symbol[0] == -1:
							print("b = 4a ============================")
							leg_symbol[2] = leg_symbol[0]
							print("5 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
							eval=True
							break
						elif diff == 1 or diff == -1:
							print("b = 4b ============================")
							leg_symbol[2] = diff
							print("6 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
							eval=True
							break
						elif leg_symbol[0] > leg_symbol[1]:
							print("b = 5c ============================")
							#mod reduce leg_symbol[1]
							leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
							print("3 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)

						#if diff == -1:
						#	print("b = 4c ============================")
						#	leg_symbol[2] = -1
						#	print("7 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						#	eval=True
						#	break

					elif leg_symbol[0] > 1 and leg_symbol[1] > 1 and leg_symbol[0] < leg_symbol[1]:
						print("b = 5 ============================")
						#print("Leg_symbol[0] > 1 and leg_symbol[1] > 1 and leg_symbol[0] < leg_symbol[1]")
						
						print("Leg_symbol[0]:",leg_symbol[0])
						print("Leg_symbol[1]:",leg_symbol[1])

						#print("TO DO")
						#input("Waiting for user..")

						#mod reduce leg_symbol[0]
						leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
						print("4 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)
						
						diff = leg_symbol[0] - leg_symbol[1]
						#print("Diff:",diff)
						
						if leg_symbol[0] == 1 or leg_symbol[0] == -1:
							print("b = 5a ============================")
							leg_symbol[2] = leg_symbol[0]
							print("7 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
							eval=True
							break
						elif diff == 1 or diff == -1:
							print("b = 5b ============================")
							leg_symbol[2] = diff
							print("8 --- Legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
							eval=True
							break
						elif leg_symbol[0] > leg_symbol[1]:
							print("b = 5c ============================")
							#mod reduce leg_symbol[1]
							leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
							print("5 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)


					#elif leg_symbol[0] > 1:
					#	print("Leg_symbol[0] > 1")
					#	print("Leg_symbol[0]:",leg_symbol[0])
					#	print("Leg_symbol[1]:",leg_symbol[1])

						#mod reduce leg_symbol[0]
					#	leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
					#	print("Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)
						
					#	diff = leg_symbol[0] - leg_symbol[1]
					#	print("Diff:",diff)
						
					#	if leg_symbol[0] == 1 or leg_symbol[0] == -1:
					#		print("b = 6 ============================")
					#		leg_symbol[2] = leg_symbol[0]
					#		print("legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
					#		eval=True
					#		break

					#mod reduce leg_symbol[0]
					#if leg_symbol[0] != 1:
					#	if leg_symbol[0] != -1:
					#		print("Leg_symbol[0] not  1 nor -1")
					#		leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
					#		print("Revised legendre_symbol after mod", leg_symbol[1],":",leg_symbol)
							
					#		if leg_symbol[0] == 1 or leg_symbol[0] == -1:
					#			print("b = 7 ============================")
					#			leg_symbol[2] = leg_symbol[0]
					#			print("legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
					#			eval=True
					#			#break
					
					elif leg_symbol[0] == 1 or leg_symbol[0] == -1:
						print("b = 8 ============================")
						print("Leg_symbol[0] is 1 or -1")
						leg_symbol[2] = leg_symbol[0]
						print("9 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						break
					elif leg_symbol[0] > 1:
						print("Leg_symbol[0]",leg_symbol[0],"is > 1")
						leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
						print("6 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)

					if not leg_symbol[0] == 1:
						if leg_symbol[1] >=2:
							if isprime(leg_symbol[0]) and leg_symbol[0] > 2:
								#mod 4 rules
								if leg_symbol[0] % 4 == 1:
									print("leg_symbol[0] % 4 == 1")
									temp=leg_symbol[0]
									leg_symbol[0]=leg_symbol[1]
									leg_symbol[1]=temp
								elif leg_symbol[1] % 4 == 1:
									print("leg_symbol[1] % 4 == 1")
									temp=leg_symbol[0]
									leg_symbol[0]=leg_symbol[1]
									leg_symbol[1]=temp
								elif leg_symbol[0] % 4 == 3:
									if leg_symbol[1] % 4 == 3:
										print("leg_symbol[1] % 4 == 3")
										temp=leg_symbol[0]
										leg_symbol[0]=-leg_symbol[1]
										leg_symbol[1]=temp
								print("7 ~~~ Revised legendre_symbol after mod 4 rule:",leg_symbol)

							elif leg_symbol[0] == 2 and isprime(leg_symbol[1]):
								print("c = 1 ++++++++++++")
								print("Leg_symbol[0] == 2 and isprime(",leg_symbol[1],") == True")
								if leg_symbol[1] % 8 == 1 or leg_symbol[1] % 8 == 7: 
									leg_symbol[2] = 1
									print("10 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
									break

								elif leg_symbol[1] % 8 == 3 or leg_symbol[1] % 8 == 5: 
									leg_symbol[2] = -1
									print("11 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
									break

								else: 
									leg_symbol[2] = (-1)**(p**2 / 8)
									print("12 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
									break

							elif leg_symbol[0] == 3 and isprime(leg_symbol[1]) and leg_symbol[2] != 3:
								print("c = 2 ++++++++++++")
								print("Leg_symbol[0] == 3 and isprime(",leg_symbol[1],") == True",leg_symbol[2],"!= 3")
								if leg_symbol[1] % 8 == 1 or leg_symbol[1] % 8 == 7: 
									leg_symbol[2] = -1
									print("13 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
									break

								elif leg_symbol[1] % 12 == 1 or leg_symbol[1] % 12 == 11: 
									leg_symbol[2] = 1
									print("14 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
									break

								else: 
									leg_symbol[2] = (-1)**(p**2 / 8)
									print("15 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
									break

							#elif leg_symbol[0] == 2:
							#	print("c = 3 ++++++++++++")
							#	print("Leg_symbol[0] == 2 and isprime(",leg_symbol[1],") == False")
							#	print("Undefined as",leg_symbol[1],"is not prime")

							else:
								print("c = 3 ++++++++++++")
								print("Running factorise_powers(",leg_symbol[0],")")
								result_ls = factorise_powers(leg_symbol[0])
								#return prime_factors, powers, round(c_calc_primefactors,8), round(c_calc_powers,8), round(total_calc_time,8)
								prime_factors_ls =result_ls[0]
								powers_ls = result_ls[1]
								print(result_ls)

								powers_new_ls=[]
								for power_ls in powers_ls:
									if power_ls >=2:
										powers_new_ls.append(power_ls % 2)
									else:
										powers_new_ls.append(power_ls)

								print("powers_ls mod 2:",powers_new_ls)





								print("TO DO") ##TO DO
								input("Waiting for user..")

					if leg_symbol[0] == 1:
						print("b = 9 ============================")
						print("leg_symbol[0] == 1 or leg_symbol[0] == -1")
						leg_symbol[2] = leg_symbol[0]
						print("16 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						break
					elif leg_symbol[0] == -1:
						print("b = 10 ============================")
						print("leg_symbol[0] == -1")
						leg_symbol[2] = leg_symbol[0]
						print("17 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						#break
					elif leg_symbol[0] > 1:
						print("leg_symbol[0] > 1")
						leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
						print("8 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)		

					if leg_symbol[0] != 1:
						if leg_symbol[0] != -1:		
							print("leg_symbol[0] not 1 nor -1")
							#mod reduce leg_symbol[0]
							leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
							print("9 ~~~ Revised legendre_symbol after mod", leg_symbol[1],":",leg_symbol)
					elif leg_symbol[0] == 1 or leg_symbol[0] == -1:
						print("b = 11 ============================")
						print("leg_symbol[0] == 1 or == -1")
						leg_symbol[2] = leg_symbol[0]
						print("18 --- legendre_symbol evaluated for:",leg_symbol,"as:",leg_symbol[2])
						eval=True
						break
					elif leg_symbol[0] > 1:
						print("leg_symbol[0] > 1")
						leg_symbol[0] = leg_symbol[0] % leg_symbol[1]
						print("10 ~~~ Revised legendre_symbol after mod",leg_symbol[1],":",leg_symbol)

				return leg_symbol, eval

def factorise_powers(N):

	#call number_checks() for simple checks on input 
	#number_checks(N)	
	
	#Call size_input_check() if want to stop program running for very large numbers 
	#size_input_check()

	len_N = len(str(N))

	#if len_N <= 5:
	#	result1 = w235_primefactors_powers_v5.factorise_trialdivision(N)
	#	#return factors, c_factorisations
	#	factors = result1[0]
	#	c_factorisations = result1[1]

	if 0 < len_N <= 10:

	#elif 5 < len_N <= 10:
		result1 = w235_primefactors_powers_v5.factorise_235wheel(N)
		#return factors, c_factorisations
		factors = result1[0]
		c_factorisations = result1[1]

	elif 20 < len_N <= 30: #Typical according to Google Gemini
	#	#"run for a fixed, limited number of iterations to quickly pull out any "small" prime factors (up to roughly 10–15 decimal digits).
		result1 = factorise_pollards_rho(N)
		#return factors, c_factorisations
		factors = result1[0]
		c_factorisations = result1[1]

	#elif 30 < len_N <= 40: #Typical according to Google Gemini
		#"run for a fixed, limited number of iterations to quickly pull out any "small" prime factors (up to roughly 10–15 decimal digits) before handing the remaining composite over to ECM.
	#	result1 = factorise_pollards_rho(N)
	#	#return factors, c_factorisations
	#	factors = result1[0]
	#	c_factorisations = result1[1]

	#	result2 = factorise_ECM(N)
	#	#return factors, c_factorisations
	#	factors = result2[0]
	#	c_factorisations = result2[1]

	#elif 40 < len_N <= 50: #Self Initializing Quadratic SIeve (SIQS / MPQS)
		#"Self-Initializing Quadratic Sieve (SIQS / MPQS). This is the lower bound where the Quadratic Sieve begins to outpace ECM for tough semiprimes with equally sized factors"
		#"run for a fixed, limited number of iterations to quickly pull out any "small" prime factors (up to roughly 10–15 decimal digits) before handing the remaining composite over to SIQS.
	#	result1 = factorise_pollards_rho(N)
		#return factors, c_factorisations
	#	factors = result1[0]
	#	c_factorisations = result1[1]

	#	result2 = factorise_SIQS(N)
		#return factors, c_factorisations
	#	factors = result2[0]
	#	c_factorisations = result2[1]

	#	result3 = factorise_MPQS(N)
		#return factors, c_factorisations
	#	factors = result3[0]
	#	c_factorisations = result3[1]

	#elif 50 < len_N <= 100: #QS dominance
		#Includes variants MPQS and SIQS

		#"run for a fixed, limited number of iterations to quickly pull out any "small" prime factors (up to roughly 10–15 decimal digits) before handing the remaining composite over to SIQS.
	#	result1 = factorise_pollards_rho(N)
		#return factors, c_factorisations
	#	factors = result1[0]
	#	c_factorisations = result1[1]

	#	result2 = factorise_SIQS(N)
		#return factors, c_factorisations
	#	factors = result2[0]
	#	c_factorisations = result2[1]

	#	result3 = factorise_MPQS(N)
		#return factors, c_factorisations
	#	factors = result3[0]
	#	c_factorisations = result3[1]

	#elif 100 < len_N <= 110: #NFS - SIQS to GNFS transition zone
	#	result1 = factorise_SIQS(N)
		#return factors, c_factorisations
	#	factors = result1[0]
	#	c_factorisations = result1[1]

	#	result2 = factorise_GNFS(N)
		#return factors, c_factorisations
	#	factors = result2[0]
	#	c_factorisations = result2[1]

	#elif 110 < len_N: #NFS - GNFS era
	#	result1 = factorise_GNFS(N)
		#return factors, c_factorisations
	#	factors = result1[0]
	#	c_factorisations = result1[1]

	#print("Factors are:",factors)
	#print("Time for factorisation is:",round(c_factorisations,8))
	
	result2 = calc_primefactors_powers(N, factors)
	#return prime_factors, powers, c_calc_primefactors, c_calc_powers		
	prime_factors = result2[0]
	powers = result2[1]
	c_calc_primefactors = result2[2]
	c_calc_powers = result2[3]
	total_calc_time = c_factorisations + c_calc_powers + c_calc_primefactors

	#print("Prime factors are:",prime_factors)
	#print("powers are:",powers)
	#print("time for calc prime factors & powers is:",round(c_calc_powers + c_calc_primefactors,8))
	#print("total calc time is: ",round(total_calc_time,8))

	return prime_factors, powers, round(c_calc_primefactors,8), round(c_calc_powers,8), round(total_calc_time,8)

def factorise_235wheel(N):		
	#based on code on https://stackoverflow.com/questions/16996217/prime-factorization-list/
	#Author states this is is O(sqrt(n))) and 2 to 3 times faster than trial division in practice
	#Wheel factorization, which uses a cyclic set of gaps between potential primes to greatly
	#reduce the number of trial divisions.
	#uses a 2,3,5-wheel

	#print("Running factorise()..")	

	#Create lists to hold prime factors of N and corresponding powers
	#s_before_lists = time.time()	
	factors = []
	#c_lists = time.time() - s_before_lists

	#print("Calculating prime factors and powers"
	s_before_factorisations = time.time()	
	#N=5 - gets listed as remainder instead of factor!!!	
		
	gaps=[1,2,2,4,2,4,2,4,6,2,6]
	length, cycle = 11,3
	f, factors, next = 2, [], 0
	while f*f <= N:
		while N % f == 0:		
			#f is a factor. Add factor f to fs
			factors.append(f)
			N /= f
		f += gaps[next]		
		next += 1
		if next == length:
			next = cycle
	if N > 1: factors.append(int(N))
		
	c_factorisations = time.time() - s_before_factorisations

	#print("Factors are: "+str(factors)
	#print("c_factorisations are: "+str(c_factorisations)

	#input("Waiting for user..")	
	
	#c_pps=result2[3]
	#c_nrem=result2[4]

	return factors, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations
	#return prime_factors, powers, remainder, c_lists, c_factorisations, c_pps, c_nrem


#def factorise_trialdivision(N):



#def factorise_pollards_rho(N):



#def factorise_williams_p+1(N):



#def factorise_ECM(N):



#def factorise_SIQS(N):



#def factorise_MPQS(N):



#def factorise_GNFS(N):



def isSquare(N):
	#Checks for divisibility by square numbers giving remainder of 1
	if N==1:
		return True

	i = 2
	while i**2 <= N:
		if N / i**2 == 1:
			return True
		i += 1

	return False

def isprime(p):		
	#Checks for divisibility by factors upto sqrt(n)
	#Likely to be O(sqrt(n))
	
	print("Running isprime(",str(p),")..")
	# www.rookieslab.com/posts/fastest-way-to-check-if-a-number-is-prime-or-not
	if p==1:
		return False	
		
	i = 2
	while i*i <= p:
		if p % i == 0:
			return False
		i += 1

	return True

def is_primitive_root(g, p):
	#Efficiently checks if g is a primitive root modulo p.
	#Time Complexity: O(sqrt(p) + log(p)) due to factorization.
	if g <= 1 or g >= p:
    		return False

	#Step 1: Get the unique prime factors of phi(p) which is p-1
	totient = p - 1
	prime_factors = get_unique_prime_factors(totient)
	print("prime factors of p-1:",prime_factors)

	# Step 2: Test powers
	for q in prime_factors:
		test_exponent = totient // q
		if pow(g, test_exponent, p) == 1:
			return False  # Failed the test; g loops too early
            
	return True  # Passed all tests; g is a primitive root

def get_unique_prime_factors(n):
    #Finds all unique prime factors of a number n
    factors = set()
    # Check factor 2
    if n % 2 == 0:
        factors.add(2)
        while n % 2 == 0:
            n //= 2
            
    #Check odd factors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 2
        
    #If n is still greater than 1, then n itself is prime
    if n > 1:
        factors.add(n)
    return factors

def calc_primefactors_powers(N, factors):
	#print("------------------"
	#print("Running calc_primefactors_powers(",factors,")..")
	
	#Now want to find max powers m for each factor in factors.
	#can do this by counting unique factors			
	prime_factors=[]
	fac_list = []
	c_calc_primefactors = 0
	s_before_primefactors = time.time()	
	for factor in factors:		
		#print("------------------"	
		#print("factor is: "+str(factor)		
		if factor not in fac_list:
			#factor is not in fac_list
			#add factor to prime_factors
			prime_factors.append(factor)
			#print("Added "+str(factor)+" to prime_factors"
			#print("prime_factors is: "+str(prime_factors)
			#print str(factor)+" is NOT in fac_list"
			#append it				
			fac_list.append(factor)				
			
			#print("count is: "+str(count)
			#print("fac_list is: "+str(fac_list)
				
		else:
			#factor is in fac_list
			fac_list.append(factor)
			#print str(factor)+" added to fac_list"
	
	#prime_factors = fs
	#print("Prime_factors are: "+str(prime_factors)
	#prime_factors.append(factor)
	#print("Added "+str(factor)+" to prime_factors"
	
	#print("Prime_factors are: "+str(prime_factors)
	c_calc_primefactors = time.time() - s_before_primefactors

	powers = []
	s_before_calc_powers = time.time()
	for prime_factor in prime_factors:
		count = 0
		while N % prime_factor == 0:
			count = count + 1
			N = N / prime_factor		
		else:
			powers.append(count)
				
	#print("powers are: "+str(powers)
	c_calc_powers = time.time() - s_before_calc_powers

	#input("Waiting for user..")	

	return prime_factors, powers, c_calc_primefactors, c_calc_powers

if __name__=='__main__':
	#main()
	#result = leg_s_g_p_new(2, 1009)
	#result = leg_s_g_p_new(51, 1009)
	result = leg_s_g_p_new(513, 100907)

	print("legendre_symbol_g_p is:",str(result))

#def legendre_symbol_g_p(g,p):
#
#	#print('Running legendre_symbol_g_p(',g,',',p,')...')
#
#	#outputs the legendre symbol (g over p) for inputs g and p 
#	#legendre_g_p(g over p) == -1 when g is a quadratic residue mod p and g % p !=0 
#	#legendre_g_p(g over p) == 1 when g is a non-quadratic residue mod p
#	#legendre_g_p(g over p) == 0 when g % p = 0
#
#	power=int((p-1)/2)
#	#print('power:',power)
#
#	legendre_symbol_g_p=pow(g,power,p)
#
#	if legendre_symbol_g_p > 1:
#		legendre_symbol_g_p = legendre_symbol_g_p - p
#	
#	return legendre_symbol_g_p
