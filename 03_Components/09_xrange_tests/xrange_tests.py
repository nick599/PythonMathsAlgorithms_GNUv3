#import sys
#import math
#import os
#import itertools
#import csv
#import time

def main():

	#num=""
	result= OneXvalue_3nested_xranges_wo_breaks()
	#raw_input("Waiting for user..")	
	result= OneXvalue_3nested_xranges_with_1break()
	#raw_input("Waiting for user..")
	result= TwoXvalues_3nested_xranges_with_1break()
	#raw_input("Waiting for user..")
	result= TwoXvalues_3nested_xranges_wo_break()
	#raw_input("Waiting for user..")

def OneXvalue_3nested_xranges_wo_breaks():

	print " ----------- Running 1xvalue_3nested_xranges_wo_breaks -----------"
	cumul_sum=0
	concat_list=[]
	for x in xrange(2,3):
		for y in xrange(2,100):
			concat_x_y = str(x)+"_"+str(y)
			if concat_x_y in concat_list:
				print "concat_x_y previously appended into list!"							
			else:
				concat_list.append(concat_x_y)
			for z in xrange(2,1000):
				cumul_sum=cumul_sum + 1
		status = True
		#print "status is True"
		print "concat_x_y: "+str(concat_x_y)
		print "cumul_sum is: "+str(cumul_sum)

	return status

def OneXvalue_3nested_xranges_with_1break():

	print " ----------- Running 1xvalue_3nested_xranges_with_1break -----------"
	cumul_sum=0
	concat_list=[]
	for x in xrange(2,3):
		for y in xrange(2,100):
			concat_x_y = str(x)+"_"+str(y)
			if concat_x_y in concat_list:
				print "concat_x_y previously appended into list!"							
			else:
				concat_list.append(concat_x_y)
			for z in xrange(2,1000):
				cumul_sum=cumul_sum + 1
				if z == x:
					break
		status = True
		#print "status is True"
		print "concat_x_y: "+str(concat_x_y)
		print "cumul_sum is: "+str(cumul_sum)

	return status

def TwoXvalues_3nested_xranges_with_1break():

	print "----------- Running 2xvalues_3nested_xranges_with_1break -----------"
	cumul_sum=0
	concat_list=[]
	for x in xrange(2,4):
		for y in xrange(2,100):
			concat_x_y = str(x)+"_"+str(y)
			if concat_x_y in concat_list:
				print "concat_x_y previously appended into list!"							
			else:
				concat_list.append(concat_x_y)
			for z in xrange(2,1000):
				cumul_sum=cumul_sum + 1
				if z == x:
					break
		status = True
		#print "status is True"
		print "concat_x_y: "+str(concat_x_y)
		print "cumul_sum is: "+str(cumul_sum)

	return status

def TwoXvalues_3nested_xranges_wo_break():

	print "----------- Running 2xvalues_3nested_xranges_wo_break -----------"
	cumul_sum=0
	concat_list=[]
	for x in xrange(2,4):
		for y in xrange(2,100):
			concat_x_y = str(x)+"_"+str(y)
			if concat_x_y in concat_list:
				print "concat_x_y previously appended into list!"							
			else:
				concat_list.append(concat_x_y)
			for z in xrange(2,1000):
				cumul_sum=cumul_sum + 1

		status = True
		#print "status is True"
		print "concat_x_y: "+str(concat_x_y)
		print "cumul_sum is: "+str(cumul_sum)

	return status

if __name__ == "__main__":
	main()




