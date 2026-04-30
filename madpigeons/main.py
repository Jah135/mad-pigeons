import pygame
import pymunk
from game import PhysGame
from birds import RedBird

class TheGame(PhysGame):
    window_width = 1000
    window_height = 282 * 2

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(pygame.image.load("./assets/background.jpg"), (self.window_width, self.window_height))

        red = RedBird(self.space)
        red.body.apply_force_at_local_point((2000, 0), (10, 0))

        self.bird = red

        segment = pymunk.Segment(self.space.static_body, (0, self.window_height * 0.8), (self.window_width, self.window_height * 0.8), 20)
        segment.density = 1
        segment.friction = 10

        self.space.add(segment)

    def on_mouse_down(self, left: bool, middle: bool, right: bool):
        pass

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)
        self.bird.draw(out)
    


game = TheGame()
game.start()