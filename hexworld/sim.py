from grid import Grid

# determine which adjacent cell the water flows into
def flowCell(x,y,grid):
    currCell = grid.find_hex(x,y)
    



def main():
    # Create grid
    grid = Grid(10, 10)
    # Draw grid
    draw(grid, 'test.png', lambda h: (100, 0, 20), draw_edges=True)

if __name__ == '__main__':
    main()