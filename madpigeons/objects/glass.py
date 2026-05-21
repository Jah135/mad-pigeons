import pymunk
from pygame import transform

from .entity import FragileEntity
from .constants import (
    STANDARD_BOX_SIZE,
    STANDARD_BALL_RADIUS,
    STANDARD_THICK_PLANK_LENGTH,
    STANDARD_THIN_PLANK_LENGTH,
)
from .generate import (
    generate_rectangle_polygon_points,
    generate_triangle_polygon_points,
    generate_wedge_polygon_points,
)
import assets

# glass properties
STANDARD_GLASS_ELASTICITY = 0.1
STANDARD_GLASS_FRICTION = 0.1
STANDARD_GLASS_DENSITY = 0.9
STANDARD_GLASS_DAMAGE_RESISTANCE = 1.3


class Box(FragileEntity):
    max_health = 30
    damage_resistance = STANDARD_GLASS_DAMAGE_RESISTANCE
    damage_frames = (assets.GLASS_BOX_0,)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_GLASS_DENSITY
        shape.friciton = STANDARD_GLASS_FRICTION
        shape.elasticity = STANDARD_GLASS_ELASTICITY

        return body


class Wedge(FragileEntity):
    max_health = 30
    damage_resistance = STANDARD_GLASS_DAMAGE_RESISTANCE
    damage_frames = ()

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_wedge_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_GLASS_DENSITY
        shape.friciton = STANDARD_GLASS_FRICTION
        shape.elasticity = STANDARD_GLASS_ELASTICITY

        return body


class Triangle(FragileEntity):
    max_health = 30
    damage_resistance = STANDARD_GLASS_DAMAGE_RESISTANCE
    damage_frames = ()

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_triangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_GLASS_DENSITY
        shape.friciton = STANDARD_GLASS_FRICTION
        shape.elasticity = STANDARD_GLASS_ELASTICITY

        return body


class Slab(FragileEntity):
    max_health = 20
    damage_resistance = STANDARD_GLASS_DAMAGE_RESISTANCE
    damage_frames = ()

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE, 2)
        )
        shape.density = STANDARD_GLASS_DENSITY
        shape.friciton = STANDARD_GLASS_FRICTION
        shape.elasticity = STANDARD_GLASS_ELASTICITY

        return body


class LargeBall(FragileEntity):
    max_health = 30
    damage_resistance = STANDARD_GLASS_DAMAGE_RESISTANCE
    damage_frames = ()

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, STANDARD_BALL_RADIUS)
        shape.density = STANDARD_GLASS_DENSITY
        shape.friciton = STANDARD_GLASS_FRICTION
        shape.elasticity = STANDARD_GLASS_ELASTICITY

        return body


class SmallBall(FragileEntity):
    max_health = 15
    damage_resistance = STANDARD_GLASS_DAMAGE_RESISTANCE
    damage_frames = ()

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, STANDARD_BALL_RADIUS // 2)
        shape.density = STANDARD_GLASS_DENSITY
        shape.friciton = STANDARD_GLASS_FRICTION
        shape.elasticity = STANDARD_GLASS_ELASTICITY

        return body
