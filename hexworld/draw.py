from PIL import Image, ImageDraw, ImageFont
from world import World
from constants import SIDE_LENGTH, HEX_HEIGHT, HEX_RADIUS, HEX_RECT_HEIGHT, HEX_RECT_WIDTH, FLOOD_LEVEL,MAX_ELEV,MIN_ELEV

# Draw hexagon grid to image
def draw(world, file_name, color_func, draw_edges=True):
    # Create image
    image = Image.new('RGB', (int(world.width * HEX_RECT_WIDTH), int(world.height * (SIDE_LENGTH + HEX_HEIGHT))), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw hexagons
    for x, row in enumerate(world.grid):
        for y, col in enumerate(row):
            cx = y * HEX_RECT_WIDTH + ( (x % 2) * HEX_RADIUS)
            cy = x * (SIDE_LENGTH + HEX_HEIGHT)
            draw_hexagon(draw, cx, cy, x, y, world, color_func, draw_edges)

    # Save image
    image.save('bin/' + file_name)

# Define color function
def color_func_elevation(h):
    min_elevation = MIN_ELEV
    max_elevation = MAX_ELEV

    # Normalize elevation
    e  = (h.elevation - min_elevation) / (max_elevation - min_elevation)
    # Calculate color
    r = int(255 * e)
    g = int(255 * e)
    b = int(255 * e)
    return (r, g, b)

def color_func_water(h):
    min_water = 0
    max_water = FLOOD_LEVEL
    if h.is_flooded:
        return (255,0,0)

    if h.drain_status is False:
        return (0, 255, 0)

    # Normalize water
    w = (h.water_level - min_water) / (max_water - min_water)
    # Calculate as shades of blue
    r = int(0)
    g = int(0)
    b = int(255 * w)
    return (r, g, b)


# Draw hexagon to image
def draw_hexagon(draw, cx, cy, x, y, world, color_func, draw_edges):
    origin = (cx + HEX_RADIUS, cy)
    pointer = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT)
    pointer_2 = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT + SIDE_LENGTH)
    pointer_3 = (cx + HEX_RADIUS, cy + HEX_RECT_HEIGHT)
    pointer_4 = (cx, cy + SIDE_LENGTH + HEX_HEIGHT)
    pointer_5 = (cx, cy + HEX_HEIGHT)

    h = world.find_hex(x, y)
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
        draw_hex_edges(draw, cx, cy, x, y, world)
    
# Draw hexagon edges to image
def draw_hex_edges(draw, cx, cy, x, y, world):
    origin = (cx + HEX_RADIUS, cy)
    pointer = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT)
    pointer_2 = (cx + HEX_RECT_WIDTH, cy + HEX_HEIGHT + SIDE_LENGTH)
    pointer_3 = (cx + HEX_RADIUS, cy + HEX_RECT_HEIGHT)
    pointer_4 = (cx, cy + SIDE_LENGTH + HEX_HEIGHT)
    pointer_5 = (cx, cy + HEX_HEIGHT)

    h = world.find_hex(x, y)
    draw.line([origin, pointer], fill=(0, 0, 0))
    draw.line([pointer, pointer_2], fill=(0, 0, 0))
    draw.line([pointer_2, pointer_3], fill=(0, 0, 0))
    draw.line([pointer_3, pointer_4], fill=(0, 0, 0))
    draw.line([pointer_4, pointer_5], fill=(0, 0, 0))
    draw.line([pointer_5, origin], fill=(0, 0, 0))

def main():
    # Create grid
    world = World(20, 20)
    # Draw grid
    # Use color_func_elevation to draw elevation
    draw(world, 'test.png', color_func_elevation, draw_edges=True)
    # draw(grid, 'test.png', lambda h: (int(h.elevation * 10), int(h.elevation * 10), int(h.elevation * 10)), draw_edges=True)
    # draw(grid, 'test.png', lambda h: (100, 0, 20), draw_edges=True)

if __name__ == '__main__':
    main()
