import pymunk
from pygame import transform

from .entity import FragileEntity
from .dimensions import STANDARD_BOX_SIZE, STANDARD_BALL_RADIUS, STANDARD_THICK_PLANK_LENGTH, STANDARD_THIN_PLANK_LENGTH, generate_rectangle_polygon_points, generate_triangle_polygon_points, generate_wedge_polygon_points
from .. import assets

# stone properties
STANDARD_STONE_ELASTICITY = 0.2
STANDARD_STONE_FRICTION = 0.6
STANDARD_STONE_DENSITY = 0.8
STANDARD_STONE_DAMAGE_RESISTANCE = 3


class Box(FragileEntity):
    max_health = 150
    damage_resistance = STANDARD_STONE_DAMAGE_RESISTANCE
    damage_frames = (assets.STONE_BOX_3, assets.STONE_BOX_2,
                     assets.STONE_BOX_1, assets.STONE_BOX_0)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        return body


class Wedge(FragileEntity):
    max_health = 150
    damage_resistance = STANDARD_STONE_DAMAGE_RESISTANCE
    damage_frames = (assets.STONE_WEDGE_3, assets.STONE_WEDGE_2,
                     assets.STONE_WEDGE_1, assets.STONE_WEDGE_0)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_wedge_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        return body


class Triangle(FragileEntity):
    max_health = 150
    damage_resistance = STANDARD_STONE_DAMAGE_RESISTANCE
    damage_frames = (assets.STONE_TRIANGLE_3, assets.STONE_TRIANGLE_2,
                     assets.STONE_TRIANGLE_1, assets.STONE_TRIANGLE_0)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_triangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        return body


class Slab(FragileEntity):
    max_health = 100
    damage_resistance = STANDARD_STONE_DAMAGE_RESISTANCE
    damage_frames = (assets.STONE_SLAB_3, assets.STONE_SLAB_2,
                     assets.STONE_SLAB_1, assets.STONE_SLAB_0)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE, 2))
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        return body


class LargeBall(FragileEntity):
    max_health = 140
    damage_resistance = STANDARD_STONE_DAMAGE_RESISTANCE
    damage_frames = (assets.LARGE_STONE_BALL_3, assets.LARGE_STONE_BALL_2,
                     assets.LARGE_STONE_BALL_1, assets.LARGE_STONE_BALL_0)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, STANDARD_BALL_RADIUS)
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        return body


class SmallBall(FragileEntity):
    max_health = 80
    damage_resistance = STANDARD_STONE_DAMAGE_RESISTANCE
    damage_frames = (assets.SMALL_STONE_BALL_3, assets.SMALL_STONE_BALL_2,
                     assets.SMALL_STONE_BALL_1, assets.SMALL_STONE_BALL_0)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, STANDARD_BALL_RADIUS // 2)
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        return body
