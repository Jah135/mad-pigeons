import pymunk
from pygame import transform

from .entity import FragileEntity
from .dimensions import *
from .. import assets


class TNT(FragileEntity):
    max_health = 50
    damage_resistance = 1.3
    damage_frames = (assets.TNT,)

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body

    def on_break(self) -> None:
        print("explode or something yea this isn't done TODO this")  # TODO: this
