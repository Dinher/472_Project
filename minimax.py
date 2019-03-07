"""
*Make sure max player is set before running minmax - defaults to colour*

# each cell of the board array is a cell object with attributes
self.colour = 	'R' or 'W'					
self.dot = 		'F' or 'C'				
self.link = 	cell_index + 1 or cell_index + board_width
self.link_direction = directional symbol, set but unused here

TODO:: 
- create array of legal cells from root board 
- hardcode/create function to return sample heuristical value
- caclulate heuristic value of given board state
- add heuristical value to leaf node
- turn into class
"""

from game2 import Game
import math, random

WIDTH = 4
HEIGHT = 4
DEPTH = 3
GRID = []																					# 1D board representation - each element is a cell object
MAX_PLAYER = 'colour'
MIN_PLAYER = 'dot'
TREE_HEIGHT = 3 																			# depth/height, doesn't include root node
NUM_CHILDREN = 3 # len(ROTATION) * WIDTH													# 8 rotations * board width
MAX_LEAVES = int(math.pow(NUM_CHILDREN, TREE_HEIGHT))										# number of nodes with a value
MAX_NODES = int((math.pow(NUM_CHILDREN, TREE_HEIGHT + 1) - 1 ) / ( NUM_CHILDREN - 1 ))		# total calculated nodes of tree
TREE_ARRAY = [None] * MAX_NODES																# k-ary array
ROOT_BOARD = []
LEGAL_CELLS = []
ROTATION = {
	1: {
		'C1' : {'colour':'R','dot':'F'},
		'C2' : {'colour':'W','dot':'C'},
		'link': 'right'
	},
	2: {
		'C1' : {'colour':'W','dot':'C'},
		'C2' : {'colour':'R','dot':'F'},
		'link': 'up'
	},
	3:{
		'C1' : {'colour':'W','dot':'C'},
		'C2' : {'colour':'R','dot':'F'},
		'link': 'right'
	},
	4:{
		'C1' : {'colour':'R','dot':'F'},
		'C2' : {'colour':'W','dot':'C'},
		'link': 'up'
	},
	5:{
		'C1' : {'colour':'R','dot':'C'},
		'C2' : {'colour':'W','dot':'F'},
		'link': 'right'
	},
	6:{
		'C1' : {'colour':'W','dot':'F'},
		'C2' : {'colour':'R','dot':'C'},
		'link': 'up'
	},
	7:{
		'C1' : {'colour':'W','dot':'F'},
		'C2' : {'colour':'R','dot':'C'},
		'link': 'right'
	},
	8:{
		'C1' : {'colour':'R','dot':'C'},
		'C2' : {'colour':'W','dot':'F'},
		'link': 'up'
	}
}
COLUMNS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# # #							# # #
# # #  Board manipulation code 	# # #
# # #							# # #	
def setBoard(board):
	ROOT_BOARD = board
	setLegalCells(ROOT_BOARD)

# TODO:: return array of legal cells/index vales
def getLegalCells(board_state):
	# umm... how?
	legal_cells = False
	return legal_cells

def setWidth(width):
	WIDTH = width

def setHeight(height):
	HEIGHT = height

# missing recycled move code
def addMoveToBoard(grid, move, legal_cells):
		board = grid.copy()
		column = move['column']
		row = move['row']
		rotation = move['rotation']

		# check last move played for RECYCLED moves
		"""
		if IS_RECYCLED_GAME:
			last_move = list(MOVE_HISTORY.items())[-1][1]
			if last_move['column'] == column and last_move['row'] == row and last_move['rotation']:
				return False
		"""

		# check bounds
		# This required for the AI?
		if(column > WIDTH or column < 1 or row > HEIGHT or row < 1):
			return False

		# determine placement in array
		index = (column - 1) + ((row - 1) * WIDTH)

		# check empty cell
		if(board[index].colour == 'R' or board[index].colour == 'W'):
			return False

		# check if move is 1st row or over other tiles
		if((index + 1) not in legal_cells):
			return False

		# Get cell attributes of rotation type
		C1 = ROTATION[rotation]['C1']
		C2 = ROTATION[rotation]['C2']
		link = ROTATION[rotation]['link']

		# determine index of link cell
		if (link is	'up'):
			link = index + self.width
			if(link >= (self.width * self.height)):				
				return False
		else:
			link = index + 1
			if(link >= (WIDTH * row)):
				return False

			elif((link+1)not in legal_cells):
				return False

		updateLegalCells(legal_cells, index, link)
		if ROTATION[rotation]['link'] == 'right':			
			updateCell( board ,index, C1['colour'], C1['dot'], link, '>' )  
			updateCell( board, link, C2['colour'], C2['dot'], index, '<' )
		elif ROTATION[rotation]['link'] == 'up':
			updateCell( board, index, C1['colour'], C1['dot'], link, '^' )
			updateCell( board, link, C2['colour'], C2['dot'], index, 'v' )
		return board

def updateCell(board, cell, colour, dot, link, link_direction):
	board[cell].colour = colour
	board[cell].dot = dot
	board[cell].link = link
	board[cell].link_direction = link_direction

def displayBoard(board):
	display_height = 1
	for i in range(WIDTH):
		print(' _ _ _', end='')
	print()

	output = []
	string = ''
	# board
	for i in range(len(board)): 
		string += "|"+ board[i].link_direction + str(board[i].colour) + str(board[i].dot) + board[i].link_direction +"|" 			
		
		# newline at width length
		if(math.ceil(i % WIDTH) is WIDTH-1):
			# print(str(display_height))
			string += str(display_height)
			output.append(string)
			string = ''
			
			display_height += 1
	
	# display right-side-up				
	for line in range(len(output),0,-1):
		print(output[line-1])

	# column names 
	for i in range(WIDTH):
		#print(' '+COLUMNS[i]+'  ',end='')
		print('  '+ COLUMNS[i] +'   ',end='')
	print('')

def updateLegalCells(legal_cells, index, link):
	legal_cells.remove(index + 1)				# remove previous index from list
	legal_cells.append(index + WIDTH + 1) 		# cell above is now legal, add to list
	legal_cells.remove(link + 1)				# remove previous link from list
	legal_cells.append(link + WIDTH + 1) 		# cell above is now legal, add to list
	legal_cells.sort()

	# clear score data if not a legal cells
	TEMP_SCORES = legal_cell_score.copy()
	for cell in TEMP_SCORES:
		if cell not in legal_cells:
			legal_cell_score.pop(str(cell),None)
	
	# add new legal cells to scores
	for cell in legal_cells:	
		if str(cell) not in legal_cell_score: 
			legal_cell_score[str(cell)] = {
				'R': 0,
				'W': 0,
				'F': 0,
				'C': 0
			}


# # #			# # #
# # #  MiniMax	# # #
# # #			# # #
def setTreeHeght(height):
	TREE_HEIGHT = height
	
def setMaxPlayer(player_type):
	if player_type == 'colour':
		MAX_PLAYER = 'colour'
		MIN_PLAYER = 'dot'
	else:
		MAX_PLAYER = 'dor'
		MIN_PLAYER = 'colour'

# TODO:: return heuristical value based on test heuristic
def calculateHeuristic(board_state):
	heuristic = random.randint(-10,10)
	return heuristic

# Creates a 1D k-ary tree based on TREE_HEIGHT and NUM_CHILDREN per node
def buildTree(depth, parent_index, board_state = False, legal_cells = False):
	# not at leaf node
	if depth is not TREE_HEIGHT:														# if depth is not TREE_HEIGHT and board_state is not False:						
		# contents of parent node - placeholder value before minmax algorithm
		TREE_ARRAY[parent_index] = math.inf

		# testing algorithm
		for c in range(NUM_CHILDREN):
			child_index = NUM_CHILDREN * parent_index + c + 1

			# go to child node
			buildTree(depth + 1, child_index)

		"""
		### production algorithm - UNTESTED
		child_index_count = 0
		for index in LEGAL_CELLS:														# 8 rotations * 8 legal cells = 64 children per board state   O_O
			for r in ROTATION:
				child_index = NUM_CHILDREN * parent_index + child_index_count + 1

				new_move = {
					'column' : index % WIDTH,
					'row' : math.ceil(index/self.width),
					'rotation' : r
				}
				
				new_board = addMoveToBoard(board_state, new_move, legal_cells)
				
				if new_board is not False:												# ie. move is legal
					child_index_count += 1
					new_legal_cells = getLegalCells(new_board)
					buildTree( depth + 1, child_index, new_board, new_legal_cells )
				else:
					# subtree is unavailable
					# make this cell value None? or continue tree?
					child_index_count += 1
					build(depth + 1, child_index)
		"""
	
	# at leaf node 
	else:
		TREE_ARRAY[parent_index] = calculateHeuristic(board_state)
		return 

# Pretty prints tree
def printTree(depth, parent_index):
	if depth is not TREE_HEIGHT:
		for k in range(depth):
			print('\t',end='')
		print('Parent: '+str(TREE_ARRAY[parent_index]))
		for c in range(NUM_CHILDREN):
			for i in range(depth):
				print('\t',end='')
			child_index = NUM_CHILDREN * parent_index + c + 1
			print('\tChild: '+str(TREE_ARRAY[child_index]))
			printTree(depth + 1, child_index)
	else:
		# nothing to do
		return 

# returns value of leaf root node
def minMax(depth, parent_index):
	if depth is not TREE_HEIGHT:
		
		# odd == MIN_PLAYER, (1,3,5...)
		if (depth % 2) > 0:
			node_value = math.inf
			
			# check value of each child
			for c in range(NUM_CHILDREN):
				child_index = NUM_CHILDREN * parent_index + c + 1
				node_value = min(node_value, minMax(depth + 1, child_index))
			print('(-) for node ['+str(parent_index)+'] = ['+str(node_value)+']')
			return node_value

		# even == MAX_PLAYER, (0,2,4...)
		else:
			node_value = -math.inf
			
			# check value of each child
			for c in range(NUM_CHILDREN):
				child_index = NUM_CHILDREN * parent_index + c + 1
				node_value = max(node_value, minMax(depth + 1, child_index))
			print('(+) for node ['+str(parent_index)+'] = ['+str(node_value)+']')
			return node_value

	# terminal node, return value
	else:
		return TREE_ARRAY[parent_index]



### Tests
g = Game(WIDTH, HEIGHT, 'colour')

g.move(1,1,1)
g.display()

grid = g.getGrid()

legal_cells =g.getLegalCells()
legal_cell_score = g.getLegalCellScore()
player_scores = g.getPlayerScores()

new_move = {
	'column' : 3,
	'row' : 1,
	'rotation' : 1
}

new_board = addMoveToBoard(grid, new_move, legal_cells)
if new_board is not False:
	displayBoard(new_board)
print("\nLegal Cells:")
print(legal_cells)
print()
g.showGrid()
print('\n*****MIN MAX TESTS****')

# populate tree
buildTree(0,0)

# meta stats
print('Max nodes')
print(MAX_NODES)
print('Max leaves')
print(MAX_LEAVES)
print('length of list')
print(len(TREE_ARRAY))

# pretty print tree
printTree(0,0)

# view raw list
print(TREE_ARRAY)

# value of root node
print('Root score: '+str(minMax(0,0)))
