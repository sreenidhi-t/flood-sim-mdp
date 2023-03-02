import numpy as np
import random


# Define the Hex class
class Hex:

    # Hex constructor
    def __init__(self, grid, x, y, elevation, population, drain_rate, water_level = 0, drain_status = True):
        self.grid = grid
        self.x = x
        self.y = y
        self.elevation = elevation
        self.population = population
        self.drain_rate = drain_rate
        self.drain_status = drain_status
        self.water_level = water_level

        # Define neighbors as E, NE, NW, W, SW, SE
        self.neighbors = [None, None, None, None, None, None]

    # Define flooded property
    @property
    def is_flooded(self):
        return self.water_level > 0
    
    @property
    def neighbor_east(self):
        # Return the neighbor to the east
        # If at the edge of the grid, return None
        if self.x == self.grid.width - 1:
            return None
        else:
            return self.grid.find_hex(self.x + 1, self.y)
    
    @property
    def neighbor_west(self):
        # Return the neighbor to the west
        # If at the edge of the grid, return None
        if self.x == 0:
            return None
        else:
            return self.grid.find_hex(self.x - 1, self.y)
    
    @property
    def neighbor_northwest(self):
        # Return the neighbor to the northwest
        # If at the edge of the grid, return None
        if self.y == 0:
            return None
        else:
            return self.grid.find_hex(self.x, self.y - 1)
        
    @property
    def neighbor_northeast(self):
        # Return the neighbor to the northeast
        # If at the edge of the grid, return None
        if self.y == 0 or self.x == self.grid.width - 1:
            return None
        else:
            return self.grid.find_hex(self.x + 1, self.y - 1)
        
    @property
    def neighbor_southwest(self):
        # Return the neighbor to the southwest
        # If at the edge of the grid, return None
        if self.y == self.grid.height - 1:
            return None
        else:
            return self.grid.find_hex(self.x, self.y + 1)
    
    @property
    def neighbor_southeast(self):
        # Return the neighbor to the southeast
        # If at the edge of the grid, return None
        if self.y == self.grid.height - 1 or self.x == self.grid.width - 1:
            return None
        else:
            return self.grid.find_hex(self.x + 1, self.y + 1)
        
    
    # Return the neighbor in the given direction (east, northeast, northwest, west, southwest, southeast)
    def get_neighbors_dir(self, direction):
        # If the neighbors have not been calculated, calculate them
        if self.neighbors[0] is None:
            self.neighbors = [self.neighbor_east, self.neighbor_northeast, self.neighbor_northwest, self.neighbor_west, self.neighbor_southwest, self.neighbor_southeast]
        # Dictionary of directions
        cardinal_directions = {"east": 0, "northeast": 1, "northwest": 2, "west": 3, "southwest": 4, "southeast": 5}
        return self.neighbors[cardinal_directions[direction]]

    # Return all neighbors
    def get_neighbors_all(self):
        # If the neighbors have not been calculated, calculate them
        if self.neighbors[0] is None:
            self.neighbors = [self.neighbor_east, self.neighbor_northeast, self.neighbor_northwest, self.neighbor_west, self.neighbor_southwest, self.neighbor_southeast]
        return self.neighbors
    
    # Update hex based on water in-flow
    def update_water_level(self, water_inflow):
        # If the drain is open, subtract the drain rate from the water inflow
        if self.drain_status:
            water_inflow -= self.drain_rate

        # update water level: if drainage is greater than inflow + curr level, water level is 0
        self.water_level = max(self.water_level + water_inflow, 0)
        
    



    