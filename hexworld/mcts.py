from world import World
from water_sim import simRain, simDrain, simFlow, randDrainFail
from constants import FLOOD_LEVEL, MAX_EVAC_CELLS, PRECIP_RATE, R_DRY_EVAC, R_DRY_NO_EVAC, R_FLOOD_EVAC, R_FLOOD_NO_EVAC
import numpy as np
import itertools
import random
from copy import deepcopy

# Node class for MCTS tree
class Node:
    def __init__(self, state: World):
        self.state = None
        self.action = None
        self.parent = None
        self.children = []
        self.visits = 0
        self.reward = 0
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def update(self, reward):
        self.visits += 1
        self.reward += reward

       
# MTCS Class
class MCTS:

    def __init__(self, root: World):
        self.root = None  # State to perform MTCS on
        self.depth = 0  # Depth of tree
        self.m = 0  # Number of simulations to run
        self.c = 0  # Exploration constant
        self.tree = None  # Tree of nodes

    def get_next_state(self, state: World, action):
        # Create a copy of the current state
        next_state = deepcopy(state)
        # Perform evacuation action
        next_state.evacWorld(action)
        # one time step worth of rain
        next_state = simRain(next_state, PRECIP_RATE)
        # one time step worth of flooding
        next_state = simFlow(next_state)
        # one time step worth of randomized drain clogging
        next_state = randDrainFail(next_state)
        # one time step worth of drainage
        next_state = simDrain(next_state)

        return next_state

    def narrow_action_space(self, state: World):
        # Get hexes with water level atleast 25% of flood level and not already flooded
        hexes = state.hexes
        hex_space = [h for h in hexes if (h.water_level > 0.25*FLOOD_LEVEL) and (not h.is_flooded)]

        # Return x, y, coordinates of hexes in hex_space
        coord_space = [(h.x, h.y) for h in hex_space]
        return coord_space
    
    def calculate_reward(self, state: World, action):
        reward = 0
        next_state = self.get_next_state(state, action)
        print(action)
        for hex in state.hexes:
            x, y = hex.x, hex.y
            # evacuated and flooded
            if (x,y) in action and next_state.grid[x][y].is_flooded:
                reward += R_FLOOD_EVAC*hex.population
            # evacuated and not flooded
            if (x, y) in action and not next_state.grid[x][y].is_flooded:
                reward += R_DRY_EVAC*hex.population
            # not evacuated and flooded
            if (x,y) not in action and next_state.grid[x][y].is_flooded:
                reward += R_FLOOD_NO_EVAC*hex.population
            # not evacuated and not flooded
            if (x,y) not in action and not next_state.grid[x][y].is_flooded:
                reward += R_DRY_NO_EVAC*hex.population
        return reward
    
    
    def random_rollout(self, state: World, steps):
        # create a copy of our state after taking a current action
        rollout_state = deepcopy(state)
        # rollout for a certain number of states
        utility = 0
        for i in range(steps):
            # select random action (i.e. select some number of random hexes to evacuate)
            action_space = self.narrow_action_space(rollout_state)
            if len(action_space) < MAX_EVAC_CELLS:
                evac_hexes = action_space
            else:
                evac_hexes = random.choices(action_space, k=MAX_EVAC_CELLS)
            # calculate reward for this action step and add to the total utility
            utility += self.calculate_reward(rollout_state, evac_hexes)
            # get the next state and repeat
            rollout_state = self.get_next_state(rollout_state, evac_hexes)
        return utility

    def hallucinate(self, parent):
        # Get action space
        coord_space = self.narrow_action_space(parent.state)
        # Create combinations of all actions
        action_space = []
        
        if len(coord_space) < MAX_EVAC_CELLS:
            for i in range(0, len(coord_space) + 1):
                action_space.append(itertools.combinations(coord_space), i)
        else:
            for i in range(0, MAX_EVAC_CELLS + 1):
                action_space.append(itertools.combinations(coord_space), i)

        # Randomly choose m actions from action space
        if len(action_space) < self.m:
            actions = action_space
        else:
            actions = random.choices(action_space, k=self.m)
               
        
        # For each action, get next state, then random rollout
        for action in actions:
            # Get next state
            next_state = self.get_next_state(parent.state, action)
            # Calculate reward
            reward = self.random_rollout(next_state, 10)
            # Create new node
            new_node = Node(next_state)
            new_node.action = action
            new_node.parent = parent
            new_node.update(reward)
            parent.add_child(new_node)
            # Update tree
            self.tree.append(new_node)

        # caluclate UCB1 heuristic for each node in parent's children
        ucb1_values = [self.ucb1(child) for child in parent.children]
        # determine best action from index of maximum UCB1 value
        best_action = parent.children[ucb1_values.index(max(ucb1_values))].action
        # return best action
        return best_action
   
    # function to calulate the UCB1 exploration heuristic for a node
    def ucb1(self, node):
        if node.visits == 0:
            return float("inf")
        # otherwise, return the UCB1 heuristic for the node
        return (node.reward) + self.c * np.sqrt(np.log(node.parent.visits) / node.visits)
    
    


def main():
    # Create a world
    world = World(20, 20)
    # Create a MCTS object
    mcts = MCTS(world)
    # Get action space
    a = mcts.random_rollout(world, 10)
    print(a)

if __name__ == "__main__":
    main()