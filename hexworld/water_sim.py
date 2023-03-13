from world import World
import numpy as np
from copy import deepcopy
from draw import draw, color_func_water, color_func_elevation
from constants import PRECIP_RATE, FLOW_PER_LEVEL, PROB_DRAIN_FAIL, SIM_TIME, DRAIN_FAIL_LEVEL
from PIL import Image


# generate neighbors of a cell that are lower in elevation
def low_neighbors(x,y,grid):    
    # get the current cell from the grid and its neighbors
    currCell = grid[x][y]
    neighbors = currCell.get_neighbors_all()
    # compile a list of neighbors with lower elevations
    lower = []
    for neighbor in neighbors:
        # Check if there is a neighbor with a lower elevation based on the difference in height of water
        if (neighbor != None) and ((neighbor.elevation + neighbor.water_level) < (currCell.elevation + currCell.water_level)):
            lower.append(neighbor)
    return lower

# simulate water flow for one time step in the grid 
def simFlow(world):
    copyWorld = deepcopy(world)   
    copyGrid = copyWorld.grid
    # Iterate thorugh base grid and update copy
    for x, row in enumerate(world.grid):
        for y, col in enumerate(world.grid):
            # if there is water in the current cell determine the water's movement
            if world.grid[x][y].water_level > 0:
                lower_neighbors = low_neighbors(x,y,world.grid)
                # if there are lower neighbors for the water to move to,
                # determine how much water moves to each cell
                if len(lower_neighbors) > 0:
                    flow_rates = calculateFlow(world.grid[x][y], lower_neighbors)
                    for i, cell in enumerate(lower_neighbors):
                        water_in = flow_rates[i] * world.grid[x][y].water_level
                        copyGrid[cell.x][cell.y].add_water(water_in)
                        copyGrid[x][y].remove_water(water_in)
                # print("Cell found: {},{}".format(cell.x,cell.y))
    return copyWorld

def calculateFlow(source, neighbors):
    flow_rates = np.array([])
    for neighbor in neighbors:
        # Find difference in elevation between source and neighbor
        delta_elevation = (source.elevation + source.water_level) - (neighbor.elevation + neighbor.water_level)
        # Calculate flow rate based on difference in elevation
        flow_rate = delta_elevation * FLOW_PER_LEVEL
        flow_rates = np.append(flow_rates, flow_rate)
    # Normalized
    flow_rates = flow_rates / np.sum(flow_rates)
    return flow_rates

def randDrainFail(world):
    copyWorld = deepcopy(world)   
    copyGrid = copyWorld.grid
    # Iterate thorugh base grid and update copy
    for x, row in enumerate(world.grid):
        for y, col in enumerate(world.grid):
            # TODO: Update fail rate to either elavation or water level
            waterThresholdPassed = copyGrid[x][y].water_level >= DRAIN_FAIL_LEVEL
            drainFail = np.random.uniform(0,1)
            if copyGrid[x][y].drain_status and drainFail <= PROB_DRAIN_FAIL and waterThresholdPassed:
                copyGrid[x][y].drain_status = False
    return copyWorld

def simDrain(world):
    copyWorld = deepcopy(world)   
    copyGrid = copyWorld.grid
    # Iterate thorugh base grid and update copy
    for x, row in enumerate(world.grid):
        for y, col in enumerate(world.grid):
            # for each hex cell, update the flow out based on the drain rate
            copyGrid[x][y].drain_water()
    return copyWorld

def simRain(world, precipRate):
    copyWorld = deepcopy(world)   
    copyGrid = copyWorld.grid
    # Iterate thorugh base grid and update copy
    for x, row in enumerate(world.grid):
        for y, col in enumerate(world.grid):
            # for each hex cell, update the flow in based on the downfall rate
            copyGrid[x][y].add_water(precipRate)
    # print(copyWorld.hexes[0].water_level)

    return copyWorld

# function to simulate water movement for t timesteps
def simulate(world, timeSteps):
    # storage for animation
    image_files = []

    # set initial condition for the desired cell
    draw(world, 'sim_test_outputs/floodinit.png', color_func = color_func_water, draw_edges=True)
    image_files.append('bin/sim_test_outputs/floodinit.png')
    # loop through all time steps
    
    for t in range(timeSteps):
        # one time step worth of rain
        world = simRain(world, PRECIP_RATE)
        # one time step worth of flooding
        world = simFlow(world)
        # one time step worth of randomized drain clogging
        world = randDrainFail(world)
        # one time step worth of drainage
        world = simDrain(world)
        # generate image and store file name for animation later
        draw(world, 'sim_test_outputs/flood{}.png'.format(t), color_func = color_func_water, draw_edges=True)
        image_files.append('bin/sim_test_outputs/flood{}.png'.format(t))

        # print("Time step {} complete".format(t))
    
    animate(image_files,"bin/sim_test_outputs/flood.gif")


def animate(inPics, outGif):
    # set gif size and mode
    with Image.open(inPics[0]) as pic:
        size = pic.size
        mode = pic.mode

    # collate image objects
    slides = []
    for pic_file in inPics:
        with Image.open(pic_file) as pic:
            # resize
            if pic.size != size:
                pic = pic.resize(size)
            slides.append(pic.convert(mode))
    
    # compile into a gif
    slides[0].save(outGif,save_all=True, append_images=slides[1:], duration = 200, loop = 0)
    

def main():
    world = World(20, 20)
    # Draw world map
    draw(world, 'sim_test_outputs/map.png', color_func = color_func_elevation, draw_edges=True)
    simulate(world, SIM_TIME)

if __name__ == '__main__':
    main()