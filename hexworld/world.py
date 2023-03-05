import math
import noise
import numpy as np
import random
from constants import MAX_DRAIN_RATE, MAX_ELEV, MAX_ELEV_DEV, MIN_ELEV

from hex import Hex

class GridBoundsException(Exception):
    pass

# Create grid from Hex objects
class World:
    
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
                drain_rate = random.random()*MAX_DRAIN_RATE
                # Create the hex
                self.grid[x][y] = Hex(self, x, y, elevation, population, drain_rate)
                # Add the hex to the list of hexes
                self.hexes.append(self.grid[x][y])
        
        self.calculate()
        self.update_elevations2()

    def __deepcopy__(self, memo):
        '''Deep copy the grid'''
        new_grid = World(self.width, self.height)
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                new_grid.grid[x][y] = self.grid[x][y].__deepcopy__(memo)
        return new_grid

    # Update the elevations of the grid
    def update_elevations(self):
        max_elevation = MAX_ELEV
        min_elevation = MIN_ELEV
        max_deviation = MAX_ELEV_DEV
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
                self.grid[x][y].elevation = avg_elevation + deviation + random.random()
                # Set the elevation of the hex to the max elevation if it is greater than the max elevation
                if self.grid[x][y].elevation > max_elevation:
                    self.grid[x][y].elevation = max_elevation
                # Set the elevation of the hex to the min elevation if it is less than the min elevation
                if self.grid[x][y].elevation < min_elevation:
                    self.grid[x][y].elevation = min_elevation

    def update_elevations2(self):
        max_elevation = MAX_ELEV
        min_elevation = MIN_ELEV
        max_deviation = MAX_ELEV_DEV

        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                nx = x/self.height
                ny = y/self.width
                self.grid[x][y].elevation = noise.pnoise2(nx, ny, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0)


    

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