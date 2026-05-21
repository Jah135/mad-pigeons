import pymunk

from .entity import FragileEntity
from .dimensions import STANDARD_BIRD_RADIUS
from .. import assets


class BirdRed(FragileEntity):
    current_display_image = assets.RED_BIRD

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()

        shape = pymunk.Circle(body, STANDARD_BIRD_RADIUS)
        shape.density = 0.3
        shape.friction = 0.4

        return body
