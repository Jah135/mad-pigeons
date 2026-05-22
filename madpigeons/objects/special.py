import pymunk
from pygame import transform

from .entity import FragileEntity
from .generate import generate_rectangle_polygon_points
from .constants import BOX_WIDTH
from .wood import (
    WOOD_DENSITY,
    WOOD_ELASTICITY,
    WOOD_FRICTION,
)
import assets


class TNT(FragileEntity):
    max_health = 50
    damage_resistance = 1.3
    damage_textures = (assets.TNT,)
    texture_dimensions = (BOX_WIDTH, BOX_WIDTH)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(BOX_WIDTH))
        shape.density = WOOD_DENSITY
        shape.friction = WOOD_FRICTION
        shape.elasticity = WOOD_ELASTICITY

        return body

    def on_death(self) -> None:
        print("explode or something yea this isn't done TODO this")  # TODO: this
