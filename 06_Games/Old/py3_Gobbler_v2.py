#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 2. 19/06/2018.
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

version = 2

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version:",version,". 19/06/2018.")
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
	black_pieces_off_board =[[XL_B, L_B, M_B, S_B],[XL_B, L_B, M_B, S_B],[XL_B, L_B, M_B, S_B]]

	#white_pieces_on_board = []
	#black_pieces_on_board = []

	Size_board_x = 4	
	Size_board_y = 4

	Squares_on_board = Size_board_x * Size_board_y 

	#initialise board
	board =[for x in ]

	print("Welcome to Gobbler! Size of board is:",Size_board_x," by ",Size_board_y,"") 
	
	while Victory == False:
		print("White to move!")		
		colour_to_move = "W"
		result1 = pieces_available_to_choose(white_pieces_off_board, board, colour_to_move)
		# = result[0]
		print("Pieces available for White to move:",result)



		print("Black to move!")
		colour_to_move = "B"		
		result2 = pieces_available_to_choose(black_pieces_off_board, board, colour_to_move)
		print("Pieces available for Black to move:",result)
		input("waiting for user..")

	data="Output\n------------\n"

	#print("data:",data)
	txtfile_create_new(data,output_path)

	data_for_append = []


def pieces_available_to_choose(pieces_off_board, board, colour_to_move):
	
	print("pieces_off_board:",pieces_off_board,", board:",board,", colour_to_move:",colour_to_move)

	pieces_to_choose = []
	empty_square = False

	#check if there are any empty squares on board
	for row in board:
		if empty_square == False:
			for square in row:
				if not square:
					#a square is empty
					empty_square = True
					break
		else:
			break	

	#now store pieces_on_board for colour_to_move
	#for row in board:
	#	for piece in row:
	#		#want to take last character from piece
	#		last_char_piece = piece[-1:]			
	#		print("last_char_piece:",last_char_piece)
	#		if last_char_piece == colour_to_move:
	#			pieces_to_choose.append(piece)

	if empty_square == True:
		#There is an empty square on board
		for piece in pieces_off_board:
			pieces_to_choose.append(piece)

		#now store pieces_on_board for colour_to_move
		for row in board:
			for piece in row:
				#want to take last character from piece
				last_char_piece = piece[-1:]			
				print("last_char_piece:",last_char_piece)
				if last_char_piece == colour_to_move:
					pieces_to_choose.append(piece)
	else:
		#There are no empty squares on board
		#now store pieces_on_board for colour_to_move
		for row in board:
			for piece in row:
				#want to take last character from piece
				last_char_piece = piece[-1:]			
				print("last_char_piece:",last_char_piece)
				if last_char_piece == colour_to_move:
					pieces_to_choose.append(piece)

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

