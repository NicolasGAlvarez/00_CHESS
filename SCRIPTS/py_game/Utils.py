import os
import pygame
from chess.Utils import get_position_by_index, get_index_by_position
from math import floor

def load_image(name):
    fullname = os.path.join('RESOURCES', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
    image = image.convert_alpha()
    return image, image.get_rect()

def to_pygame(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], height - coords[1])

def get_coords_by_position(position):
    x_offset = 18
    y_offset = 18
    screen = pygame.display.get_surface()
    width = screen.get_width() - x_offset * 2
    height = screen.get_height() - y_offset * 2
    cell_size = width/8
    index = get_index_by_position(position)
    x = x_offset + index % 8 * cell_size + cell_size / 2
    y = y_offset + floor(index / 8) * cell_size
    return to_pygame((x,y), height)