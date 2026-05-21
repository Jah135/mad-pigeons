import pymunk

from .entity import FragileEntity
from .dimensions import STANDARD_PIG_RADIUS
from .. import assets


class Pig(FragileEntity):
    current_display_image = assets.SMALL_PIG

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()

        shape = pymunk.Circle(body, STANDARD_PIG_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = 0.5

        return body
