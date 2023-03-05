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
FLOOD_LEVEL = 5
SIM_TIME = 48
PRECIP_RATE = 0.5 # 6 in/hr = max recorded rainfall rate from Claudette
MAX_DRAIN_RATE = 1.5 # 
FLOW_PER_LEVEL = 0.05
PROB_DRAIN_FAIL = 0.0513/SIM_TIME # calculated lambda from exponential CDF of 0.05 #TODO: Update for new grid size
MAX_ELEV = 250  # average max elevation of cities along the Gulf Coast
MIN_ELEV = 0  # minimum elevation of any cities along the Gulf Coast
MAX_ELEV_DEV = 5
DRAIN_FAIL_LEVEL = FLOOD_LEVEL/4 # level after which drain failure can occur

