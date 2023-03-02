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
        max_elevation = 50
        # Start with top left hex and generate a random elevation
        # Then, move to the right and generate another random elevation within the average of all neighbor elevations
        # Then, move down and generate another random elevation within the average of all neighbor elevations
        # Repeat until all hexes have been assigned an elevation
        # Start with top left hex
        self.grid[0][0].elevation = random.randint(0, max_elevation)
        # Move to the right
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                # Skip the first hex
                if x == 0 and y == 0:
                    continue
                current_hex = self.grid[x][y]
                # Get the average elevation of the neighbors
                neighbors = current_hex.get_neighbors_all()
                neighbor_elevations = []
                for neighbor in neighbors:
                    if neighbor is None:
                        continue
                    else:
                        neighbor_elevations.append(neighbor.elevation)
                average_elevation = sum(neighbor_elevations) / len(neighbor_elevations)
                # Generate a random elevation within the average of the neighbor elevations
                current_hex.elevation = random.randint(math.floor(average_elevation - 5), math.floor(average_elevation + 5))
                # If the elevation is greater than the max elevation, set it to the max elevation
                if current_hex.elevation > max_elevation:
                    current_hex.elevation = max_elevation
                # If the elevation is less than 0, set it to 0
                if current_hex.elevation < 0:
                    current_hex.elevation = 0

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