from kung_fu2 import *
import simplejson as json
import numpy as np


def test_can_move():
	start = [4,2]
	down = 3
	#should not be able to move down
	print canMove(start,board,0,visited) == False
	print canMove(start,board,1,visited) == False
	print canMove(start,board,2,visited) == False
	print canMove(start,board,3,visited) == False
	
	print canFall(start,board,0) ==True
	print canFall(start,board,1) == True
	print canFall(start,board,2) == True
	print canFall(start,board,3) == False

	print isStanding(start, board) == True
	print isStanding([0,0], board) == False
	print isStanding([3,4], board) == True

def test_topple():
	print 'Testing a sequence of topples and moves'
	start = [4,2]
	middle = [3,4]

	[board_left, new_left] = topple(start,board,0)
	#print board_left
	print new_left == [4,1]
	[board_right, new_right] = topple(start,board,1)
	#print board_right
	print new_right == [4,3]

	[board_up, new_up] = topple(start,board,2)
	#print board_up
	print new_up == [3,2]
	print canFall(start,board,3) == False

	print canMove(new_left, board_left, 0, visited) == True
	print canMove(new_left, board_left, 3, visited) == False
	print canMove(new_left, board_left, 2, visited) == False
	
	nl2 = moveOne(new_left, board_left, 0)
	print nl2 == [4,0]
	print canMove(nl2, board_left,0, visited) == False
	print canMove(nl2, board_left,1, visited) == True
	print canMove(nl2, board_left,2, visited) == False
	print canMove(nl2, board_left,3, visited) == False
	print board_left

def test_win():
	print 'testing the sequences of winning moves'
	start = game['start']
	[b1, n1 ] = topple(start,board,1)
	new_pos = moveOne(n1,b1,1)
	new_pos = moveOne(new_pos,b1,2)
	print new_pos
	[b2,n1] = topple(new_pos,b1,0)
	print b2
	for j in range(3):
		n1= moveOne(n1,b2,0)
		print n1
		print b2
		print "-"*20
	print canMove(n1,b2,0,visited) == False
	print canMove(n1,b2,1,visited) == True
	print canMove(n1,b2,2,visited) == True
	print canMove(n1,b2,3,visited) == False
	
	res = moveOne(n1,b2,2)
	
	#THIS SHOULD NOT BE ALLOWED!
	print canMove(res,b2,1,visited) == False
	print moveOne(res,b2,1)
	[b3,n2] = topple(res,b2,1)
	print b3
	print n2
	print 'above should be 2,1'
	#Now move 2 spaces to the right
	n3 = moveOne(n2,b3,1)
	n4 = moveOne(n3,b3,1)
	n5 = moveOne(n4,b3,2) #moveUp
	print b3
	print n5
	print 'should say 1,3'
	[b4,n6] = topple(n5,b3,0)
	n8 = moveOne(n6,b4,0)
	print b4
	print n8
	print 'should say 1,1 above'
	cur_pos = moveOne(n8, b4,2) #moveUP
	print canFall(cur_pos,b4,1) == True
	[b5,n9] = topple(cur_pos,b4,1)
	print b5
	fin = moveOne(moveOne(n9,b5,1),b5,1)
	print fin

	





if __name__ == "__main__":
	fn = 'sample_game'
	game = json.loads(open(fn, 'r').read())
	board = np.zeros(game['board'])
	visited = np.zeros(game['board'])
	for cr in game['standing_crates']:
		[r,c,h] = cr
		board[r,c] = h
	print board
	#RUN SOME TESTS
	test_can_move()
	test_topple()
	test_win()
