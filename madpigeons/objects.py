import pygame
import pymunk

from math import degrees
from pymunk import Vec2d

from pygame import draw, transform

import assets


class EntityScope:
    def __init__(self, space: pymunk.Space):
        self.entities: set[RigidEntity] = set()
        self.space = space

        self._body_to_entity: dict[pymunk.Body, RigidEntity] = {}

    def get_entity_from_body(self, body: pymunk.Body) -> "RigidEntity | None":
        return self._body_to_entity.get(body)

    def append(self, entity: "RigidEntity"):
        self._body_to_entity[entity.body] = entity

        self.entities.add(entity)
        self.space.add(entity.body)

    def remove(self, entity: "RigidEntity"):
        if entity in self.entities:
            return
        self.entities.remove(entity)
        self.space.remove(entity.body, *entity.body.shapes)


class RigidEntity:
    body: pymunk.Body
    image: pygame.Surface

    def __init__(self, scope: EntityScope):
        self.scope = scope
        self.body = pymunk.Body()

        scope.append(self)

    def remove(self):
        self.scope.remove(self)

    def on_collision(self, arbiter: pymunk.Arbiter): ...

    def draw(self, screen: pygame.Surface):
        rotated = transform.rotate(self.image, -degrees(self.body.angle))
        screen.blit(rotated, self.body.position - Vec2d(*rotated.size) / 2)


## Bird presets
class RedBird(RigidEntity):
    image = assets.RED_BIRD

    def __init__(self, scope: EntityScope):
        super().__init__(scope)

        shape = pymunk.Circle(self.body, 18)
        shape.density = 0.3
        shape.friction = 0.4

        scope.space.add(shape)


## Pig presets
STANDARD_PIG_RADIUS = 20


class Piggy(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        radius = scale * STANDARD_PIG_RADIUS

        self.image = transform.scale(
            assets.PIG_SMILING,
            (radius * 2, radius * 2),
        )

        self.radius = radius

        shape = pymunk.Circle(self.body, radius)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = STANDARD_STONE_DENSITY

        scope.space.add(shape)

    def on_collision(self, arbiter: pymunk.Arbiter):
        force = (arbiter.total_impulse / self.body.mass).length

        if force > 800:
            self.remove()

    def debug_draw(self, screen: pygame.Surface):
        draw.circle(screen, "blue", self.body.position, self.radius, 1)


## Standard constants
STANDARD_BOX_SIZE = 50
STANDARD_BALL_RADIUS = STANDARD_BOX_SIZE / 2

STANDARD_THIN_PLANK_LENGTH = 100
STANDARD_THICK_PLANK_LENGTH = 50

STANDARD_GLASS_ELASTICITY = 0.1


## Wood presets
STANDARD_WOOD_ELASTICITY = 0.5
STANDARD_WOOD_FRICTION = 0.8
STANDARD_WOOD_DENSITY = 0.4


class WoodBox(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        scope.space.add(shape)

        self.image = transform.scale(assets.WOOD_BOX, (size, size))


class WoodPlankThick(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        length = STANDARD_THICK_PLANK_LENGTH * scale

        shape = pymunk.Poly(
            self.body,
            (
                (-length // 2, -length // 2 // 2),
                (length // 2, -length // 2 // 2),
                (-length // 2, length // 2 // 2),
                (length // 2, length // 2 // 2),
            ),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        scope.space.add(shape)

        self.image = transform.scale(assets.WOOD_RECTANGLE, (length, length // 2))


class WoodPlankThin(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        length = STANDARD_THIN_PLANK_LENGTH * scale

        shape = pymunk.Poly(
            self.body,
            (
                (-length // 2, -length // 2 // 8),
                (length // 2, -length // 2 // 8),
                (-length // 2, length // 2 // 8),
                (length // 2, length // 2 // 8),
            ),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        scope.space.add(shape)

        self.image = transform.scale(assets.WOOD_PLANK, (length, length // 8))


class WoodWedge(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float, mirrored: bool = False):
        super().__init__(scope)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            (
                ((-1 if mirrored else 1) * -size // 2, -size // 2),
                ((-1 if mirrored else 1) * -size // 2, size // 2),
                ((-1 if mirrored else 1) * size // 2, size // 2),
            ),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        scope.space.add(shape)

        self.image = transform.flip(
            transform.scale(assets.WOOD_WEDGE, (size, size)), mirrored, False
        )


class WoodTriangle(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2)),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        scope.space.add(shape)

        self.image = transform.scale(assets.WOOD_TRIANGLE, (size, size))


class WoodBall(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        radius = STANDARD_BALL_RADIUS * scale

        shape = pymunk.Circle(self.body, radius)
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        scope.space.add(shape)

        self.image = transform.scale(assets.WOOD_BALL, (radius * 2, radius * 2))


## Stone presets
STANDARD_STONE_ELASTICITY = 0.2
STANDARD_STONE_FRICTION = 0.6
STANDARD_STONE_DENSITY = 0.8


class StoneBox(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float):
        super().__init__(scope)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        scope.space.add(shape)

        self.image = transform.scale(assets.STONE_BOX, (size, size))


class StoneWedge(RigidEntity):
    def __init__(self, scope: EntityScope, scale: float, mirrored: bool = False):
        super().__init__(scope)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            (
                ((-1 if mirrored else 1) * -size // 2, -size // 2),
                ((-1 if mirrored else 1) * -size // 2, size // 2),
                ((-1 if mirrored else 1) * size // 2, size // 2),
            ),
        )
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        scope.space.add(shape)

        self.image = transform.flip(
            transform.scale(assets.STONE_WEDGE, (size, size)), mirrored, False
        )
