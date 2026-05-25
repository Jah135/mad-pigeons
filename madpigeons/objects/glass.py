import pymunk

from . import polygon
from .entity import FragileEntity
from .constants import (
    BOX_WIDTH,
    SLAB_WIDTH,
    SLAB_XY_RATIO,
    LARGE_PLANK_LENGTH,
    LARGE_PLANK_XY_RATIO,
    LARGE_BALL_RADIUS,
    SMALL_BALL_RADIUS,
)
import assets

# glass properties
GLASS_ELASTICITY = 0.1
GLASS_FRICTION = 0.3
GLASS_DENSITY = 0.6
GLASS_DAMAGE_RESISTANCE = 0.5


class Box(FragileEntity):
    max_health = 10
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.GLASS_BOX_3,
        assets.GLASS_BOX_2,
        assets.GLASS_BOX_1,
        assets.GLASS_BOX_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_rectangle(BOX_WIDTH))
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body


class Wedge(FragileEntity):
    max_health = 10
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.GLASS_WEDGE_3,
        assets.GLASS_WEDGE_2,
        assets.GLASS_WEDGE_1,
        assets.GLASS_WEDGE_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_wedge(BOX_WIDTH))
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body


class Triangle(FragileEntity):
    max_health = 10
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.GLASS_TRIANGLE_3,
        assets.GLASS_TRIANGLE_2,
        assets.GLASS_TRIANGLE_1,
        assets.GLASS_TRIANGLE_0,
    )
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_triangle(BOX_WIDTH))
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body


class Slab(FragileEntity):
    max_health = 10
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.GLASS_SLAB_3,
        assets.GLASS_SLAB_2,
        assets.GLASS_SLAB_1,
        assets.GLASS_SLAB_0,
    )
    texture_dimensions = (SLAB_WIDTH, SLAB_WIDTH // SLAB_XY_RATIO)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, polygon.generate_rectangle(SLAB_WIDTH, SLAB_XY_RATIO))
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body


class LargePlank(FragileEntity):
    max_health = 10
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.LARGE_GLASS_PLANK_3,
        assets.LARGE_GLASS_PLANK_2,
        assets.LARGE_GLASS_PLANK_1,
        assets.LARGE_GLASS_PLANK_0,
    )
    texture_dimensions = (
        LARGE_PLANK_LENGTH,
        LARGE_PLANK_LENGTH // LARGE_PLANK_XY_RATIO,
    )

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, polygon.generate_rectangle(LARGE_PLANK_LENGTH, LARGE_PLANK_XY_RATIO)
        )
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body


class LargeBall(FragileEntity):
    max_health = 10
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.LARGE_GLASS_BALL_3,
        assets.LARGE_GLASS_BALL_2,
        assets.LARGE_GLASS_BALL_1,
        assets.LARGE_GLASS_BALL_0,
    )
    texture_dimensions = (LARGE_BALL_RADIUS * 2, LARGE_BALL_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, LARGE_BALL_RADIUS)
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body


class SmallBall(FragileEntity):
    max_health = 5
    damage_resistance = GLASS_DAMAGE_RESISTANCE
    damage_textures = (
        assets.SMALL_GLASS_BALL_3,
        assets.SMALL_GLASS_BALL_2,
        assets.SMALL_GLASS_BALL_1,
        assets.SMALL_GLASS_BALL_0,
    )
    texture_dimensions = (SMALL_BALL_RADIUS * 2, SMALL_BALL_RADIUS * 2)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, SMALL_BALL_RADIUS)
        shape.density = GLASS_DENSITY
        shape.friction = GLASS_FRICTION
        shape.elasticity = GLASS_ELASTICITY

        return body
