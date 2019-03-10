"""
TODO:: 
- interface between this and other datastructure
- pretty print to demo format and write to file
- recycled moves
"""
import math, random, copy

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

WIDTH = 2
HEIGHT = 12
GRID = []																					# 1D board representation - each element is a cell object
MAX_PLAYER = 'colour'
MIN_PLAYER = 'dot'
TREE_HEIGHT = 3																			# depth/height, doesn't include root node
NUM_CHILDREN = len(ROTATION) * WIDTH														# 8 rotations * maximum number of legal cells
MAX_LEAVES = int(math.pow(NUM_CHILDREN, TREE_HEIGHT))										# number of nodes with a value
MAX_NODES = int((math.pow(NUM_CHILDREN, TREE_HEIGHT + 1) - 1 ) / ( NUM_CHILDREN - 1 ))		# total calculated nodes of tree
TREE_ARRAY = [math.nan] * MAX_NODES																# k-ary array
ROOT_BOARD = []

# # #							# # #
# # #  Board manipulation code 	# # #
# # #							# # #	
def getLegalCells(board_state):
	legal_cells = []
	for cell in range(len(board_state) - 1):						
		# cell has been played, check above
		if board_state[cell]['colour'] == 'R' or board_state[cell]['colour'] == 'W':
			if cell + WIDTH <= len(board_state) - 1:
				if board_state[cell + WIDTH]['colour'] != 'R' and board_state[cell + WIDTH]['colour'] != 'W':				
					legal_cells.append(cell+WIDTH)
			
		# cell is in first row
		elif cell <= WIDTH:			
			if board_state[cell + WIDTH]['colour'] != 'R' or board_state[cell + WIDTH]['colour'] != 'W':
				legal_cells.append(cell)				

	# double check to remove unnecessary values
	for c in legal_cells:
		if (c + WIDTH) in legal_cells:
			legal_cells.remove(c + WIDTH)

	return legal_cells

def setWidth(width):
	WIDTH = width

def setHeight(height):
	HEIGHT = height

# missing recycled move code
def addMoveToBoard(parent_board, move, legal_cells):
		board = copy.deepcopy(parent_board)
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
		if(column > WIDTH or column < 0 or row > HEIGHT or row < 0):
			#print('[Illegal] Move out of bounds')
			return False

		# determine placement in array
		index = column + (row * WIDTH)

		# check empty cell
		if(board[index]['colour'] == 'R' or board[index]['colour'] == 'W'):
			#print('[Illegal] Cell Occupied')
			return False

		# if in legal cells
		if( index not in legal_cells):
			#print('[Illegal] not in legal cells')
			return False


		# Get cell attributes of rotation type
		C1 = ROTATION[rotation]['C1']
		C2 = ROTATION[rotation]['C2']
		link = ROTATION[rotation]['link']

		# determine index of link cell
		if (link is	'up'):
			link = index + WIDTH
			if(link >= (WIDTH * HEIGHT)):				
				#print('[Illegal] Link above can\'t play')
				return False
		else:
			link = index + 1
			if(link >= (WIDTH * (row+1))):
				#print('[Illegal] LINK out of row bounds')
				return False

			elif( ( link )not in legal_cells):		# prev link + 1?
				#print('[Illegal] link right not legal')
				return False

		# updateLegalCells(legal_cells, index, link)
		if ROTATION[rotation]['link'] == 'right':			
			updateCell( board ,index, C1['colour'], C1['dot'], link, '>' )  
			updateCell( board, link, C2['colour'], C2['dot'], index, '<' )
		elif ROTATION[rotation]['link'] == 'up':
			updateCell( board, index, C1['colour'], C1['dot'], link, '^' )
			updateCell( board, link, C2['colour'], C2['dot'], index, 'v' )
		return board

def updateCell(board, cell, colour, dot, link, link_direction):
	board[cell]['colour'] = colour
	board[cell]['dot'] = dot
	board[cell]['link'] = link
	board[cell]['link_direction'] = link_direction

def displayBoard(board):
	display_height = 1
	for i in range(WIDTH):
		print(' _ _ _', end='')
	print()

	output = []
	string = ''
	# board
	for i in range(len(board)): 
		link_direction = '.' if str(board[i]['link_direction']) == '' else str(board[i]['link_direction'])
		colour = '.' if str(board[i]['colour']) == '' else str(board[i]['colour'])
		dot = '.' if str(board[i]['dot']) == '' else str(board[i]['dot'])
		string += "|"+ link_direction + colour + dot + link_direction +"|" 			
		
		# newline at width length
		if(math.ceil(i % WIDTH) is WIDTH-1):
			string += str(display_height)
			output.append(string)
			string = ''
			
			display_height += 1
	
	# display right-side-up				
	for line in range(len(output),0,-1):
		print(output[line-1])

	# column names 
	for i in range(WIDTH):
		print('  '+ COLUMNS[i] +'   ',end='')
	print('')


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
		MAX_PLAYER = 'dot'
		MIN_PLAYER = 'colour'

# TODO:: return heuristical value based on test heuristic
def calculateHeuristic(board_state):
	score = 0

	for index,cell in enumerate(board_state):
		column = index % (WIDTH) +1
		row = ((int) (index /(WIDTH)))
		coordinates = int(str(row) + str(column))
		if cell['colour'] == 'R':
			if cell['dot'] == 'C':
				score -= 1.5*coordinates
			if cell['dot'] == 'F':
				score -= 2*coordinates
		elif cell['colour'] == 'W':
			if cell['dot'] == 'C':
				score += coordinates
			if cell['dot'] == 'F':
				score += 3*coordinates
		else:
			continue

	return score
	
# Creates a 1D k-ary tree based on TREE_HEIGHT and NUM_CHILDREN per node
# Tree is build DEPTH FIRST
def buildTree(depth, parent_index, board_state = False, legal_cells = False):
	# not at leaf node	
	if depth is not TREE_HEIGHT:						

		# contents of parent node - 0 is not appropriate placeholder	 
		TREE_ARRAY[parent_index] = 0		
		
		# testing algorithm
		# Uncomment this and comment out production section
		"""
		for c in range(NUM_CHILDREN):
			child_index = NUM_CHILDREN * parent_index + c + 1

			# go to child node
			buildTree(depth + 1, child_index)
		
		"""

		### production algorithm 
		child_index_count = 0
		for index in legal_cells:														
			for r in ROTATION:
				child_index = NUM_CHILDREN * parent_index + child_index_count + 1

				new_move = {
					'column' : index % WIDTH,
					'row' : math.floor( index / WIDTH),
					'rotation' : r
				}
				
				# returns new board if legal, False bool if illegal
				new_board = addMoveToBoard(board_state, new_move, legal_cells)			

				# display board after legal play
				"""
				if new_board is not False:						
					print('playing move: '+str(new_move))					
					#print('child board')
					displayBoard(new_board)
				"""

				if new_board != False:													
					child_index_count += 1
					new_legal_cells = getLegalCells(new_board)

					# immediately follow child subtree						
					buildTree( depth + 1, child_index, new_board, new_legal_cells )
				
				# make subtree unavailable
				else:										
					child_index_count += 1			

					# buildTree(depth + 1, child_index, copy.deepcopy(board_state), copy.deepcopy(legal_cells))
					
					# 0 is not an appropriate placeholder
					TREE_ARRAY[child_index] = math.nan															
	
	# at leaf node 
	else:
		heuristic = calculateHeuristic(board_state)
		TREE_ARRAY[parent_index] = heuristic
		

# Pretty prints tree
def printTree(depth, parent_index):
	if depth is not TREE_HEIGHT:
		for k in range(depth):
			print('\t',end='')
		print('Parent['+str(parent_index)+']: '+str(TREE_ARRAY[parent_index]))
		for c in range(NUM_CHILDREN):
			for i in range(depth):
				print('\t',end='')
			child_index = NUM_CHILDREN * parent_index + c + 1
			print('\tChild['+str(child_index)+']: '+str(TREE_ARRAY[child_index]))
			printTree(depth + 1, child_index)
	else:
		# nothing to do
		return 

# returns value of leaf root node
def minMax(depth, parent_index, show_stats=False):
	stats = ""
	if depth is not TREE_HEIGHT:
		
		# odd == MIN_PLAYER, (1,3,5...)
		if (depth % 2) > 0:
			node_value = math.inf
			
			# check value of each child
			for c in range(NUM_CHILDREN):
				
				child_index = NUM_CHILDREN * parent_index + c + 1
				child_value = minMax(depth + 1, child_index, show_stats)
				if math.isinf(node_value) and not math.isnan(child_value):
					node_value = child_value
				node_value = min(node_value, child_value)

			for n in range(depth):
				stats += '\t'
			stats += '(-) for node ['+str(parent_index)+'] = ['+str(node_value)+']'
			if show_stats:
				print(stats)

			return node_value

		# even == MAX_PLAYER, (0,2,4...)
		else:
			node_value = -math.inf
			
			# check value of each child
			for c in range(NUM_CHILDREN):			
				
				child_index = NUM_CHILDREN * parent_index + c + 1
				child_value = minMax(depth + 1, child_index, show_stats)
				if math.isinf(node_value) and not math.isnan(child_value):
					node_value = child_value
				node_value = max(node_value, child_value)			

			for n in range(depth):
				stats += '\t'
			stats += '(+) for node ['+str(parent_index)+'] = ['+str(node_value)+']'
			
			if show_stats:
				print(stats)
				
			return node_value

	# terminal node, return value
	else:		
		node_value = TREE_ARRAY[parent_index]
		return node_value

def interfaceBoard(board_state):
	return board_state.copy()

def getNextMove(board_state, show_trace=False, show_stats=False):
	root_board = interfaceBoard(board_state)
	legal_cells = getLegalCells(root_board)

	buildTree(0, 0, root_board, legal_cells)

	if show_trace == True:
		print(printTree(0,0))

	root_score = minMax(0,0,show_stats)
	print(root_score)

	if show_stats == True:
		# meta stats
		print('\n'+str(TREE_ARRAY)+'\n')
		print('',end="\n**************\n")
		print('Dimensions', end=': ')
		print(str(WIDTH)+' '+str(HEIGHT))
		print('Board Cells', end=': ')
		print(str(WIDTH * HEIGHT))
		print('Depth', end=': ')
		print(str(TREE_HEIGHT))
		print('Children per node', end=': ')
		print(NUM_CHILDREN)
		print('Max nodes', end=': ')
		print(MAX_NODES)
		print('Max leaves', end=': ')
		print(MAX_LEAVES)
		print('Parent Nodes', end=': ')
		print(MAX_NODES - MAX_LEAVES)
		print('Length of tree', end=': ')
		print(len(TREE_ARRAY))

	return root_score

print('\n*****MIN MAX TESTS****')
test_board = []
for n in range(WIDTH * HEIGHT):
	cell = {
		"colour": '',
		"dot": '',
		"link": '',
		"link_direction": ''
	}
	test_board.append(cell)

# populate tree
getNextMove(test_board)


