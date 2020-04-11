#Source: stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
#Date accessed: 21/04/18

def main():
	s1 = "attack at dawn"
	print "s1 is: "+str(s1)	
	s2 = "really why"
	print "s2 is: "+str(s2)
	output_string = sxor_output_string(s1, s2)	
	print "output string is:\n"+str(output_string)
	output_number = sxor_output_number(s1, s2)
	print "output number is:\n"+str(output_number)
	
def sxor_output_string(s1, s2):
	#print "zip(s1,s2) is: "+str(zip(s1,s2))
	#return ''.join(ord(a) ^ ord(b) for a,b in zip(s1,s2))
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

	#output_string=''
	#for a,b in zip(s1,s2):
	#	print "a, b is: "+str(a)+", "+str(b)
	#	print "chr(ord("+str(a)+") ^ ord("+str(b)+")) is: "+str(chr(ord(a) ^ ord(b)))
	#	print "ord("+str(a)+") ^ ord("+str(b)+") is: "+str(ord(a) ^ ord(b))
	#	#print "output_string is: "+str(output_string)

def sxor_output_number(s1, s2):
	#print "zip(s1,s2) is: "+str(zip(s1,s2))
	#return ''.join(ord(a) ^ ord(b) for a,b in zip(s1,s2))
	#return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

	s=""
	ans_working=[]
	for a,b in zip(s1,s2):
		#print "a, b is: "+str(a)+", "+str(b)
	#	print "chr(ord("+str(a)+") ^ ord("+str(b)+")) is: "+str(chr(ord(a) ^ ord(b)))
		
		#print ord(a) ^ ord(b)
		if len(str(ord(a) ^ ord(b))) < 2:
			#print "ord("+str(a)+") ^ ord("+str(b)+") is: "+str(ord(a) ^ ord(b))+str(0)
			ans = str(ord(a) ^ ord(b))+str(0)		
		else:
			#print "ord("+str(a)+") ^ ord("+str(b)+") is: "+str(ord(a) ^ ord(b))
			ans = str(ord(a) ^ ord(b))
		#print "ans is: "+str(ans)
		ans_working.append(ans)
		#print "ans_working before is: "+str(ans_working)
		#.join(ans_working, ans)
	
	return s.join(ans_working)
	#print "ans_working is: "+str(s.join(ans_working))

if __name__ == "__main__":
	main()
