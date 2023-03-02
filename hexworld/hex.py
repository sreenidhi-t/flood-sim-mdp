import numpy as np
import random


# Define the Hex class
class Hex:

    # Hex constructor
    def __init__(self, grid, x, y, elevation, population, drainage_capacity, water_level):
        self.grid = grid
        self.x = x
        self.y = y
        self.elevation = elevation
        self.population = population
        self.drainage_capacity = drainage_capacity
        self.water_level = water_level

        # Define neighbors as W, NW, NE, E, SE, SW
        self.neighbors = [None, None, None, None, None, None]

    # Define flooded property
    @property
    def is_flooded(self):
        return self.water > 0
    
    # Return the neighbor in the given direction
    def hex_neighbors(self, direction):
        return self.neighbors[direction]
    
    # Update hex based on water in-flow
    def update_water_level(self, water_inflow):
        self.water_level = self.water_level + water_inflow
    



    