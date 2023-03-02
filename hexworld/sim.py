from grid import Grid




def main():
    # Create grid
    grid = Grid(10, 10)
    # Draw grid
    draw(grid, 'test.png', lambda h: (100, 0, 20), draw_edges=True)

if __name__ == '__main__':
    main()