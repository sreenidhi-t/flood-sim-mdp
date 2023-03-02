from grid import Grid
import numpy as np

# determine which adjacent cell the water flows into
def flowCell(x,y,grid):
    currCell = grid.find_hex(x,y)
    neighbors = currCell.get_neighbors_all()
    lower = []
    for neighbor in neighbors:
        if neighbor.elevation <= currCell.elevation:
            lower += neighbor
    if currCell.water_level > 0:
        nextCell = np.random.choice(lower)
    else:
        nextCell = None
    return nextCell

# simulate one time step in the grid
def simulate():
    pass


def main():
    pass

if __name__ == '__main__':
    main()