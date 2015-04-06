from functools import partial
from shm.properties import Array, Point, Bool, Float, Int

BOT_RADIUS = 300 # in mm

# properties
position = Point(0, 0, 0)
position_order = Point(0, 0, 0)
radius = Int(BOT_RADIUS)
left_arm = Float(0)
left_arm_order = Float(0)
left_claw = Float(0)
right_arm = Float(0)
right_claw = Float(0)
top_stop = Bool(False)
bottom_stop = Bool(False)

# exposition
property_descriptions = (
        ('position',       lambda: position),
        ('position_order', lambda: position_order),
        ('radius',         lambda: radius),
        ('left_arm',       lambda: left_arm),
        ('left_arm_order', lambda: left_arm_order),
        ('left_claw',      lambda: left_claw),
        ('right_arm',      lambda: right_arm),
        ('right_claw',     lambda: right_claw),
        ('top_stop',       lambda: top_stop),
        ('bottom_stop',    lambda: bottom_stop),
        )
