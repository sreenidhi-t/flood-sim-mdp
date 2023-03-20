# Flood Sim MDP

## World Elevation Map
Below is the elevation map for the model hexworld that was generated using Perlin noise. The darker areas correspond to lower elevation and lighter areas correspond to higher elevation.
![plot](./hexworld/bin/evac_out/test.png)

## Flooding Simulation
This is a gif of the water dynamics simulated in our world over 20 timesteps. The blue indicates water accumulation, red indicates a flooded cell (i.e. water level has exceeded floor threshold), and green represents a cell with a drainage failure.
![plot](./hexworld/bin/sim_test_outputs/flood.gif)

## Evacuation Policy
Here, the flood simulation is overlayed with the online evacuation policy that was generated using the MCTS-DPW algorithm. Cells with white outlines indicate that they have been evacuated.
![plot](./hexworld/bin/evac_out/evac.gif)