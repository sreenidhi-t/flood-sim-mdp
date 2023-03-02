from grid import Grid
import numpy as np
from copy import deepcopy

# determine which adjacent cell the water flows into
def flowCell(x,y,grid):
    # get the current cell from the grid and its neighbors
    currCell = grid.find_hex(x,y)
    neighbors = currCell.get_neighbors_all()
    # compile a list of neighbors with lower elevations
    lower = []
    for neighbor in neighbors:
        if neighbor.elevation <= currCell.elevation:
            lower += neighbor
    # given the current cell has water, identify the next cell it flows to
    if currCell.water_level > 0:
        nextCell = np.random.choice(lower)
    else:
        nextCell = None
    return nextCell

# simulate one time step in the grid
def simulate(grid):
    copyGrid = deepcopy(grid)
    for x, row in enumerate(copyGrid):
        for y, col in enumerate(copyGrid):
            # if there is a designated cell for water flow, flood it
            cell = flowCell(x,y,copyGrid)
            if cell:
                copyGrid[x][y].update_water_level(20)
    grid = copyGrid


def main():
    pass

if __name__ == '__main__':
    main()