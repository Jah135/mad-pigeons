from __future__ import annotations

import pygame
import pymunk

from math import degrees
from pymunk import Vec2d
from pygame import draw, transform

import assets


class World:
    all_entities: set[Entity]
    physical_entities: set[PhysicsEntity]
    space: pymunk.Space

    _body_to_entity: dict[pymunk.Body, PhysicsEntity]

    def __init__(self, space: pymunk.Space):
        self.space = space
        self.all_entities = set()
        self.physical_entities = set()
        self._body_to_entity = dict()

    def get_physics_entity_from_body(self, body: pymunk.Body) -> None | PhysicsEntity:
        return self._body_to_entity.get(body)


class Entity:
    world: World

    def __init__(self, world: World) -> None:
        self.world = world
        world.all_entities.add(self)

    def remove(self):
        if self in self.world.all_entities:
            self.world.all_entities.remove(self)

    def update(self, dt: float): ...

    def draw(self, screen: pygame.Surface): ...


class PhysicsEntity(Entity):
    body: pymunk.Body
    image: pygame.Surface

    def __init__(self, world: World):
        super().__init__(world)

        self.body = pymunk.Body()

        world.physical_entities.add(self)
        world.space.add(self.body)
        world._body_to_entity[self.body] = self

    def remove(self):
        super().remove()

        if self in self.world.physical_entities:
            self.world.physical_entities.remove(self)
            self.world.space.remove(self.body, *self.body.shapes)
            del self.world._body_to_entity[self.body]

    def draw(self, screen: pygame.Surface):
        rotated = transform.rotate(self.image, -degrees(self.body.angle))
        screen.blit(rotated, self.body.position - Vec2d(*rotated.size) / 2)

    def on_collision(self, arbiter: pymunk.Arbiter): ...


class HealthyEntity(PhysicsEntity):
    resistance: float
    health: float
    max_health: float
    health_image_stages: list[pygame.Surface]

    def update_image(self):
        alpha = self.health / self.max_health
        index = int((len(self.health_image_stages) - 1) * alpha)

        self.image = self.health_image_stages[index]

    def inflict_damage(self, raw_damage: float):
        self.health -= raw_damage * (1.1**self.resistance)

        if self.health <= 0:
            self.remove()
        else:
            self.update_image()

    def on_collision(self, arbiter: pymunk.Arbiter):
        arbiter.total_impulse


## Bird presets
class RedBird(PhysicsEntity):
    image = assets.RED_BIRD

    def __init__(self, world: World):
        super().__init__(world)

        shape = pymunk.Circle(self.body, 18)
        shape.density = 0.3
        shape.friction = 0.4

        world.space.add(shape)


## Pig presets
STANDARD_PIG_RADIUS = 20


class Piggy(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

        radius = scale * STANDARD_PIG_RADIUS

        self.image = transform.scale(
            assets.BIG_PIG_HURT_1,
            (radius * 2, radius * 2),
        )

        self.radius = radius

        shape = pymunk.Circle(self.body, radius)
        shape.density = 0.3
        shape.friction = 0.4
        shape.elasticity = STANDARD_STONE_DENSITY

        world.space.add(shape)

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


class WoodBox(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

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

        world.space.add(shape)

        self.image = transform.scale(assets.WOOD_BOX, (size, size))


class WoodPlankThick(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

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

        world.space.add(shape)

        self.image = transform.scale(assets.WOOD_RECTANGLE, (length, length // 2))


class WoodPlankThin(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

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

        world.space.add(shape)

        self.image = transform.scale(assets.WOOD_PLANK, (length, length // 8))


class WoodWedge(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        world.space.add(shape)

        self.image = transform.scale(assets.WOOD_WEDGE, (size, size))


class WoodTriangle(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2)),
        )
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        world.space.add(shape)

        self.image = transform.scale(assets.WOOD_TRIANGLE, (size, size))


class WoodBall(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

        radius = STANDARD_BALL_RADIUS * scale

        shape = pymunk.Circle(self.body, radius)
        shape.density = STANDARD_WOOD_DENSITY
        shape.friction = STANDARD_WOOD_FRICTION
        shape.elasticity = STANDARD_WOOD_ELASTICITY

        world.space.add(shape)

        self.image = transform.scale(assets.WOOD_BALL, (radius * 2, radius * 2))


## Stone presets
STANDARD_STONE_ELASTICITY = 0.2
STANDARD_STONE_FRICTION = 0.6
STANDARD_STONE_DENSITY = 0.8


class StoneBox(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

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

        world.space.add(shape)

        self.image = transform.scale(assets.STONE_BOX, (size, size))


class StoneWedge(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            (
                (-size // 2, -size // 2),
                (-size // 2, size // 2),
                (size // 2, size // 2),
            ),
        )
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        world.space.add(shape)

        self.image = transform.scale(assets.STONE_WEDGE, (size, size))


class StoneTriangle(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

        size = STANDARD_BOX_SIZE * scale

        shape = pymunk.Poly(
            self.body,
            ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2)),
        )
        shape.density = STANDARD_STONE_DENSITY
        shape.friction = STANDARD_STONE_FRICTION
        shape.elasticity = STANDARD_STONE_ELASTICITY

        world.space.add(shape)

        self.image = transform.scale(assets.STONE_TRIANGLE, (size, size))


# this should be done a different way this kinda sucks
class Explosion(Entity):
    position: Vec2d
    blast_radius: int
    blast_force: int

    def __init__(
        self, world: World, position: Vec2d, blast_radius: int, blast_force: int
    ) -> None:
        super().__init__(world)

        self.position = position
        self.blast_radius = blast_radius
        self.blast_force = blast_force

    def update(self, dt: float):
        space = self.world.space

        for info in space.point_query(
            self.position.int_tuple, self.blast_radius, pymunk.ShapeFilter()
        ):
            closest_shape = info.shape
            body = closest_shape.body

            if body == None:
                continue

            body.apply_force_at_world_point(
                -info.gradient * self.blast_force,
                info.point,
            )
        self.remove()


class TNT(PhysicsEntity):
    def __init__(self, world: World, scale: float):
        super().__init__(world)

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

        world.space.add(shape)

        self.image = transform.scale(assets.TNT, (size, size))

    def on_collision(self, arbiter: pymunk.Arbiter):
        force = arbiter.total_impulse.length / self.body.mass

        if force > 600:
            Explosion(self.world, self.body.position, 150, 20000000)
            self.remove()
