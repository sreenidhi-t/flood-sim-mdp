import math
from PIL import ImageColor


# Constants for Drawing Grid
HEXAGON_ANGLE = 28 * math.pi / 180;  # 30 degrees
SIDE_LENGTH = 17
BOARD_WIDTH = 100;
BOARD_HEIGHT = BOARD_WIDTH;
HEX_HEIGHT = math.sin(HEXAGON_ANGLE) * SIDE_LENGTH
HEX_RADIUS = math.cos(HEXAGON_ANGLE) * SIDE_LENGTH
HEX_RECT_HEIGHT = SIDE_LENGTH + 2 * HEX_HEIGHT
HEX_RECT_WIDTH = 2 * HEX_RADIUS

## Any other constants useful for simulation
FLOOD_LEVEL = 2
SIM_TIME = 20
PRECIP_RATE = 0.5 # 6 in/hr = max recorded rainfall rate from Claudette
MAX_DRAIN_RATE = 1.5 # 
FLOW_PER_LEVEL = 0.05
PROB_DRAIN_FAIL = 0.0513/SIM_TIME # calculated lambda from exponential CDF of 0.05 #TODO: Update for new grid size
MAX_ELEV = 250  # average max elevation of cities along the Gulf Coast
MIN_ELEV = 0  # minimum elevation of any cities along the Gulf Coast
MAX_ELEV_DEV = 5
DRAIN_FAIL_LEVEL = FLOOD_LEVEL/4 # level after which drain failure can occur

## MDP Constants
MAX_EVAC_CELLS = 3 # maximum number of cells that can be evacuated
DISCOUNT = 0.9
R_FLOOD_NO_EVAC = -10e-1 # reward for flooding per population
# R_DRY_NO_EVAC = 1e-1 # reward for evacuating per population
R_FLOOD_EVAC = 5e-1 # reward for surviving per population
# R_DRY_EVAC = -2e-1 # reward for evacuating per population
R_FLOOD = 10e-1
R_EVAC = -2e-1
MCTS_RUN = True # boolean to alter run mode as MCTS or Random

## MCTS-DPW Constants
MAX_DEPTH = 5 # maximum depth of tree defined by levels of actions 
NUM_SIMS = 200 # cumulative number of simulations
K = 2 # DPW coefficient
ALPHA = 0.1 # DPW progressive widening parameter
C = 0.05 # exploration constant
MAX_ACTION_SPACE = 5 # maximum number of actions to consider at each node
MAX_STATE_SPACE = 5 # maximum number of states to consider at each node
ROLL_STEPS = 10 # number of steps to roll out for each simulation