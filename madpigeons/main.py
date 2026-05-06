import pygame
import pymunk
from game import PhysGame
from objects import Entity, Box, RedBird


class TheGame(PhysGame):
    window_width = 1000
    window_height = 282 * 2
    gravity = 500
    title = "Mad Pigeons™️ (not angry birds)"
    icon = RedBird.IMAGE

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(
            pygame.image.load("./assets/background.jpg"),
            (self.window_width, self.window_height),
        )

        entity_scope: list[Entity] = []

        red = RedBird(entity_scope, self.space)
        red.body.position = (500, 300)

        Box(entity_scope, self.space, 250, 250).body.position = (510, -400)

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (-1e4, self.window_height * 0.82),
            (1e4, self.window_height * 0.82),
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
