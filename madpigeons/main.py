import pygame
import pymunk
from game import PhysGame
from objects import Entity, Box, RedBird


class TheGame(PhysGame):
    window_width = 1000
    window_height = 282 * 2
    gravity = 500

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(
            pygame.image.load("./assets/background.jpg"),
            (self.window_width, self.window_height),
        )

        entity_scope: list[Entity] = []

        red = RedBird(entity_scope, self.space)
        red.body.apply_force_at_local_point((5000, 0), (10, 0))

        Box(entity_scope, self.space, 50, 50).body.position = (400, 100)
        Box(entity_scope, self.space, 150, 250).body.position = (375, 0)
        Box(entity_scope, self.space, 25, 50).body.position = (300, 0)

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (0, self.window_height * 0.82),
            (self.window_width, self.window_height * 0.82),
            20,
        )
        floor_segment.density = 1
        floor_segment.friction = 0.6

        self.space.add(floor_segment)
        self.entities = entity_scope

    def on_mouse_down(self, left: bool, middle: bool, right: bool):
        pass

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)

        for entity in self.entities:
            entity.draw(out)


game = TheGame()
game.start()
