import numpy as np
import random
from constants import FLOOD_LEVEL


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
        self.evac_flag = False
        self.flood_flag = False

        # Define neighbors as E, NE, NW, W, SW, SE
        self.neighbors = [None, None, None, None, None, None]

    def __deepcopy__(self, memo):
        '''Deep copy the hex'''
        return Hex(self.grid, self.x, self.y, self.elevation, self.population, self.drain_rate, self.water_level, self.drain_status)

    @property
    def is_flooded(self):
        '''# Define flooded property'''
        return self.water_level > FLOOD_LEVEL  
    
    @property
    def neighbor_east(self):
        '''Return the neighbor to the east'''
        # If at the edge of the grid, return None
        if self.y == self.grid.width - 1:
            return None
        else:
            return self.grid.find_hex(self.x, self.y + 1)
    
    @property
    def neighbor_west(self):
        '''Return the neighbor to the west'''
        # Return the neighbor to the west
        # If at the edge of the grid, return None
        if self.y == 0:
            return None
        else:
            return self.grid.find_hex(self.x, self.y - 1)
    
    @property
    def neighbor_northwest(self):
        '''Return the neighbor to the NW'''
        # Return the neighbor to the northwest
        # If at the edge of the grid, return None
        if self.x == 0:
            return None
        even_row = self.x % 2 == 0
        if even_row:
            if self.y == 0:
                return None
            else:
                return self.grid.find_hex(self.x - 1, self.y - 1)
        else:
            return self.grid.find_hex(self.x - 1, self.y)
        
    @property
    def neighbor_northeast(self):
        '''Return the neighbor to the NE'''
        # Return the neighbor to the northeast
        # If at the edge of the grid, return None
        if self.x == 0:
            return None
        even_row = self.x % 2 == 0
        if even_row:
            return self.grid.find_hex(self.x - 1, self.y)
        else:
            if self.y == self.grid.width - 1:
                return None
            else:
                return self.grid.find_hex(self.x - 1, self.y + 1)
        
    @property
    def neighbor_southwest(self):
        '''Return the neighbor to the SW'''
        # Return the neighbor to the southwest
        # If at the edge of the grid, return None
        if self.x == self.grid.height - 1:
            return None
        even_row = self.x % 2 == 0
        if even_row:
            if self.y == 0:
                return None
            else:
                return self.grid.find_hex(self.x + 1, self.y - 1)
        else:
            return self.grid.find_hex(self.x + 1, self.y)
    
    @property
    def neighbor_southeast(self):
        '''Return the neighbor to the SE'''
        # Return the neighbor to the southeast
        # If at the edge of the grid, return None
        if self.x == self.grid.height - 1:
            return None
        even_row = self.x % 2 == 0
        if even_row:
            return self.grid.find_hex(self.x + 1, self.y)
        else:
            if self.y == self.grid.width - 1:
                return None
            else:
                return self.grid.find_hex(self.x + 1, self.y + 1)
        
    
    def get_neighbors_dir(self, direction):
        '''# Return the neighbor in the given direction (east, northeast, northwest, west, southwest, southeast)'''
        # If the neighbors have not been calculated, calculate them
        if self.neighbors[0] is None:
            self.neighbors = [self.neighbor_east, self.neighbor_northeast, self.neighbor_northwest, self.neighbor_west, self.neighbor_southwest, self.neighbor_southeast]
        # Dictionary of directions
        cardinal_directions = {"east": 0, "northeast": 1, "northwest": 2, "west": 3, "southwest": 4, "southeast": 5}
        return self.neighbors[cardinal_directions[direction]]

    def get_neighbors_all(self):
        '''# Return all neighbors'''
        # If the neighbors have not been calculated, calculate them
        if self.neighbors[0] is None:
            self.neighbors = [self.neighbor_east, self.neighbor_northeast, self.neighbor_northwest, self.neighbor_west, self.neighbor_southwest, self.neighbor_southeast]
        return self.neighbors
    
    
    def add_water(self, water_inflow=0):
        '''# Update hex based on water in-flow'''
        # update water level: if drainage is greater than inflow + curr level, water level is 0
        self.water_level += water_inflow
    
    def remove_water(self, water_out=0):
        '''# Update hex based on water out-flow'''
        # update water level: if drainage is greater than inflow + curr level, water level is 0
        self.water_level -= water_out
        if self.water_level < 0:
            self.water_level = 0

    def drain_water(self):
        '''# Drain water from the hex'''
        # If the drain is open, drain the water
        if self.drain_status:
            self.water_level -= self.drain_rate
        if self.water_level < 0:
            self.water_level = 0
        if self.water_level > FLOOD_LEVEL and not self.flood_flag:
            self.flood_flag = True

    def evac(self, ppl):
        self.population -= ppl
        self.evac_flag = True
    



    