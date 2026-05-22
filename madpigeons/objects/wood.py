import pymunk

from . import polygon
from .entity import FragileEntity
from .constants import (
    BOX_WIDTH,
    LARGE_BALL_RADIUS,
    SMALL_BALL_RADIUS,
    SLAB_WIDTH,
    SLAB_XY_RATIO,
    LARGE_PLANK_LENGTH,
    LARGE_PLANK_XY_RATIO,
)
import assets

# wood properties
WOOD_ELASTICITY = 0.5
WOOD_FRICTION = 0.8
WOOD_DENSITY = 0.4
WOOD_DAMAGE_RESISTANCE = 1.1


class Box(FragileEntity):
    max_health = 90
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.WOOD_BOX_3,
        assets.WOOD_BOX_2,
        assets.WOOD_BOX_1,
        assets.WOOD_BOX_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_rectangle(BOX_WIDTH))
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body


class Wedge(FragileEntity):
    max_health = 90
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.WOOD_WEDGE_3,
        assets.WOOD_WEDGE_2,
        assets.WOOD_WEDGE_1,
        assets.WOOD_WEDGE_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_wedge(BOX_WIDTH))
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body


class Triangle(FragileEntity):
    max_health = 90
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.WOOD_TRIANGLE_3,
        assets.WOOD_TRIANGLE_2,
        assets.WOOD_TRIANGLE_1,
        assets.WOOD_TRIANGLE_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_triangle(BOX_WIDTH))
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body


class Slab(FragileEntity):
    max_health = 50
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.WOOD_SLAB_3,
        assets.WOOD_SLAB_2,
        assets.WOOD_SLAB_1,
        assets.WOOD_SLAB_0,
    )
    texture_dimensions = (SLAB_WIDTH, SLAB_WIDTH // SLAB_XY_RATIO)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, polygon.generate_rectangle(SLAB_WIDTH, SLAB_XY_RATIO)
        )
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body


class LargePlank(FragileEntity):
    max_health = 30
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.LARGE_WOOD_PLANK_3,
        assets.LARGE_WOOD_PLANK_2,
        assets.LARGE_WOOD_PLANK_1,
        assets.LARGE_WOOD_PLANK_0,
    )
    texture_dimensions = (
        LARGE_PLANK_LENGTH,
        LARGE_PLANK_LENGTH // LARGE_PLANK_XY_RATIO,
    )

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body,
            polygon.generate_rectangle(
                LARGE_PLANK_LENGTH, LARGE_PLANK_XY_RATIO),
        )
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body


class LargeBall(FragileEntity):
    max_health = 70
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.LARGE_WOOD_BALL_3,
        assets.LARGE_WOOD_BALL_2,
        assets.LARGE_WOOD_BALL_1,
        assets.LARGE_WOOD_BALL_0,
    )
    texture_dimensions = (LARGE_BALL_RADIUS * 2, LARGE_BALL_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, LARGE_BALL_RADIUS)
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body


class SmallBall(FragileEntity):
    max_health = 30
    damage_resistance = WOOD_DAMAGE_RESISTANCE
    damage_textures = (
        assets.SMALL_WOOD_BALL_3,
        assets.SMALL_WOOD_BALL_2,
        assets.SMALL_WOOD_BALL_1,
        assets.SMALL_WOOD_BALL_0,
    )
    texture_dimensions = (SMALL_BALL_RADIUS * 2, SMALL_BALL_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, SMALL_BALL_RADIUS)
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body
