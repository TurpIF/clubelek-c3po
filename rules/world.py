'''
Define all properties about the map
Dimension are in mm and begin from (0, 0) to (MAP_WIDTH, MAP_HEIGHT).
The width correspond to the longest side. And the height the other.
During the 2014-2015 cup, the starts are on the height sides.
The external walls are not included as margin.
'''

width = 3000
height = 2000

popcorn_boxes_geometry = {
    'width': 70,
    'height': 70
}

popcorn_boxes = set([
    (300, popcorn_boxes_geometry['height'] / 2),
    (600, popcorn_boxes_geometry['height'] / 2)
])

walls = set([
    (0, 800 - 22), (400, 800),
    (0, 1200) (400, 1200 + 22),
    (0, 800), (70, 1200),
    (300 - popcorn_boxes_geometry['width'] / 2, 0), (300 + popcorn_boxes_geometry['height'] / 2, 70),
    (600 - popcorn_boxes_geometry['width'] / 2, 0), (600 + popcorn_boxes_geometry['height'] / 2, 70)
])
