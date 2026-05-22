import pymunk
from pygame import transform

from .entity import FragileEntity
from .constants import (
    BOX_WIDTH,
    LARGE_BALL_RADIUS,
    SLAB_WIDTH,
    SLAB_XY_RATIO,
    LARGE_PLANK_LENGTH,
    LARGE_PLANK_XY_RATIO,
)
from .generate import (
    generate_rectangle_polygon_points,
    generate_triangle_polygon_points,
    generate_wedge_polygon_points,
)
import assets

# stone properties
STONE_ELASTICITY = 0.2
STONE_FRICTION = 0.6
STONE_DENSITY = 0.8
STONE_DAMAGE_RESISTANCE = 3


class Box(FragileEntity):
    max_health = 150
    damage_resistance = STONE_DAMAGE_RESISTANCE
    damage_textures = (
        assets.STONE_BOX_3,
        assets.STONE_BOX_2,
        assets.STONE_BOX_1,
        assets.STONE_BOX_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(BOX_WIDTH))
        shape.density = STONE_DENSITY
        shape.friction = STONE_FRICTION
        shape.elasticity = STONE_ELASTICITY

        return body


class Wedge(FragileEntity):
    max_health = 150
    damage_resistance = STONE_DAMAGE_RESISTANCE
    damage_textures = (
        assets.STONE_WEDGE_3,
        assets.STONE_WEDGE_2,
        assets.STONE_WEDGE_1,
        assets.STONE_WEDGE_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_wedge_polygon_points(BOX_WIDTH))
        shape.density = STONE_DENSITY
        shape.friction = STONE_FRICTION
        shape.elasticity = STONE_ELASTICITY

        return body


class Triangle(FragileEntity):
    max_health = 150
    damage_resistance = STONE_DAMAGE_RESISTANCE
    damage_textures = (
        assets.STONE_TRIANGLE_3,
        assets.STONE_TRIANGLE_2,
        assets.STONE_TRIANGLE_1,
        assets.STONE_TRIANGLE_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_triangle_polygon_points(BOX_WIDTH))
        shape.density = STONE_DENSITY
        shape.friction = STONE_FRICTION
        shape.elasticity = STONE_ELASTICITY

        return body


class Slab(FragileEntity):
    max_health = 100
    damage_resistance = STONE_DAMAGE_RESISTANCE
    damage_textures = (
        assets.STONE_SLAB_3,
        assets.STONE_SLAB_2,
        assets.STONE_SLAB_1,
        assets.STONE_SLAB_0,
    )
    texture_dimensions = (SLAB_WIDTH, SLAB_WIDTH // SLAB_XY_RATIO)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(BOX_WIDTH, 2))
        shape.density = STONE_DENSITY
        shape.friction = STONE_FRICTION
        shape.elasticity = STONE_ELASTICITY

        return body


class LargeBall(FragileEntity):
    max_health = 140
    damage_resistance = STONE_DAMAGE_RESISTANCE
    damage_textures = (
        assets.LARGE_STONE_BALL_3,
        assets.LARGE_STONE_BALL_2,
        assets.LARGE_STONE_BALL_1,
        assets.LARGE_STONE_BALL_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, LARGE_BALL_RADIUS)
        shape.density = STONE_DENSITY
        shape.friction = STONE_FRICTION
        shape.elasticity = STONE_ELASTICITY

        return body


class SmallBall(FragileEntity):
    max_health = 80
    damage_resistance = STONE_DAMAGE_RESISTANCE
    damage_textures = (
        assets.SMALL_STONE_BALL_3,
        assets.SMALL_STONE_BALL_2,
        assets.SMALL_STONE_BALL_1,
        assets.SMALL_STONE_BALL_0,
    )
    texture_dimensions = (BOX_WIDTH // 2, BOX_WIDTH // 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, LARGE_BALL_RADIUS // 2)
        shape.density = STONE_DENSITY
        shape.friction = STONE_FRICTION
        shape.elasticity = STONE_ELASTICITY

        return body
