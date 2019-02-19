import random,math

HEIGHT = 12
WIDTH = 8

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

# Place into Game class
MOVE_HISTORY = {}
MOVE_COUNT = 0			# 60 == tie
MAX_NUM_MOVES = 60
TILES_REMAINING = 8
RECYCLED = False
LEGAL_CELLS = []
ILLEAGAL_MOVE = False
VERBOSE = {
	'check': 	False,
	'meta': 	False
}

def history():
	print('\n**Game History**')
	count = 1
	for i in MOVE_HISTORY:
		m = MOVE_HISTORY[i]
		print('['+str(count)+']: Col.'+str(m['column'])+' Row.'+str(m['row'])+' Rot.'+str(m['rotation']))
		count += 1

def metaStats():
	print('Dimensions: '+str(WIDTH)+'x'+str(HEIGHT))
	print('Total Cells: '+str(WIDTH * HEIGHT))
	print('Legal Cells: '+str(LEGAL_CELLS))
	print('Tiles Remaining: '+str(TILES_REMAINING))
	print('Moves Remaining: '+str(MAX_NUM_MOVES - MOVE_COUNT))
	if ILLEAGAL_MOVE:
		print('**Next illegal play is a game over**')
	if RECYCLED:
		print('**Recycled Tiles Only**')

class Cell:
	def __init__(self, colour = '·', dot = '·', link = '·', link_direction = '·'):
		self.colour = colour	
		self.dot = dot				
		self.link = link
		self.link_direction = link_direction

class Board:
	def __init__(self,height = 12,width = 8):
		self.height = height
		self.width = width
		self.grid = []
		self.total_cells = height * width
		self.win_state = False

	def initGrid(self):
		global LEGAL_CELLS
		for n in range(self.total_cells):
			self.grid.append(Cell())		
		for i in range(self.width):
			LEGAL_CELLS.append(i+1)

	def updateCell(self,cell,colour,dot,link, link_direction):
		self.grid[cell].colour = colour
		self.grid[cell].dot = dot
		self.grid[cell].link = link
		self.grid[cell].link_direction = link_direction

	def display(self):
		global COLUMNS
		display_height = 1
		# top
		for i in range(self.width):
			print(' _ _ _', end='')
		print()

		output = []
		string = ''
		# board
		for i in range(self.total_cells): 
			# print("|_" + str(self.grid[i].colour) + str(self.grid[i].dot) + "_|", end='')
			#print("|"+str(self.grid[i].link)+"|", end='')
			string += "|"+ self.grid[i].link_direction + str(self.grid[i].colour) + str(self.grid[i].dot) + self.grid[i].link_direction +"|" 			
			
			# newline at width length
			if(math.ceil(i % self.width) is self.width-1):
				# print(str(display_height))
				string += str(display_height)
				output.append(string)
				string = ''
				
				display_height += 1
		
		# display right-side-up				
		for line in range(len(output),0,-1):
			print(output[line-1])

		# column names 
		for i in range(self.width):
			#print(' '+COLUMNS[i]+'  ',end='')
			print('  '+ COLUMNS[i] +'   ',end='')
		print('')

	# prints out contents of grid array
	def showGrid(self):
		for i in range(self.total_cells):
			print('CELL['+str(i)+']: '+str(self.grid[i].colour)+" "+str(self.grid[i].dot)+" link:"+str(self.grid[i].link))

	def move(self, column, row, rotation):
		global ILLEAGAL_MOVE
		if(rotation < 1 or rotation > 8):
			print('\n**Illegal move**: not rotation type')			
			return False			

		# check bounds
		if(column > self.width or column < 1 or row > self.height or row < 1):
			print('\n**Illegal move**: Out of bounds')			
			return False

		# determine placement in array
		index = (column - 1) + ((row - 1) * self.width)

		# check empty cell
		if(self.grid[index].colour == 'R' or self.grid[index].colour == 'W'):
			print('\n**Illegal move**: Cell already played')
			return False

		# check if move is 1st row or over other tiles
		if((index + 1) not in LEGAL_CELLS):
			print('\n**Illegal move**: Playing in illegal cell '+str(index)+' '+str(index+1))
			return False

		# Get cell attributes of rotation type
		C1 = ROTATION[rotation]['C1']
		C2 = ROTATION[rotation]['C2']
		link = ROTATION[rotation]['link']

		# determine index of link cell
		if (link is	'up'):
			link = index + self.width
			if(link >= (self.width * self.height)):
				print('\n**Illegal move**: link cell out of bounds [Above]')
				print('index: '+str(index)+' '+str(link))
				return False
		else:
			link = index + 1
			if(link >= (self.width * row)):
				print('\n**Illegal move**: link cell out of bounds [Right]')
				print('index: '+str(index)+' '+str(link))
				return False

			elif((link+1)not in LEGAL_CELLS):
				print('\n**Illegal move**: link cell overhangs')
				print('index: '+str(index)+' '+str(link))
				return False

		self.updateLegalCells(index,link)
		# adds arrows to link
		# ↖ ↑ ↗
		# ← · →
		# ↙ ↓ ↘
		if ROTATION[rotation]['link'] == 'right':			
			self.updateCell( index, C1['colour'], C1['dot'], link, '>' )  
			self.updateCell( link, C2['colour'], C2['dot'], index, '<' )
		elif ROTATION[rotation]['link'] == 'up':
			self.updateCell( index, C1['colour'], C1['dot'], link, '^' )
			self.updateCell( link, C2['colour'], C2['dot'], index, 'v' )
		return True
	

class Game(Board):
	def __init__(self, height, width, turn = 'colour'):
		Board.__init__(self,height, width)
		self.initGrid()
		self.display()
		self.turn = turn
	
	def getTurn(self):
		return self.turn

	def updateGameMeta(self, column, row, rotation):
		global MOVE_HISTORY, MOVE_COUNT, TILES_REMAINING, RECYCLED
		MOVE_HISTORY[MOVE_COUNT] = {
				'column':column,
				'row': row,
				'rotation': rotation
		}
		MOVE_COUNT += 1
		TILES_REMAINING -= 1
		if TILES_REMAINING == 0:
			print('NO TILES REMAINING')
			RECYCLED = True

	# Legal cells are conceptually cells at the top-most row of tiles
	# '+ 1' ignores index[0] for consistency sake
	def updateLegalCells(self,index,link):
		global LEGAL_CELLS, RECYCLED
		LEGAL_CELLS.remove(index + 1)				# remove previous index from list
		LEGAL_CELLS.append(index + self.width + 1) 	# cell above is now legal, add to list
		LEGAL_CELLS.remove(link + 1)				# remove previous link from list
		LEGAL_CELLS.append(link + self.width + 1) 	# cell above is now legal, add to list
		# removed the tiles from the game
		# update legal cells
		# for next move check to see if its exact as what last move was
		if RECYCLED:
			for cell in LEGAL_CELLS:
				if cell - self.width < 0:
					cell = 0
				else:
					cell -= self.width

	# could be placed into single method
	def checkCellRight(self, cell, attribute, count = 1):
		# stop other checks if win state already found
		if self.win_state is True:
			return True

		# out of bounds - shouldn't reach this
		if count > 4:
			return False
		 
		# stays in bound of cell count
		if cell > len(self.grid) - 1:
			return False
		
		# 4 consecutive finds of a type is a win state
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			if count is 4:
				print("\t\t\t**WIN STATE FOUND**")
				self.win_state = True
				return True			

		global VERBOSE
		if VERBOSE['check']:
			print('\t[Rt]\t'+' '+str(cell)+' '+str(attribute)+' '+str(count))
		
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			return self.checkCellRight(cell + 1, attribute, count + 1)

	def checkCellUp(self, cell, attribute, count = 1):
		# stop other checks if win state already found
		if self.win_state is True:
			return True

		# out of bounds - shouldn't reach this
		if count > 4:
			return False
		 
		# stays in bound of cell count
		if cell > len(self.grid) - 1:
			return False

		# 4 consecutive finds of a type is a win state
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			if count is 4:
				print("\t\t\t**WIN STATE FOUND**")
				self.win_state = True
				return True			

		global VERBOSE
		if VERBOSE['check']:
			print('\t[Up]\t'+' '+str(cell)+' '+str(attribute)+' '+str(count))

		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			return self.checkCellUp(cell + self.width, attribute, count + 1)

	def checkCellDiagRight(self, cell, attribute, count = 1):	
		# stop other checks if win state already found
		if self.win_state is True:
			return True

		# out of bounds - shouldn't reach this
		if count > 4:
			return False
		 
		# stays in bound of cell count
		if cell > len(self.grid) - 1:
			return False

		# 4 consecutive finds of a type is a win state
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			if count is 4:
				print("\t\t\t**WIN STATE FOUND**")
				self.win_state = True
				return True			

		global VERBOSE
		if VERBOSE['check']:
			print('\t[DR]\t'+' '+str(cell)+' '+str(attribute)+' '+str(count))
		
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			return self.checkCellDiagRight(cell + self.width + 1, attribute, count + 1)

	def checkCellDiagLeft(self, cell, attribute, count = 1):
		# stop other checks if win state already found
		if self.win_state is True:
			return True

		# out of bounds - shouldn't reach this
		if count > 4:
			return False
		 
		# stays in bound of cell count
		if cell > len(self.grid) - 1:
			return False

		# 4 consecutive finds of a type is a win state
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			if count is 4:
				print("\t\t\t**WIN STATE FOUND**")
				self.win_state = True
				return True			

		global VERBOSE
		if VERBOSE['check']:
			print('\t[DL]\t'+' '+str(cell)+' '+str(attribute)+' '+str(count))		
		if self.grid[cell].colour == attribute or self.grid[cell].dot == attribute:
			return self.checkCellDiagLeft(cell + self.width - 1, attribute, count + 1)

	def checkWinPath(self, cell, attribute, count = 1):
		# check path in various win directions
		return 	self.checkCellRight(cell, attribute, count) or self.checkCellUp(cell, attribute, count) or self.checkCellDiagRight(cell, attribute, count) or self.checkCellDiagLeft(cell, attribute, count)	

	def checkWinState(self):
		# check each cell individually
		for index in range(0,len(self.grid)):
			cell = self.grid[index]
			# cell is not empty
			if((cell.colour == 'R' or cell.colour == 'W' or cell.dot == 'f' or cell.dot == 'c') and self.win_state == False):
				global VERBOSE
				if VERBOSE['check']:	
					print('\n\nChecking cell: '+str(index))
					print('-----------------------------')
					print('Checking Colour')
				
				if self.checkWinPath(index, cell.colour, 1):
					print("\t\t\t**Colour Wins!**")
					return True
						
				if VERBOSE['check']:					
					print('Checking Dot')
				
				if self.checkWinPath(index, cell.dot, 1):
					print("\t\t\t**Dot Wins!**")
					return True				
		return False

	# Resets game
	def clear(self):
		print('\n**RESETTING GAME**\n')
		global MOVE_HISTORY, MOVE_COUNT, LEGAL_CELLS, TILES_REMAING
		TILES_REMAINING = 24
		ILLEAGAL_MOVE = False
		MOVE_HISTORY = {}
		MOVE_COUNT = 1
		LEGAL_CELLS = []
		self.grid = []
		self.win_state = False
		self.initGrid()
		self.display()
	
def verbose(meta = False, check = False):
	VERBOSE['meta'] = meta
	# True = will display the pathfinding for the win condition
	VERBOSE['check'] = check		

def m(a,b,c = 1):
	#game.move(a,b,c)
	game.move(a,b,c)

def reset():
	game.clear()

def auto(game):
	game.move(1,1,1)
	game.updateGameMeta(1,1,1)
	game.move(5,1,1)
	game.updateGameMeta(5,1,1)
	game.move(1,2,2)
	game.updateGameMeta(1,2,2)
	game.move(5,2,6)
	game.updateGameMeta(5,2,6)
	game.move(7,2,7)
	game.updateGameMeta(7,2,7)
	game.move(3,1,1)
	game.updateGameMeta(3,1,1)
	game.move(3,2,4)
	game.updateGameMeta(3,2,4)
	game.move(7,1,1)
	game.updateGameMeta(7,1,1)
	"""
	m(1,1,2) # row
	m(2,1,6)
	m(3,1,2)
	m(4,1,6)
	
	m(1,1,1) # column
	m(1,2,5)
	m(1,3,1)
	m(1,4,5)

	m(1,1,1) # diagonal right
	m(3,1,1)
	m(2,2,1)
	m(4,2,2)
	m(2,3,3)
	m(3,4,3)

	m(1,1,1) # diagonal left
	m(3,1,1)
	m(2,2,5)
	m(1,2,2)
	m(2,3,3)
	m(1,4,3)
	"""

verbose(True, False)	# (meta,check)
#game = Board( HEIGHT , WIDTH )
#game.initGrid()
#auto()
#game.display()

# Place into main function
user_in = ''
while user_in != 'q':
	print('Welcome to Double Card')
	user_in = input("Player 1 please select [c]olour or [d]ots ([q] to quit)\n> ")
	if user_in == 'q':
		break

	while (user_in != 'c' or user_in != 'd'):
		if user_in == 'c':
			print('Initializing game [colour] begins:')
			game = Game(HEIGHT, WIDTH, 'colour')
			break
		elif user_in == 'd':
			print('initializing game [dot] begins:')
			game = Game(HEIGHT, WIDTH, 'dot')
			break
		else:
			print('select [c]olour or [d]ots')
			user_in = input()
	
	### Pre inputs game moves
	#auto(game)
	#game.display();
	#metaStats()
	
	# GAME LOOP
	while user_in != 'q':
		current_player = game.getTurn()
		user_in = input('Next move for [%s]\n> ' % current_player)
		if user_in == 'q':
			break

		if user_in == 'h':
			history()

		# 0 defines regular move
		if user_in[0] is '0':
			split_input = user_in.split('0')
			for move in range(1,len(split_input)): 	# index 0 is empty
				parse_move = split_input[move].split(' ')
				next_move = {
					'row': int(parse_move[1]),			# index 0 is empty
					'column': int((COLUMNS.index(parse_move[2]) + 1)),	# transcribe char to int
					'rotation': int(parse_move[3])
				}									
				print('Playing move: '+str(next_move))

				accept_move = False
				if RECYCLED:
					accept_move = game.moveRecycled( next_move['column'], next_move['row'], next_move['rotation'] );
				else: 
					accept_move = game.move( next_move['column'], next_move['row'], next_move['rotation'])
				
				if accept_move:
					game.updateGameMeta(next_move['column'], next_move['row'], next_move['rotation'])
					ILLEAGAL_MOVE = False
				elif ILLEAGAL_MOVE and not accept_move:
					print('[%s] forfeits with second illegal move' % current_player)
					user_in = 'q'
				else:
					ILLEAGAL_MOVE = True
					

				game.display()
				if(VERBOSE['meta']):
					metaStats()
				game.checkWinState()
			
				
		# defines recycled move
		else:
			print('Enter Move')
		

### TODO
# Recycle moves logic
# 	- remember previous position
# 	- cannot move previously played card
# 	- draw game at 60 moves
# Play modes: manual vs auto
# inputs 
# 	- 0 5 A 2 -  new move, 0 denotes new, row, column, rot
# 	- F 2 F 3 3 A 2 - recylced, old card pos, new card pos
# no illegal moves for computer
