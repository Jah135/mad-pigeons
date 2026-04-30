import pygame
import pymunk

class Game:
    window_width: int = 100
    window_height: int = 100
    target_framerate: int = 60

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.last_dt = 0
        self.running = False

    # mouse events
    def on_mouse_down(self, left: bool, middle: bool, right: bool): ...
    def on_mouse_up(self, left: bool, middle: bool, right: bool): ...

    def on_event(self, event: pygame.event.Event): ...
    def on_draw(self, out: pygame.Surface): ...
    def on_update(self, dt: float): ...

    def quit(self):
        self.running = False

    def start(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_down(*pygame.mouse.get_pressed())
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_up(*pygame.mouse.get_pressed())

                self.on_event(event=event)

            dt = clock.tick(self.target_framerate) / 1000

            self.on_update(dt=dt)
            self.on_draw(out=self.screen)
            pygame.display.flip()

            self.last_dt = dt

class PhysGame(Game):
    gravity = 100

    def __init__(self) -> None:
        super().__init__()

        self.space = pymunk.Space()
        self.space.gravity = (0, self.gravity)
    
    def on_update(self, dt: float):
        self.space.step(dt)
