import pymunk
from pygame import transform

from .entity import FragileEntity
from .generate import generate_rectangle_polygon_points
from .constants import STANDARD_BOX_SIZE
from .wood import (
    STANDARD_WOOD_DENSITY,
    STANDARD_WOOD_ELASTICITY,
    STANDARD_WOOD_FRICTION,
)
import assets


class TNT(FragileEntity):
    max_health = 50
    damage_resistance = 1.3
    damage_textures = (assets.TNT,)
    texture_dimensions = (STANDARD_BOX_SIZE, STANDARD_BOX_SIZE)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body

    def on_death(self) -> None:
        print("explode or something yea this isn't done TODO this")  # TODO: this
