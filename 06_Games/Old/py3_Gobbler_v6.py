#Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.
#Version 5. 25/06/2018.
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

version = 6

print("Copyright Nick Prowse 2018. Code Licenced under GNU GPL v3.")
print("Version:",version,". 25/06/2018.")
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

	white_pieces_off_board =[["XL_W", "L_W", "M_W", "S_W"],["XL_W", "L_W", "M_W", "S_W"],["XL_W", "L_W", "M_W", "S_W"]]
	black_pieces_off_board =[["XL_B", "L_B", "M_B", "S_B"],["XL_B", "L_B", "M_B", "S_B"],["XL_B", "L_B", "M_B", "S_B"]]

	#white_pieces_on_board = []
	#black_pieces_on_board = []

	Size_board_x = 4	
	Size_board_y = 4
	board = [""] * Size_board_x

	#print("initial board:",board)

	Num_squares_on_board = Size_board_x * Size_board_y 

	#initialise board
	#board =[for x in ]
	for i in range(Size_board_x):
		board[i]= [""] * Size_board_y	

	print("Welcome to Gobbler!\nSize of board is:",Size_board_x," by ",Size_board_y,"") 
	
	print("board:",board)

	while Victory == False:
		print("White to move!")		
		colour_to_move = "W"
		result1 = pieces_available_to_choose(white_pieces_off_board, board, colour_to_move)
		#return pieces_to_choose, pieces_on_board_column, pieces_on_board_row
		pieces_to_choose = result1[0]
		pieces_on_board_column = result1[1]
		pieces_on_board_row = result1[2]
		
		print("Pieces available for White to move:\n",pieces_to_choose)
		piece_chosen = input("Please type the piece to be moved..\n")		
		while piece_chosen not in pieces_to_choose:
			print("Piece chosen:",piece_chosen," is not in pieces available to chose:",pieces_to_choose) 
			print("Type another piece")
			piece_chosen = input("Please type the piece to be moved..\n")

		#print("Piece chosen:",piece_chosen)

		#Need to obtain index (row & column) of piece chosen in board
		piece_found = False
		square_piece_chosen_col = ""
		square_piece_chosen_row = ""
		for row in board:
			if piece_found == True:
				break
			for piece in row:
				if piece_found == True:
					break
				elif piece == piece_chosen:
					square_piece_chosen_col = row.index(piece)
					square_piece_chosen_row = board.index(row)
					piece_found = True
					break

		if square_piece_chosen_col == "" or square_piece_chosen_row == "":
			print("Piece chosen",piece_chosen,"is off-board")
		else:
			print("Piece chosen:",piece_chosen, ", Row of piece chosen:",square_piece_chosen_row,"Col of piece chosen:",square_piece_chosen_col)

		#White Piece is chosen, now need user to specify which square to put piece on / move it to
		result2 = squares_available_to_move_to(piece_chosen, square_piece_chosen_col, square_piece_chosen_row, board, colour_to_move)
		print("Squares available to move to:\n",result2)
		square_chosen = input("Please type the square to move ",piece_chosen," to ..\n")

		while square_chosen not in result2:
			print("Square chosen:",square_chosen," is not available to move to. Squares availiable:",result2) 
			print("Type another square")
			square_chosen = input("Please type the square to be moved to..\n")

		input("waiting for user..")
		
		print("Black to move!")
		colour_to_move = "B"		
		result3 = pieces_available_to_choose(black_pieces_off_board, board, colour_to_move)
		#return pieces_to_choose, pieces_on_board_column, pieces_on_board_row
		pieces_to_choose = result3[0]
		pieces_on_board_column = result3[1]
		pieces_on_board_row = result3[2]

		print("Pieces available for Black to move:\n",pieces_to_choose)
		piece_chosen = input("Please type the piece to be moved..\n")
		while piece_chosen not in pieces_to_choose:
			print("Piece chosen:",piece_chosen," is not in pieces available to chose:",pieces_to_choose) 
			print("Type another piece")
			piece_chosen = input("Please type the piece to be moved..\n")

		#print("Piece chosen:",piece_chosen)

		#Need to obtain index (row & column) of piece chosen in board
		piece_found = False
		square_piece_chosen_col = ""
		square_piece_chosen_row = ""
		for row in board:
			if piece_found == True:
				break
			for piece in row:
				if piece_found == True:
					break
				elif piece == piece_chosen:
					square_piece_chosen_col = row.index(piece)
					square_piece_chosen_row = board.index(row)
					piece_found = True
					break

		if square_piece_chosen_col == "" or square_piece_chosen_row == "":
			print("Piece chosen",piece_chosen,"is off-board")
		else:
			print("Piece chosen:",piece_chosen, ", Row of piece chosen:",square_piece_chosen_row,"Col of piece chosen:",square_piece_chosen_col)
		
		#Black Piece is chosen, now need user to specify which square to put piece on / move it to
		result2 = squares_available_to_move_to(piece_chosen, square_piece_chosen_col, square_piece_chosen_row, board, colour_to_move)
		print("Squares available to move to:\n",result2)
		square_chosen = input("Please type the square to move ",piece_chosen," to ..\n")

		while square_chosen not in result2:
			print("Square chosen:",square_chosen," is not available to move to. Squares availiable:",result2) 
			print("Type another square")
			square_chosen = input("Please type the square to be moved to..\n")

		#input("waiting for user..")
		input("waiting for user..")

		
	data="Output\n------------\n"

	#print("data:",data)
	txtfile_create_new(data,output_path)

	data_for_append = []


def pieces_available_to_choose(pieces_off_board, board, colour_to_move):
	
	#print("pieces_off_board:\n",pieces_off_board,"\nboard:\n",board,"\ncolour_to_move:\n",colour_to_move)

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

	if empty_square == True:
		#There is an empty square on board
		#Need to only be able to choose the pieces on top of each stack!
			
		#print("pieces_off_board:",pieces_off_board)
		for stack in pieces_off_board:
			#print("stack:",stack)
			#print("stack[0]:",stack[0])
			piece = stack[0]
			pieces_to_choose.append(piece)

		#now store pieces_on_board for colour_to_move
		pieces_on_board_column = []
		pieces_on_board_row = []
		for row in board:
			for piece in row:
				#want to take last character from piece
				#print("piece:",piece)
				#last_char_piece = piece[-1:]			
				#print("last_char_piece:",last_char_piece)
				if piece[-1:] == colour_to_move:
					pieces_to_choose.append(piece)
					pieces_on_board_column.append(row.index(piece))
					pieces_on_board_row.append(board.index(row)) 
	else:
		#There are no empty squares on board
		#now store pieces_on_board for colour_to_move
		pieces_on_board_column = []
		pieces_on_board_row = []
		for row in board:
			for piece in row:
				#want to take last character from piece
				#print("piece:",piece)
				#last_char_piece = piece[-1:]			
				#print("last_char_piece:",last_char_piece)
				if piece[-1:] == colour_to_move:
					pieces_to_choose.append(piece)
					pieces_on_board_column.append(row.index(piece))
					pieces_on_board_row.append(board.index(row)) 

	return pieces_to_choose, pieces_on_board_column, pieces_on_board_row

def squares_available_to_move_to(piece_chosen, square_piece_chosen_col, square_piece_chosen_row, board, colour_to_move):
	
	print("-----------------------------------------")
	print("Running squares_available_to_move_to..")	
	print("piece_chosen:\n", piece_chosen,"\nboard:\n", board,"\ncolour_to_move:\n", colour_to_move)

	squares_avail_to_move_to = []
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

	if empty_square == True:
		#There is an empty square on board
		#Need to only be able to choose the pieces on top of each stack!
			
		#print("pieces_off_board:",pieces_off_board)
		for stack in pieces_off_board:
			#print("stack:",stack)
			#print("stack[0]:",stack[0])
			piece = stack[0]
			pieces_to_choose.append(piece)

		#now store pieces_on_board for colour_to_move
		for row in board:
			for piece in row:
				#want to take last character from piece
				#print("piece:",piece)
				last_char_piece = piece[-1:]			
				#print("last_char_piece:",last_char_piece)
				if last_char_piece == colour_to_move:
					pieces_to_choose.append(piece)
	else:
		#There are no empty squares on board
		#now store pieces_on_board for colour_to_move
		for row in board:
			for piece in row:
				#want to take last character from piece
				#print("piece:",piece)
				last_char_piece = piece[-1:]			
				#print("last_char_piece:",last_char_piece)
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

