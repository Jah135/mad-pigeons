import pygame
import pygame.draw as d
import pymunk
import pymunk.constraints as joints

from math import degrees
from pymunk import Vec2d

import assets


class EntityScope:
    def __init__(self, space: pymunk.Space):
        self.entities: list[Entity] = []
        self.space = space

    def add(self, entity: "Entity"):
        self.entities.append(entity)

    def remove(self, entity: "Entity"):
        self.entities.remove(entity)


class Entity:
    def __init__(self, scope: EntityScope):
        scope.add(self)

    def draw(self, screen: pygame.Surface): ...


class RigidEntity(Entity):
    body: pymunk.Body
    image: pygame.Surface

    def __init__(self, scope: EntityScope):
        self.body = pymunk.Body()

        scope.add(self)
        scope.space.add(self.body)

    def draw(self, screen: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, -degrees(self.body.angle))
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


## Wood presets
class WoodBox(RigidEntity):
    def __init__(self, scope: EntityScope, size: int):
        super().__init__(scope)

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = 0.6
        shape.friction = 0.8

        scope.space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_BOX, (size, size))


class WoodRectangle(RigidEntity):
    def __init__(self, scope: EntityScope, length: int):
        super().__init__(scope)

        shape = pymunk.Poly(
            self.body,
            (
                (-length // 2, -length // 2 // 2),
                (length // 2, -length // 2 // 2),
                (-length // 2, length // 2 // 2),
                (length // 2, length // 2 // 2),
            ),
        )
        shape.density = 0.6
        shape.friction = 0.8

        scope.space.add(shape)

        self.image = pygame.transform.scale(
            assets.WOOD_RECTANGLE, (length, length // 2)
        )


class WoodPlank(RigidEntity):
    def __init__(self, scope: EntityScope, length: int):
        super().__init__(scope)

        shape = pymunk.Poly(
            self.body,
            (
                (-length // 2, -length // 2 // 8),
                (length // 2, -length // 2 // 8),
                (-length // 2, length // 2 // 8),
                (length // 2, length // 2 // 8),
            ),
        )
        shape.density = 0.6
        shape.friction = 0.8

        scope.space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_PLANK, (length, length // 8))


class WoodWedge(RigidEntity):
    def __init__(self, scope: EntityScope, size: int):
        super().__init__(scope)

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = 0.6
        shape.friction = 0.8

        scope.space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_WEDGE, (size, size))


class WoodTriangle(RigidEntity):
    def __init__(self, scope: EntityScope, size: int):
        super().__init__(scope)

        shape = pymunk.Poly(
            self.body,
            ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2)),
        )
        shape.density = 0.6
        shape.friction = 0.8

        scope.space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_TRIANGLE, (size, size))


class WoodBall(RigidEntity):
    def __init__(self, scope: EntityScope, radius: int):
        super().__init__(scope)

        shape = pymunk.Circle(self.body, radius / 2)
        shape.density = 0.6
        shape.friction = 0.8

        scope.space.add(shape)

        self.image = pygame.transform.scale(assets.WOOD_BALL, (radius, radius))
