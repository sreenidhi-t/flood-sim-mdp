from world import World
import numpy as np
from copy import deepcopy
from draw import draw, color_func_water, color_func_elevation

# class CopyGrid(World):
#     pass

# determine which adjacent cell the water flows into
def flowCell(x,y,grid):    
    # get the current cell from the grid and its neighbors
    currCell = grid[x][y]
    neighbors = currCell.get_neighbors_all()
    # compile a list of neighbors with lower elevations
    lower = []
    for neighbor in neighbors:
        # Check if there is a neighbor with a lower elevation
        if (neighbor != None) and (neighbor.elevation <= currCell.elevation) and not neighbor.is_flooded:
            lower.append(neighbor)
    # given the current cell has water, identify the next cell it flows to
    if len(lower) > 0 and currCell.water_level > 0:
        nextCell = np.random.choice(lower)
    else:
        nextCell = None
    return nextCell

# simulate water flow for one time step in the grid 
def simulate(world):
    copyWorld = deepcopy(world)   
    copyGrid = copyWorld.grid
    # Iterate thorugh base grid and update copy
    for x, row in enumerate(world.grid):
        for y, col in enumerate(world.grid):
            # if there is a designated cell for water flow, flood it
            cell = flowCell(x,y,world.grid)
            if cell:
                copyGrid[cell.x][cell.y].update_water_level(20)
                print("Cell found: {},{}".format(cell.x,cell.y))
    return copyWorld
    

# function to simulate water movement for t timesteps
def simFlow(world, timeSteps, x0, y0):
    # set initial condition for the desired cell
    world.grid[x0][y0].update_water_level(20)
    # print(world.grid[x0][y0].water_level)
    # draw(world, 'sim_test_pngs/floodinit.png', color_func = color_func_water, draw_edges=True)
    for t in range(timeSteps):
        world = simulate(world)
        draw(world, 'sim_test_pngs/flood{}.png'.format(t), color_func = color_func_water, draw_edges=True)
        print("Time step {} complete".format(t))
        

def main():
    world = World(30,30)
    # Draw world map
    draw(world, 'sim_test_pngs/map.png', color_func = color_func_elevation, draw_edges=True)
    simFlow(world, 10, 10, 0)

if __name__ == '__main__':
    main()