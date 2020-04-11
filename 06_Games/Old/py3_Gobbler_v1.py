#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 1. 18/06/2018.
#Programmed & tested in Python 3.4.3 only
#This program run a game of "Gobbler" - for 2 players, 3 stacks each of 4 sizes of piece in each stack. 
#It has been tested on Linux Mint v3.19 x64.

import sys
import math
#import os
#import itertools
#import csv
#import time

#python_version = sys.version

#print(python_version)

version = 1

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version:",version,". 18/06/2018.")
print("Programmed & tested in python 3.4.3 only.")
print("This program run a game of \"Gobbler\" - for 2 players, 3 stacks each of 4 sizes of piece in each stack. ")
print("It has been tested on Linux Mint v3.19 x64")
print("---------------------------------------------------------------------")

folder = "/home/mint/Desktop/"
output_filename = "output_Gobbler_v"+str(version)+".txt"
output_path = folder + output_filename
#print("output_path is:",output_path)

def main():
	
	Victory = False

	white_pieces_off_board =[[XL_W, L_W, M_W, S_W],[XL_W, L_W, M_W, S_W],[XL_W, L_W, M_W, S_W]]
	black_pieces_off_board =[[XL_W, L_W, M_W, S_W],[XL_W, L_W, M_W, S_W],[XL_W, L_W, M_W, S_W]]

	white_pieces_on_board = []
	black_pieces_on_board = []

	Size_board_x = 4	
	Size_board_y = 4

	Squares_on_board = Size_board_x * Size_board_y 

	#initialise board
	board =[for x in ]

	print("Welcome to Gobbler! Size of board is:",Size_board_x," by ",Size_board_y,"") 
	
	
	while Victory == False:
		print("White to move!")		
		result = pieces_available_to_choose(white_pieces_off_board, white_pieces_on_board)

	input("waiting for user..")

	data="Output\n------------\n"

	#print("data:",data)
	txtfile_create_new(data,output_path)

	data_for_append = []


def pieces_available_to_choose(pieces_off_board, pieces_on_board):
	
	pieces_to_choose = []


	return pieces_to_choose

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

if __name__=='__main__':
	main()

