__author__ = ['Phillip Johnson', 'Chad Wilson']

from re import match
_world = {}
_max_x = 0
_max_y = 0

def tile_exists(x, y):
    """Returns the tile at the given coordinates or None if there is no tile.

    :param x: the x-coordinate in the worldspace
    :param y: the y-coordinate in the worldspace
    :return: the tile at the given coordinates or None if there is no tile
    """
    return _world.get((x, y))


def load_tiles():
    """Parses a file that describes the world space into the _world object"""
    global _max_x, _max_y
    with open('resources/map.txt', 'r') as f:
        rows = f.readlines()
    x_max = len(rows[0].split()) # assumes all rows contain the same number of tabs
    _max_x = x_max # added for map
    _max_y = len(rows)  # added for map
    for y in range(len(rows)):
        cols = rows[y].split()
        for x in range(x_max):
            tile_name = cols[x].rstrip()
            _world[(x, y)] = None if match(r'^x+$', tile_name) else getattr(__import__('tiles'), tile_name)(x, y)



