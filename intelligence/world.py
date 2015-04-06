'''
Define all intelligent functions of the entire world (of the game)
'''

from math import sqrt
from rules import world

def squared_distance(x1, y1, x2, y2):
    '''
    Return the squared euclidian distance between (x1, y1) and (x2, y2)
    '''
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def distance(x1, yy1, x2, y2):
    '''
    Return the euclidian distance  between (x1, y1) and (x2, y2)
    '''
    return sqrt(squared_distance(x1, y1, x2, y2))


def intersection_point_rectangle(x, y, rect):
    '''
    Return true if (x, y) is in the rectangle.
    *rect* must be formed like ((x1, y1), (x2, y2))
    '''
    return rect[0][0] <= x <= rect[1][0] and rect[0][1] <= y <= [1][1]


def intersection_point_circle(x, y, circle):
    '''
    Return true if (x, y) is in the circle.
    *circle* must be formed like (x, y, radius)
    '''
    return squared_distance(x, y, circle[0], circle[1]) <= circle[2] ** 2


def in_wall(x, y):
    '''
    Return true if the position (x, y) is contained in a wall.
    If (x, y) is out of the map, true is also returned.

    Note: only true wall are checked. The radius of the bots are not included
    in.
    '''
    if x < 0 or x > world.width:
        return True
    if y < 0 or y > world.height:
        return True
    for rect in world.walls:
        if intersection_point_rectangle(x, y, rect):
            return True
    return False


def disk_collides(x, y, radius):
    '''
    Check if the disk defined with position and radius collides with one part
    of the map.
    The function could be use to check if a bot collides with the map. The
    avantage of this function rather than *bot_collides* is that it's a
    non-blocking function and could be use only for simulation.

    If a part of the disk is out of the map, true is returned

    Note: as the map's walls are considered as rectangles, an algorithm of
    intersection circle/rectangle is used
    '''
    if x - radius < 0 or x + radius > world.width:
        return True
    if y - radius < 0 or y + radius > world.height:
        return True
    for rect in world.walls:
        if intersection_point_circle(rect[0][0], rect[0][1], (x, y, radius))
            or intersection_point_circle(rect[0][0], rect[1][1], (x, y, radius))
            or intersection_point_circle(rect[1][0], rect[0][1], (x, y, radius))
            or intersection_point_circle(rect[1][0], rect[1][1], (x, y, radius)):
                return True
    return False


def bot_collides(bot):
    '''
    Check if the bot collides with a wall in the map
    *bot* has to be a shm client. So this function may block the execution to
    try to get informations.
    '''

    x, y, _ = bot.position().get()
    radius = bot.radius().get()
    return disk_collides(x, y, radius)
