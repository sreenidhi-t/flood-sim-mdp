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

        self.grid = np.ndarray((self.width, self.height), dtype=object)
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                # Set starting elevations to 0
                elevation = 0
                # Random population
                population = random.randint(0, 100)
                # Random drain rate
                drain_rate = random.randint(0, 10)
                # Create the hex
                self.grid[x][y] = Hex(self, x, y, elevation, population, drain_rate)
                # Add the hex to the list of hexes
                self.hexes.append(self.grid[x][y])
        
        self.calculate()
        self.update_elevations()

    # Update the elevations of the grid
    def update_elevations(self):
        max_elevation = 200
        max_deviation = 7
        # Start with top left hex and generate a random elevation
        self.grid[0][0].elevation = random.uniform(0, max_elevation)
        # Run through the grid and generate elevation within random deviation from the previous hex
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                # Skip the first hex
                if x == 0 and y == 0:
                    continue
                # Get elevation of neighbors
                neighbors = self.grid[x][y].get_neighbors_all()
                neighbor_elevations = []
                for n in neighbors:
                    if n is not None:
                        neighbor_elevations.append(n.elevation)
                # Get the average elevation of the neighbors    
                avg_elevation = sum(neighbor_elevations) / len(neighbor_elevations)
                # Generate a random deviation from the average elevation
                deviation = random.uniform(-max_deviation, max_deviation)
                # Set the elevation of the hex
                self.grid[x][y].elevation = avg_elevation + deviation
                # Set the elevation of the hex to the max elevation if it is greater than the max elevation
                if self.grid[x][y].elevation > max_elevation:
                    self.grid[x][y].elevation = max_elevation
                # Set the elevation of the hex to the min elevation if it is less than the min elevation
                if self.grid[x][y].elevation < 0:
                    self.grid[x][y].elevation = 0

    

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