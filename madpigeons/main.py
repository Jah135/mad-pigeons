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

        scope = objects.EntityScope(self.space)

        red = objects.RedBird(scope)
        red.body.position = (500, 300)

        for i in range(20):
            objects.WoodBall(scope, 30 + i * 8).body.position = (500, 300 - 30 * i)

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (-1e4, self.window_height * 0.82),
            (1e4, self.window_height * 0.82),
            20,
        )
        floor_segment.density = 1000
        floor_segment.friction = 0.6

        self.space.add(floor_segment)
        self.scope = scope

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)

        for entity in self.scope.entities:
            entity.draw(out)


game = TheGame()
game.start()
