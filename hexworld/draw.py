from PIL import Image, ImageDraw, ImageFont
from grid import Grid
from constants import SIDE_LENGTH, HEX_HEIGHT, HEX_RADIUS, HEX_RECT_HEIGHT, HEX_RECT_WIDTH

# Draw hexagon grid to image
def draw(grid, file_name, color_func, draw_edges=True):
    # Create image
    image = Image.new('RGB', (int(grid.width * HEX_RECT_WIDTH), int(grid.height * (SIDE_LENGTH + HEX_HEIGHT))), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw hexagons
    for x, row in enumerate(grid.grid):
        for y, col in enumerate(row):
            cx = y * HEX_RECT_WIDTH + ( (x % 2) * HEX_RADIUS)
            cy = x * (SIDE_LENGTH + HEX_HEIGHT)
            draw_hexagon(draw, cx, cy, x, y, grid, color_func, draw_edges)

    # Save image
    image.save('bin/' + file_name)

# Draw hexagon to image
def draw_hexagon(draw, cx, cy, x, y, grid, color_func, draw_edges):
    origin = (cx + HEX_RADIUS, cy)
    pointer = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT)
    pointer_2 = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT + SIDE_LENGTH)
    pointer_3 = (cx + HEX_RADIUS, cy + HEX_RECT_HEIGHT)
    pointer_4 = (cx, cy + SIDE_LENGTH + HEX_HEIGHT)
    pointer_5 = (cx, cy + HEX_HEIGHT)

    h = grid.find_hex(x, y)
    draw.polygon([origin,
                  pointer,
                  pointer_2,
                  pointer_3,
                  pointer_4,
                  pointer_5],
                 outline=None,
                 fill=color_func(h))
    
    # Draw edges
    if draw_edges:
        draw_hex_edges(draw, cx, cy, x, y, grid)
    
# Draw hexagon edges to image
def draw_hex_edges(draw, cx, cy, x, y, grid):
    origin = (cx + HEX_RADIUS, cy)
    pointer = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT)
    pointer_2 = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT + SIDE_LENGTH)
    pointer_3 = (cx + HEX_RADIUS, cy + HEX_RECT_HEIGHT)
    pointer_4 = (cx, cy + SIDE_LENGTH + HEX_HEIGHT)
    pointer_5 = (cx, cy + HEX_HEIGHT)

    h = grid.find_hex(x, y)
    draw.line([origin, pointer], fill=(0, 0, 0))
    draw.line([pointer, pointer_2], fill=(0, 0, 0))
    draw.line([pointer_2, pointer_3], fill=(0, 0, 0))
    draw.line([pointer_3, pointer_4], fill=(0, 0, 0))
    draw.line([pointer_4, pointer_5], fill=(0, 0, 0))
    draw.line([pointer_5, origin], fill=(0, 0, 0))

def main():
    # Create grid
    grid = Grid(10, 10)
    # Draw grid
    draw(grid, 'test.png', lambda h: (100, 0, 20), draw_edges=True)

if __name__ == '__main__':
    main()
