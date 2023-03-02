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
    return np.random.choice(lower)




def main():
    pass

if __name__ == '__main__':
    main()