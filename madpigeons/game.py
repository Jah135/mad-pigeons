import pygame
import pymunk


class Game:
    window_width: int = 100
    window_height: int = 100
    target_framerate: int = 60
    title: str = "Game"
    icon: pygame.Surface | None = None

    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption(self.title)

        if self.icon:
            pygame.display.set_icon(self.icon)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.last_dt = 0
        self.running = False

    # mouse events
    def on_mouse_left_down(self): ...
    def on_mouse_left_up(self): ...
    def on_mouse_move(self): ...

    def on_event(self, event: pygame.event.Event): ...
    def on_draw(self, out: pygame.Surface): ...
    def on_draw_interface(self, out: pygame.Surface): ...
    def on_update(self, dt: float): ...

    def quit(self):
        self.running = False

    def start(self):
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.on_event(event=event)

                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.on_mouse_left_down()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.on_mouse_left_up()
                elif event.type == pygame.MOUSEMOTION:
                    self.on_mouse_move()

            dt = clock.tick(self.target_framerate) / 1000

            self.on_update(dt=dt)
            self.on_draw(out=self.screen)
            self.on_draw_interface(out=self.screen)
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
