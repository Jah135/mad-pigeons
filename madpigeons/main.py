import pygame
import pymunk

from game import PhysGame
import objects
import assets


class TheGame(PhysGame):
    window_width = 1000
    window_height = 282 * 2
    gravity = 500
    title = "Mad Pigeons™ (not angry birds)"
    icon = assets.RED_BIRD

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(
            assets.BACKGROUND_1,
            (self.window_width, self.window_height),
        )

        entity_scope: list[objects.Entity] = []

        objects.RedBird(entity_scope, self.space).body.position = (500, 300)

        for i in range(10):
            objects.WoodBox(entity_scope, self.space, 40).body.position = (
                550,
                350 - i * 20,
            )

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (-1e4, self.window_height * 0.82),
            (1e4, self.window_height * 0.82),
            20,
        )
        floor_segment.density = 1000
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
