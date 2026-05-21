import pymunk
from pygame import transform

from .entity import FragileEntity
from .dimensions import STANDARD_BOX_SIZE, STANDARD_BALL_RADIUS, STANDARD_THICK_PLANK_LENGTH, STANDARD_THIN_PLANK_LENGTH, generate_rectangle_polygon_points, generate_triangle_polygon_points, generate_wedge_polygon_points
from .. import assets


# wood properties
STANDARD_WOOD_ELASTICITY = 0.5
STANDARD_WOOD_FRICTION = 0.8
STANDARD_WOOD_DENSITY = 0.4


class Box(FragileEntity):
    current_display_image = transform.scale(
        assets.WOOD_BOX, (STANDARD_BOX_SIZE, STANDARD_BOX_SIZE))

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body, generate_rectangle_polygon_points(STANDARD_BOX_SIZE))
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body


class PlankThick(FragileEntity):
    current_display_image = transform.scale(
        assets.WOOD_PLANK_THICK, (STANDARD_THICK_PLANK_LENGTH,
                                  STANDARD_THICK_PLANK_LENGTH // 2)
    )

    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(
            STANDARD_THICK_PLANK_LENGTH, 2))
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body


class PlankThin(FragileEntity):
    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(body, generate_rectangle_polygon_points(
            STANDARD_THIN_PLANK_LENGTH, 8))
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body


class Wedge(FragileEntity):
    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            self.body,
            generate_wedge_polygon_points(STANDARD_BOX_SIZE)
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body


class Triangle(FragileEntity):
    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Poly(
            body,
            generate_triangle_polygon_points(STANDARD_BOX_SIZE)
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body


class Ball(FragileEntity):
    def create_body(self) -> pymunk.Body:
        body = pymunk.Body()
        shape = pymunk.Circle(body, STANDARD_BALL_RADIUS)
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        return body
