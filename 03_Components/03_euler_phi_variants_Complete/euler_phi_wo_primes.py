import math

def main():

	print 'Enter number to be tested: '			#O(1)
	n_initial = raw_input()					#O(1)
	if n_initial.isdigit() is False:			#O(1)
		print('You have not entered a positive integer for n. n is: '+str(n_initial)+'. Please reenter.')
		sys.exit()						#O(1)

	#now convert n_initial into a long:
	n = long(n_initial)					#O(1)

	result = euler_phi_noprimesused(n)
	#return count_k, status

	count_k = result[0]
	status = result[1]

	#print "count_k is: "+str(count_k)+", status is: "+str(status)

	if status == True:
		print "euler_phi_noprimesused("+str(n)+") is: "+str(count_k)
	elif status == False and count_k == 0:
		print "euler_phi_noprimesused("+str(n)+") is: "+str(count_k)
	elif status == False and count_k <> 0:
		print "CHECK - status is False and count_k <> 0 !"
	else:
		print "CHECK - status is "+str(status)+", euler_phi_noprimesused("+str(n)+") is: "+str(count_k)

def euler_phi_noprimesused(n):	

	#euler_phi_noprimesused(n) = amount of integers k, where 1 <= k <= n for which the gcd(n,k)=1
	
	#print "Running euler_phi_noprimesused("+str(n)+").."
	status = False					#O(1)
	count_k = 0	

	#gcd(n,k) --> b=min(n,k) 
	#==> h=#base 10 digits of b
	# now h = int(math.floor(math.log(b,10))) + 1
	# Hence h = int(math.floor(math.log(min(n,k),10))) + 1

	for k in xrange(1, n + 1):		#O(n)	#Subtotal: O(n*pow(h,2))			
		#print "-----------------"
		#print "k is: "+str(k)		
		g, x, y = egcd(n, k) 

		if g == 1:			#1 op for if. #O(pow(h,2)) for gcd
			#print "egcd("+str(n)+", "+str(k)+") is 1"
			status = True
			count_k = count_k + 1			#1 op
			#print "k is "+str(k)+", count_k is now: "+str(count_k)	
			

	#print "count_k is: "+str(count_k)
	if count_k <> 0:
		status=True
	else:
		status=False

	return count_k, status

def egcd(a, b):							#O(n)
	#print("Running egcd("+str(a)+","+str(b)+")")
	#print "a is: "+str(a)
	#print "b is: "+str(b)	
	if a == 0:						#O(1)	#Subtotal: O(2)
		return (b, 0, a)				#O(1)
	g, y, x = egcd(b % a, a)				
	#print("egcd("+str(a)+","+str(b)+") is: "+str(g)+" "+str(x - (b//a) * y)+" "+str(y))
	return (g, x - (b//a) * y, y)

if __name__=='__main__':
	main()
