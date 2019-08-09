# python packages
import random
# internal packages
from block import *

class Maze():
	def __init__(self, length, height):
		self.length = length
		self.height = height
		self.maze = [None] * length * height
		# set up the maze
		self.generate_maze()

	def __repr__(self):
		string_length = self.length + 1
		string_height = self.height + 1
		string_maze = [None] * string_length * string_height
		for location, character in enumerate(string_maze):
			# get initial index
			nw = location - string_length - 1
			ne = location - string_length
			sw = location - 1
			se = location
			# recalibrate to 'true self' indices
			nw = nw - (nw // string_height)
			ne = ne - (ne // string_height)
			sw = sw - (sw // string_height)
			se = se - (se // string_height)
			print(string_height)


			# this happens when quad is on a western boundary.
			if sw == se:
				west = True
			else:
				west = False
			# this happens when quad is on a eastern boundary.
			if nw == ne:
				east = True
			else:
				east = False
			# this happens when quad is on a northern boundary.
			if nw < 0 and ne < 0:
				north = True
			else:
				north = False
			# this happens when quad is on a southern boundary.
			if sw >= len(self.maze) and se >= len(self.maze):
				south = True
			else:
				south = False

			print(
				'---\n'
				f'nw {nw}\n'
				f'ne {ne}\n'
				f'sw {sw}\n'
				f'se {se}\n'
			)

			print(
				'---\n'
				f'north {north}\n'
				f'south {south}\n'
				f'east {east}\n'
				f'west {west}\n'
			)

		return 'WiP'

	def get_block(self, row_id, column_id):
		'''
		returns the cell located at given coordinates.
		'''
		location = row_id * self.height + column_id
		block = self.maze[location]
		return block

	def get_row(self, row_id):
		'''
		returns the nth full row.
		'''
		east = row_id * self.height
		west = east + self.length
		row = self.maze[east:west]
		return row

	def get_column(self, column_id):
		'''
		returns the nth full column.
		'''
		num_columns = self.length
		column = self.maze[column_id::num_columns]
		return column

	def get_each_row(self):
		'''
		returns an array arrays; a list of every row.
		'''
		each_row = []
		for row_id in range(0, self.height):
			each_row.append(self.get_row(row_id))
		return each_row

	def get_each_column(self):
		'''
		returns an array arrays; a list of every column.
		'''
		each_column = []
		for column_id in range(0, self.length):
			each_column.append(self.get_column(column_id))
		return each_column

	def generate_maze(self, loc = None):
		'''
		generates a perfect maze.
		its done recursively via a depth-first traversal tree.
		this is a setter function; it does not return anything.
		---
		key = cardinal direction
		rev = reversed cardinal direction
		loc = root location
		nbr = neighbor location
		'''
		if loc is None:
			# start the trees loc at a random point in the maze.
			# this doesnt infer a start/exit in the finished maze.
			# one can always find a path from any point A to B;
			# the program will decide these points later.
			loc = random.randint(0, len(self.maze) - 1)
			# note our visited list exists as the maze property.

		# first, fill the maze spot with an empty block.
		self.maze[loc] = Block()

		# grab the location id from each cardinal direction.
		neighbor_locations = {
			'north': loc - self.length,
			'south': loc + self.length,
			'east': loc - 1,
			'west': loc + 1,
		}

		# this is useful for doubly-linked vertices.
		reverse_compass = {
			'north': 'south',
			'south': 'north',
			'east': 'west',
			'west': 'east',
		}

		# validate will remove indices that are out-of-bounds.
		def validate(location):
			if len(self.maze) > location >= 0:
				return location
			else:
				return None

		# update neighbors with validate.
		for key, nbr in neighbor_locations.items():
			# it is safe to update a key's value in a loop;
			# it isnt safe to update a key in a loop.
			neighbor_locations[key] = validate(nbr)

		for key, nbr in neighbor_locations.items():
			# rev reverses key, a cardinal direction.
			rev = reverse_compass[key]
			# nbr is empty, representing a maze boundary.
			if nbr is None:
				self.maze[loc].neighbors[key] = None
				pass

			# nbr is an int, representing a spot in maze.
			else:
				# this spot is empty! fill it up!
				if self.maze[nbr] is None:
					# generate a new maze block.
					self.generate_maze(nbr)
					# link up the net / graph / tree.
					self.maze[loc].neighbors[key] = self.maze[nbr]
					self.maze[nbr].neighbors[rev] = self.maze[loc]

				# this spot is filled.
				else:
					pass
