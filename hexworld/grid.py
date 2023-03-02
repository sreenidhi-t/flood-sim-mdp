import math
import numpy as np
import random

from hex import Hex

class GridBoundsException(Exception):
    pass

# Create grid from Hex objects
class Grid:
    
    # Grid constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.hexes = []

        self.grid = np.ndarray((self.width, self.height), dtype=np.object)
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                # Randomly generate elevation
                elevation = random.randint(0, 20)
                # Random population
                population = random.randint(0, 100)
                # Random drain rate
                drain_rate = random.randint(0, 10)
                self.grid[x][y] = Hex(self, x, y, elevation, population, drain_rate)
                self.hexes.append(self.grid[x][y])
        
        self.calculate()

    # Calculate the grid
    def calculate(self):
        # Run through the grid, calculate the edges
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                # self.grid[x][y].calculate()
                self.hexes.append(self.grid[x][y])

    def find_hex(self, x, y):
        # Find hex at x and y coordinate
        try:
            return self.grid[x][y]
        except IndexError:
            raise GridBoundsException("Invalid coordinates {}, {}".format(x, y))