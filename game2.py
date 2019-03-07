import random,math

HEIGHT = 3
WIDTH = 3

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

VERTICAL_ROTATIONS = [2,4,6,8]

HORIZONTAL_ROTATIONS = [1,3,5,8]

COLUMNS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# Place into Game class
MOVE_HISTORY = {0:{}}
MOVE_COUNT = 0			# 60 == tie
MAX_NUM_MOVES = 20
TILES_REMAINING = 10
RECYCLED = False
LEGAL_CELLS = []
LEGAL_CELL_SCORE = {}
ILLEAGAL_MOVE = False
VERBOSE = {
	'check': 	False,
	'meta': 	False
}
PLAYER_SCORES = {
	'F' : 0,
	'C' : 0,
	'R' : 0,
	'W' : 0
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
	print('Legal Cell Scores: ')
	for cell in LEGAL_CELL_SCORE:
		r = LEGAL_CELL_SCORE[cell]['R']
		w = LEGAL_CELL_SCORE[cell]['W']
		f = LEGAL_CELL_SCORE[cell]['F']
		c = LEGAL_CELL_SCORE[cell]['C']
		print(str(cell)+' r['+str(r)+'] w['+str(w)+'] f['+str(f)+'] c['+str(c)+']')
	print('Tiles Remaining: '+str(TILES_REMAINING))
	print('Moves Remaining: '+str(MAX_NUM_MOVES - MOVE_COUNT))
	print('Dot Score: F['+ str(PLAYER_SCORES['F']) + '] C[' + str(PLAYER_SCORES['C']) + ']')
	print('Colour Score: R['+ str(PLAYER_SCORES['R'])+'] W['+str(PLAYER_SCORES['W'])+']')
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
		for i in range(self.width):
			LEGAL_CELL_SCORE[str(i)] = {
				'R': 0,
				'W': 0,
				'F': 0,
				'C': 0
			}

	def updateCell(self, cell, colour, dot, link, link_direction):
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
			# print('CELL['+str(i)+']: '+str(self.grid[i].colour)+" "+str(self.grid[i].dot)+" link:"+str(self.grid[i].link))
			print('INDEX['+str(i)+'] { "colour": "'+str(self.grid[i].colour)+'", "dot": "'+str(self.grid[i].dot)+'", "link": "'+str(self.grid[i].link)+'"},')

	def getGrid(self):
		return self.grid

	# Returns True if move is playable
	def move(self, column, row, rotation):
		global ILLEAGAL_MOVE, RECYCLED, MOVE_HISTORY
		
		# check last move played for RECYCLED moves
		if RECYCLED:
			last_move = list(MOVE_HISTORY.items())[-1][1]
			if last_move['column'] == column and last_move['row'] == row and last_move['rotation']:
				print('\n**Illegal Move**: Duplicate move')

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
		if ROTATION[rotation]['link'] == 'right':			
			self.updateCell( index, C1['colour'], C1['dot'], link, '>' )  
			self.updateCell( link, C2['colour'], C2['dot'], index, '<' )
		elif ROTATION[rotation]['link'] == 'up':
			self.updateCell( index, C1['colour'], C1['dot'], link, '^' )
			self.updateCell( link, C2['colour'], C2['dot'], index, 'v' )
		return True
	
	def removeCell(self, removed_cell, removed_link):
		global LEGAL_CELLS
		# determine placement in array
		removed_index = (removed_cell['column'] - 1) + ((removed_cell['row'] - 1) * self.width)
		removed_link_index = (removed_link['column'] - 1) + ((removed_link['row'] - 1) * self.width)

		# verify index and link connection
		if self.grid[removed_index].link is not removed_link_index:
			print('Removed Tile cells do not match')
			return False

		# make sure removed cells don't create illegal board state
		def checkLegalBoardState(removed_index, removed_link_index):
			# check horizontal tile		
			if removed_index + 1 == removed_link_index:	
				if (removed_index + self.width + 1) in LEGAL_CELLS and (removed_link_index + self.width + 1) in LEGAL_CELLS:
					return True
				else:
					return False
			# check vertical tile
			elif removed_index + self.width == removed_link_index:
				if removed_link_index + self.width + 1 in LEGAL_CELLS:
					return True
				else:
					return False
			else:
				return False

		if checkLegalBoardState(removed_index, removed_link_index) is False:
			print('Illegal Move: Removing tile will create bad board state')
			return False

		# reset cells
		self.updateCell( removed_index, '.', '.', '.', '.' )
		self.updateCell( removed_link_index, '.', '.', '.', '.' )

		self.removeFromLegalCells(removed_index, removed_link_index)
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
		global LEGAL_CELLS, LEGAL_CELL_SCORE
		LEGAL_CELLS.remove(index + 1)				# remove previous index from list
		LEGAL_CELLS.append(index + self.width + 1) 	# cell above is now legal, add to list
		LEGAL_CELLS.remove(link + 1)				# remove previous link from list
		LEGAL_CELLS.append(link + self.width + 1) 	# cell above is now legal, add to list
		LEGAL_CELLS.sort()
		# clear score data if not a legal cells
		TEMP_SCORES = LEGAL_CELL_SCORE.copy()
		for cell in TEMP_SCORES:
			if cell not in LEGAL_CELLS:
				LEGAL_CELL_SCORE.pop(str(cell),None)
		
		# add new legal cells to scores
		for cell in LEGAL_CELLS:	
			if str(cell) not in LEGAL_CELL_SCORE: 
				LEGAL_CELL_SCORE[str(cell)] = {
					'R': 0,
					'W': 0,
					'F': 0,
					'C': 0
				}

	def removeFromLegalCells(self, index, link):		
		global LEGAL_CELLS
		LEGAL_CELLS.remove(link + self.width + 1)				# remove previous legal cell from list
		LEGAL_CELLS.append(link + 1) 							# cell above is now legal, add to list
		LEGAL_CELLS.remove(index + self.width + 1)				# remove previous legal cell from list
		LEGAL_CELLS.append(index + 1) 							# cell below is now legal, add to list
		LEGAL_CELLS.sort()

		#TODO:: Clear cell score array

	def getLegalCells(self):
		global LEGAL_CELLS
		return LEGAL_CELLS

	def getLegalCellScore(self):
		global LEGAL_CELL_SCORE
		return LEGAL_CELL_SCORE

	def getPlayerScores(self):
		global PLAYER_SCORES
		return PLAYER_SCORES

	# for > 3 path, ie winning move - should always play vertical?
	def selectTile4(self,index,attribute):
		global VERTICAL_ROTATIONS, ROTATION
		print('Play vertical')
		for r in VERTICAL_ROTATIONS:
			for cell in ROTATION[r].keys():
				if cell != 'link':
					if ROTATION[r][cell]['colour'] == attribute or ROTATION[r][cell]['dot'] == attribute:
						return r

	# for > 1 path
	def selectTile2(self,index,attribute):
		global LEGAL_CELLS
		# legal cell is horizontal
		if index + 1 in LEGAL_CELLS:
			if index % 5 != 0:					# track last column of row
				print('Play horizontal')
				for r in HORIZONTAL_ROTATIONS:
					for cell in ROTATION[r].keys():			
						if cell != 'link' or cell == 'C2':
							if ROTATION[r][cell]['colour'] == attribute or ROTATION[r][cell]['dot'] == attribute:
								if cell == 'C2':
									return r - 1
								else:
									return r
		# legal cell is vertical
		## can give colour in wrong cell positions
		else:
			print('Play vertical')
			for r in VERTICAL_ROTATIONS:
				for cell in ROTATION[r].keys():
					if cell != 'link':
						if ROTATION[r][cell]['colour'] == attribute or ROTATION[r][cell]['dot'] == attribute:
							return r
			

	# recursively checks cell for attribute and follows leads
	def checkCell(self, cell, attribute, direction,count = 1):
		global PLAYER_SCORES, LEGAL_CELLS, LEGAL_CELL_SCORE
		# stop other checks if win state already found
		if self.win_state is True:
			return True

		# out of bounds - shouldn't reach this
		if count > 4:
			return False
		 
		# stays in bound of cell count
		if cell > len(self.grid) - 1:
			return False

		# #							  # #  
		# # #  testing heuristics 	# # #
		# #							  # #
		"""
		if count is 3:
			print('\nPotential Win state\n'+direction+' - '+attribute +' Should play at cell: '+COLUMNS[(cell % self.width)]+' '+ str(math.ceil(cell/self.width)))
			if cell+1 in LEGAL_CELLS:
				print('Cell ['+str(cell+1)+'] is playable')
				rotation = self.selectTile2(cell+1,attribute)
				print('play rotation:'+str(rotation))
		"""
		if count is 4:
			print('\nPotential Win state\n'+direction+' - '+attribute +' Should play at cell: '+COLUMNS[(cell % self.width)]+' '+ str(math.ceil(cell/self.width)))
			if cell+1 in LEGAL_CELLS:
				print('Cell ['+str(cell+1)+'] is playable')
				rotation = self.selectTile4(cell+1,attribute)
				print('play rotation:'+str(rotation))

		

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
			
			if direction == 'up':
				return self.checkCell(cell + self.width, attribute, 'up', count + 1)
			elif direction == 'right':
				return self.checkCell(cell + 1, attribute, 'right', count + 1)
			elif direction == 'diagRight':
				return self.checkCell(cell + self.width + 1, attribute, 'diagRight', count + 1)
			elif direction == 'diagLeft':
				return self.checkCell(cell + self.width - 1, attribute, 'diagLeft', count + 1)

		# cell is empty and legal cell, give it a score based on count
		elif cell+1 in LEGAL_CELLS:
			score = 0;
			if count == 2: 
				score = 10
			if count == 3:
				score = 100
			if count == 4:
				score = 1000
			LEGAL_CELL_SCORE[str(int(cell) + 1)][attribute] += score

	# could be placed into single method
	"""
	def checkCellRight(self, cell, attribute, count = 1):
		global PLAYER_SCORES
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
			PLAYER_SCORES[attribute] += (count - 1)
			return self.checkCellRight(cell + 1, attribute, count + 1)

	def checkCellUp(self, cell, attribute, count = 1):
		global PLAYER_SCORES
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
			PLAYER_SCORES[attribute] += (count - 1)
			return self.checkCellUp(cell + self.width, attribute, count + 1)

	def checkCellDiagRight(self, cell, attribute, count = 1):	
		global PLAYER_SCORES
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
			PLAYER_SCORES[attribute] += (count - 1)
			return self.checkCellDiagRight(cell + self.width + 1, attribute, count + 1)

	def checkCellDiagLeft(self, cell, attribute, count = 1):
		global PLAYER_SCORES
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
			PLAYER_SCORES[attribute] += (count - 1)
			return self.checkCellDiagLeft(cell + self.width - 1, attribute, count + 1)
	"""
	def checkWinPath(self, cell, attribute, count = 1):
		global PLAYER_SCORES
		# check path in various win directions
		checkUp = self.checkCell(cell, attribute, 'up', count)
		checkRight = self.checkCell(cell, attribute, 'right', count)
		checkDiagRight = self.checkCell(cell, attribute, 'diagRight', count)
		checkDiagLeft = self.checkCell(cell, attribute, 'diagLeft', count)
		return checkUp or checkRight or checkDiagRight or checkDiagLeft
		# return 	self.checkCellRight(cell, attribute, count) or self.checkCellUp(cell, attribute, count) or self.checkCellDiagRight(cell, attribute, count) or self.checkCellDiagLeft(cell, attribute, count)	

	def checkWinState(self):
		global PLAYER_SCORES, LEGAL_CELL_SCORE
		for t in PLAYER_SCORES:
			PLAYER_SCORES[t] = 0

		
		# check each cell individually
		for index in range(0,len(self.grid)):
			cell = self.grid[index]
			# cell is not empty
			if((cell.colour == 'R' or cell.colour == 'W' or cell.dot == 'F' or cell.dot == 'C') and self.win_state == False):
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

		# cheap player heuristical value
		for cell in LEGAL_CELL_SCORE:
			PLAYER_SCORES['R'] += LEGAL_CELL_SCORE[cell]['R']
			PLAYER_SCORES['W'] += LEGAL_CELL_SCORE[cell]['W']
			PLAYER_SCORES['F'] += LEGAL_CELL_SCORE[cell]['F']
			PLAYER_SCORES['C'] += LEGAL_CELL_SCORE[cell]['C']

		# No declarable winner	
		return False

	# Resets game
	def clear(self):
		print('\n**RESETTING GAME**\n')
		global MOVE_HISTORY, MOVE_COUNT, LEGAL_CELLS, TILES_REMAING
		TILES_REMAINING = 24
		ILLEAGAL_MOVE = False
		MOVE_HISTORY = {0:{}}
		MOVE_COUNT = 1
		LEGAL_CELLS = []
		self.grid = []
		self.win_state = False
		self.initGrid()
		self.display()
	
def verbose(meta = False, check = False):
	VERBOSE['meta'] = meta
	VERBOSE['check'] = check				# True = will display the pathfinding for the win condition

def reset(game):
	game.clear()

# pre-add game moves here
def auto(game):
	"""
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

# (Output game stats, Output win-state pathfinding)
verbose(True, False)	

# Place into main function
def main():
	global ILLEAGAL_MOVE, WIDTH, HEIGHT
	user_in = ''
	while user_in != 'q':
		print('Welcome to Double Card')
		user_in = input("Player 1 please select [c]olour or [d]ots ([q] to quit)\n> ")
		if user_in == 'q':
			break

		# P1 chooses type
		while (user_in != 'c' or user_in != 'd'):
			if user_in == 'c':
				print('Initializing game: [colour] begins:')
				game = Game(HEIGHT, WIDTH, 'colour')
				break
			elif user_in == 'd':
				print('Initializing game: [dot] begins:')
				game = Game(HEIGHT, WIDTH, 'dot')
				break
			else:
				print('select [c]olour or [d]ots')
				user_in = input()
		
		### Pre inputs game moves
		#auto(game)
		#game.display();
		#metaStats()
		
		if(VERBOSE['meta']):
			metaStats()

		# #					  # #	
		# # # # GAME LOOP # # # #
		# # 				  # #
		while user_in != 'q':
			current_player = game.getTurn()
			user_in = input('Next move for [%s]\n> ' % current_player)

			#quit game
			if user_in == 'q':
				break

			# show move history
			if user_in == 'h':
				history()
				break

			if user_in == 'r':
				reset(game)
				break

			if user_in == 'g':
				game.showGrid()
				break

			# 0 defines regular move
			if user_in[0] is '0':
				split_input = user_in.split('0')
				
				for move in range( 1, len(split_input) ): 	# index 0 is empty
					
					parse_move = split_input[move].split(' ')					

					next_move = {
						'row': int(parse_move[3]),							# index 0 is empty
						'column': int((COLUMNS.index(parse_move[2]) + 1)),	# transcribe char to int
						'rotation': int(parse_move[1])
					}									
					
					print('\nPlaying move: '+str(next_move))
				
					# method verifies move
					accept_move = game.move( next_move['column'], next_move['row'], next_move['rotation'])
					
					if accept_move:
						game.updateGameMeta(next_move['column'], next_move['row'], next_move['rotation'])
						ILLEAGAL_MOVE = False
					elif ILLEAGAL_MOVE and not accept_move:
						# 2nd illegal move, game exit
						print('[%s] forfeits with second illegal move' % current_player)
						user_in = 'q'
						break
					else:
						# Register first illegal move
						ILLEAGAL_MOVE = True
						

					game.checkWinState()
					game.display()
					if(VERBOSE['meta']):
						metaStats()
				
					
			# other inputs define recycled move
			## Add check for recycled game state
			else:
				split_input = user_in.split(' ')
				removed_cell = {
					'column':	int( (COLUMNS.index(split_input[0]) + 1) ),
					'row':		int( split_input[1] )
				}
				removed_link = {
					'column':	int( (COLUMNS.index(split_input[2]) + 1) ),
					'row':		int( split_input[3] )
				}

				next_move = {
					'row': int(split_input[6]),							# index 0 is empty
					'column': int((COLUMNS.index(split_input[5]) + 1)),	# transcribe char to int
					'rotation': int(split_input[4])
				}				

				## Check removed cell doesn't create bad state
				removed_cell = game.removeCell(removed_cell, removed_link)

				if removed_cell:
					accept_move = game.move( next_move['column'], next_move['row'], next_move['rotation'])	
					if accept_move:
						game.updateGameMeta(next_move['column'], next_move['row'], next_move['rotation'])
						ILLEAGAL_MOVE = False
					elif ILLEAGAL_MOVE and not accept_move:
						# 2nd illegal move, game exit
						print('[%s] forfeits with second illegal move' % current_player)
						user_in = 'q'
						break
					else:
						# Register first illegal move
						ILLEAGAL_MOVE = True

				elif ILLEAGAL_MOVE and not removed_cell:
					# 2nd illegal move, game exit
					print('[%s] forfeits with second illegal move' % current_player)
					user_in = 'q'
				else:
					# Register first illegal move
					print('Cannot remove selected tile')					
					ILLEAGAL_MOVE = True	

				game.checkWinState()
				game.display()
				if(VERBOSE['meta']):
					metaStats()

								
# START GAME!			
# main()

#TODO::
# exit game at win state
"""
0 3 A 1
0 5 C 1
0 7 B 1
0 7 B 2
0 5 B 3
0 2 D 2
"""
