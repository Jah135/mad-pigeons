import pymunk

BOX_WIDTH = 50
LARGE_BALL_RADIUS = BOX_WIDTH // 2
SMALL_BALL_RADIUS = LARGE_BALL_RADIUS // 2

SLAB_WIDTH = 50
SLAB_XY_RATIO = 2

LARGE_PLANK_LENGTH = 100
LARGE_PLANK_XY_RATIO = 8


def get_collision_force(arbiter: pymunk.Arbiter) -> float:
    shape_a, shape_b = arbiter.shapes
    total_mass = shape_a.mass + shape_b.mass
    return arbiter.total_impulse.length / total_mass
