import random,math

HEIGHT = 6
WIDTH = 6

ROTATION = {
	1: {
		'C1' : {'colour':'R.','dot':'f_'},
		'C2' : {'colour':'W.','dot':'c_'},
		'link': 'right'
	},
	2: {
		'C1' : {'colour':'W.','dot':'c_'},
		'C2' : {'colour':'R.','dot':'f_'},
		'link': 'up'
	},
	3:{
		'C1' : {'colour':'W.','dot':'c_'},
		'C2' : {'colour':'R.','dot':'f_'},
		'link': 'right'
	},
	4:{
		'C1' : {'colour':'R.','dot':'f_'},
		'C2' : {'colour':'W.','dot':'c_'},
		'link': 'up'
	},
	5:{
		'C1' : {'colour':'R.','dot':'c_'},
		'C2' : {'colour':'W.','dot':'f_'},
		'link': 'right'
	},
	6:{
		'C1' : {'colour':'W.','dot':'f_'},
		'C2' : {'colour':'R.','dot':'c_'},
		'link': 'up'
	},
	7:{
		'C1' : {'colour':'W.','dot':'f_'},
		'C2' : {'colour':'R.','dot':'c_'},
		'link': 'right'
	},
	8:{
		'C1' : {'colour':'R.','dot':'c_'},
		'C2' : {'colour':'W.','dot':'f_'},
		'link': 'up'
	}
}

COLUMNS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

MOVE_HISTORY = {}
MOVE_COUNT = 1

LEGAL_CELLS = []

def history():
	count = 1
	for i in MOVE_HISTORY:
		m = MOVE_HISTORY[i]
		print('['+str(count)+']: Col.'+str(m['column'])+' Row.'+str(m['row'])+' Rot.'+str(m['rotation']))
		count += 1

class Cell:
	def __init__(self, colour = '__', dot = '__', link = '__'):
		self.colour = colour	# 0 == white, 1 = red
		self.dot = dot				# 0 == circle, 1 == filled
		self.link = link			# other cell location, eg A4

class Board:
	def __init__(self,height = 12,width = 8):
		self.height = height
		self.width = width
		self.grid = []
		self.total_cells = height * width

	def initGrid(self):
		global LEGAL_CELLS
		for n in range(self.total_cells):
			self.grid.append(Cell())		
		for i in range(self.width):
			LEGAL_CELLS.append(i)

	def updateCell(self,cell,colour,dot,link):
		self.grid[cell].colour = colour
		self.grid[cell].dot = dot
		self.grid[cell].link = link

	def display(self):
		display_height = 1

		# top
		for i in range(self.width):
			print('______', end='')
		print()

		# board
		for i in range(self.total_cells):
			print("|"+str(self.grid[i].colour)+str(self.grid[i].dot)+"|", end='')
			#print("|"+str(self.grid[i].link)+"|", end='')

			# newline at width length
			if(math.ceil(i % self.width) is self.width-1):
				print(str(display_height))
				display_height += 1

		# column names
		for i in range(self.width):
			#print(' '+COLUMNS[i]+'  ',end='')
			print('  '+ str( i + 1 ) +'   ',end='')
		print('')
		global LEGAL_CELLS
		print('Legal Cells: '+str(LEGAL_CELLS))
				
	# prints out contents of grid array
	def showGrid(self):
		for i in range(self.total_cells):
			print('CELL['+str(i)+']: '+str(self.grid[i].colour)+" "+str(self.grid[i].dot)+" link:"+str(self.grid[i].link))

	def move(self, column, row, rotation):
		global MOVE_HISTORY, MOVE_COUNT
		MOVE_HISTORY[MOVE_COUNT] = {
				'column':column,
				'row': row,
				'rotation': rotation
		}
		MOVE_COUNT += 1

		if(rotation < 1 or rotation > 8):
			print('\n**Illegal move**: not rotation type')
			self.display()
			return

		# check bounds
		if(column > self.width or column < 1 or row > self.height or row < 1):
			print('\n**Illegal move**: Out of bounds')
			self.display()
			return

		# determine placement in array
		index = (column - 1) + ((row - 1) * self.width)

		# check empty cell
		if(self.grid[index].colour == 'R.' or self.grid[index].colour == 'W.'):
			print('\n**Illegal move**: Cell already played')
			self.display()
			return

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
				self.display()
				return
		else:
			link = index + 1
			if(link >= (self.width * row)):
				print('\n**Illegal move**: link cell out of bounds [Right]')
				print('index: '+str(index)+' '+str(link))
				self.display()
				return

		print('index: '+str(index)+' '+str(link))
		self.updateLegalCells(index,link)
		self.updateCell( index, C1['colour'], C1['dot'], link )
		self.updateCell( link, C2['colour'], C2['dot'], index )
		self.display()
	
	def clear(self):
		global MOVE_HISTORY, MOVE_COUNT
		MOVE_HISTORY = {}
		MOVE_COUNT = 1
		self.grid = []
		self.initGrid()
		self.display()

	def updateLegalCells(self,index,link):
		global LEGAL_CELLS
		LEGAL_CELLS.remove(index)
		LEGAL_CELLS.append(index + self.width) # cell above is legal
		LEGAL_CELLS.remove(link)
		LEGAL_CELLS.append(link + self.width) # cell above is legal


def m(a,b,c = 1):
	game.move(a,b,c)

def reset():
	game.clear()

def auto():
	m(1,1,1)
	m(1,2,2)
	m(3,4,1)
	m(4,2,2)

game = Board( HEIGHT , WIDTH )
game.initGrid()
game.display()
