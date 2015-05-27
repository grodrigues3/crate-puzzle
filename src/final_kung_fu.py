#!/usr/local/python/bin/python
"""
Title
Author: Garrett Rodrigues
Date: 04/22/14
Description:
	This file is python script that solves the kung fu crate puzzle
	as seen online at www.puzzlebeast.com/crate/.  Input a sample game
	file specified in JSON format that should be in a sample_games folder 
	in a child directory.

	The solve_game function uses a backtracking approach to solving the
	puzzle and tries every combination of moves, while keeping track of
	squares it has already visited.  If a topple occurs, it resets
	the visited list because new paths may now be possible.

	solve_game: 
		inputs: 1)board_config- 3-element list containing current location, board and visitedl ist
		returns: boolean indicating whether current path found the end
		effects: also responsible for contributing the Global path variable which gives 
		correct sequences of left and rights
	move####:
		inputs: 1) position- [r,c] list
			2) board - a copy of the current board configuration as a numpy matrix (array)
			3) visited - a numpy array of the relevant already visited squares for this search attempt  
	


"""

import simplejson as json
import numpy as np
import copy,sys

def solve_game(board_config):
	[location, current_board, visited] = board_config
	if location == -1:
		return False
	global path, final_board
	if location == game['end']:
		final_board = current_board
		return True
	c1 = copy.deepcopy(current_board)
	v1 = copy.deepcopy(visited)
	if solve_game(moveLeft(location, c1,v1)) :
		path += ["L"]
		return True
	c2 = copy.deepcopy(current_board)
	v2 = copy.deepcopy(visited)
	if solve_game(moveRight(location,c2,v2)):
		path += ["R"]
		return True
	c3 = copy.deepcopy(current_board)
	v3 = copy.deepcopy(visited)
	if solve_game(moveUp(location, c3,v3)):
		path += ['U']
		return True
	c4 = copy.deepcopy(current_board)
	v4 = copy.deepcopy(visited)
	if solve_game(moveDown(location, c4, v4)):
		path += ["D"]
		return True
	return False


def moveLeft(loc, cb, vis):
	[r,c] = loc
	standing = isStanding(loc, cb)
	cannotMove = [-1,0,0]
	h = cb[r,c]
	if c-1 <0:
		return cannotMove
	if not standing and (cb[r,c-1] == 0 or vis[r,c-1]==1):
		return cannotMove
	elif cb[r,c-1] !=0 and vis[r,c-1]==0: 
		new_loc = [r,c-1]
		vis[r,c-1] = 1
		return [new_loc, cb, vis]
	elif standing and sum(cb[r,(c-h):c]) == 0 and c-h>=0:
		vis = np.zeros(vis.shape)
		vis[r,c-1] = 1
		[new_board, new_loc] = topple(loc, cb, 0)
		return [new_loc, new_board, vis]
	else:
		return cannotMove

def moveRight(loc, cb, vis):
	[r,c] = loc
	h = cb[r,c]
	standing = isStanding(loc, cb)
	cannotMove = [-1,0,0]
	[rows,cols] = cb.shape
	if c+1 >= cols:
		return cannotMove
	if not standing and (cb[r,c+1] == 0 or vis[r,c+1]==1):
		return cannotMove
	elif cb[r,c+1] !=0 and vis[r,c+1]==0: #there's a create and it hasn't been visited
		new_loc = [r,c+1]
		vis[r,c+1] = 1
		return [new_loc, cb, vis]
	#you're on a standing crate and there's room for it to fall
	if standing and c+h<cols and sum(cb[r,(c+1):(c+h+1)]) == 0: 
			vis = np.zeros(vis.shape) #board changed so reset visited board
			vis[r,c+1] = 1
			[new_board, new_loc] = topple(loc, cb, 1) #topple to the right
			return [new_loc, new_board, vis]
	else:
		#print 'none of the move conditions were met'
		return cannotMove

def moveUp(loc, cb, vis):
	#print 'trying to move upwards'
	[r,c] = loc
	h = cb[r,c]
	standing = isStanding(loc, cb)
	cannotMove = [-1,0,0]
	[rows,cols] = cb.shape
	if r-1 < 0:
		return cannotMove
	if not standing and (cb[r-1,c] == 0 or vis[r-1,c]==1):
		#print 'nothing above or already visited'
		return cannotMove
	elif cb[r-1,c] !=0 and vis[r-1,c]==0: 
		new_loc = [r-1,c]
		vis[r-1,c] = 1
		return [new_loc, cb, vis]
	#you're on a standing crate and there's room for it to fall
	elif standing and sum(cb[r-h:r,c]) == 0 and r-h>=0: 
		vis = np.zeros(vis.shape) #board changed so reset visited board
		vis[r-1,c] = 1
		[new_board, new_loc] = topple(loc, cb, 2) #topple up
		return [new_loc, new_board, vis]
	else:
		return cannotMove

def moveDown(loc, cb, vis):
	[r,c] = loc
	h = cb[r,c]
	standing = isStanding(loc, cb)
	cannotMove = [-1,0,0]
	[rows,cols] = cb.shape
	if r+1 >= rows:
		return cannotMove
	if not standing and (cb[r+1,c] == 0 or vis[r+1,c]==1):
		return cannotMove
	elif cb[r+1,c] !=0 and vis[r+1,c]==0: #there's a crate below you and it hasn't been visited
		new_loc = [r+1,c]
		vis[r+1,c] = 1
		return [new_loc, cb, vis]
	#you're on a standing crate and there's room for it to fall
	elif standing and sum(cb[r+1:(r+h+1),c]) == 0 and r+h<rows: 
		vis = np.zeros(vis.shape) #board changed so reset visited board
		vis[r+1,c] = 1
		[new_board, new_loc] = topple(loc, cb, 3) #topple to the right
		return [new_loc, new_board, vis]
	else:
		return cannotMove



#check to see if the current location is standing
#return True if yes, False if no
def isStanding(location, current_board):
	[r,c] = location
	return current_board[r,c] > 1

#topple
#error checking has been completed before calling topple
#copies the board
def topple(location, current_board, direction):
	[r,c] = location
	h = current_board[r,c]
	new_board = copy.deepcopy(current_board)
	new_board[r,c] = 0
	if direction == 0:
		new_board[r,c-h:c] = 1
		new_location = [r,c-1]
	elif direction == 1:
		new_board[r,c+1:c+h+1] = 1
		new_location = [r,c+1]
	elif direction == 2:
		new_board[r-h:r, c] = 1
		new_location = [r-1,c]
	elif direction == 3:
		new_board[r+1:r+h+1, c] = 1
		new_location = [r+1,c]
	return [new_board, new_location]

"""
This section of the code is for reconstructing the json format after
the correct path and final board layout have already been determined
"""
def return_json_board(start, board, path):
	vis = np.zeros(board.shape)
	last = start
	for move in path:
		old_board = copy.deepcopy(board)
		old_pos = copy.deepcopy(last)
		if move == 'L':
			[last, board, vis] = moveLeft(last, board, vis)
		elif move == 'R':
			[last, board, vis] = moveRight(last, board, vis)
		elif move == 'U':
			[last, board, vis] = moveUp(last, board, vis)
		elif move == 'D':
			[last, board, vis] = moveDown(last, board, vis)
		if not np.array_equal(old_board, board):
			height = remove_from_standing(old_pos)
			add_to_toppled(old_pos, move, height)
	
def remove_from_standing(pos):
	[r,c] = pos
	for cr in game['standing_crates']:
		if cr[0] == r and cr[1] == c:
			game['standing_crates'].remove(cr)
			return cr[2]

def add_to_toppled(pos, direction, h):
	[r,c] = pos
	if direction == 'L': game['toppled_crates'].append([r, c-h, r,c-1])
	elif direction == 'R': game['toppled_crates'].append([r, c+1,r,c+h])
	elif direction == 'U': game['toppled_crates'].append([r-h, c,r-1,c])
	elif direction == 'D':game['toppled_crates'].append([r+1, c,r+h,c]) 

if __name__ == "__main__":
	game_num = raw_input('Which game would you like to run? ')
	game_directory = "sample_games/"
	fn = "sample_game" + game_num
	try:
		with open(game_directory+fn,'r') as g:
			game = json.loads(g.read())
	except:
		print "Couldn't find " + fn
		sys.exit()

	print 'Now solving ' + fn
	#Do some initialization
	board = np.zeros(game['board'])
	path = []
	visited = np.zeros(game['board'])
	for cr in game['standing_crates']:
		[r,c,h] = cr
		board[r,c] = h
	[r1,c1] = game['end']
	board[r1,c1] = 1
	start = game['start']
	solve_game([start,board,visited])
	
	#Global variable path contains the Keystrokes you'd have to press to get to the End in Reverse Order
	correct_path = path[::-1]
	return_json_board(start, board, correct_path)
	answer_directory = "../answers/"
	answer_file =  answer_directory+'board' + str(game_num) + "_solution.json"
	try:
		with open(answer_file, 'w') as f:
			f.write(json.dumps(game))
	except:
		print "Could not write to the answers directory"
		sys.exit()
