import pygame

from pygame import mouse, key


class Game:
    window_width: int = 100
    window_height: int = 100
    target_framerate: int = 60
    title: str = "Game"
    icon: pygame.Surface | None = None

    running: bool = False
    screen: pygame.Surface

    _last_dt: float = 0
    _last_mouse_pos: tuple[int, int] = (0, 0)

    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption(self.title)

        if self.icon:
            pygame.display.set_icon(self.icon)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    # mouse events
    def on_mouse_left_down(self, pos: tuple[int, int]): ...
    def on_mouse_left_up(self, pos: tuple[int, int]): ...
    def on_mouse_move(self, pos: tuple[int, int]): ...

    # keyboard events
    def on_key_down(self, key: str): ...

    def on_event(self, event: pygame.event.Event): ...
    def on_draw_scene(self, out: pygame.Surface): ...
    def on_draw_interface(self, out: pygame.Surface): ...
    def on_update(self, dt: float): ...

    def setup(self): ...

    # def

    def quit(self):
        self.running = False

    def start(self):
        clock = pygame.time.Clock()
        self.running = True

        self.setup()

        while self.running:
            mouse_pos = mouse.get_pos()

            for event in pygame.event.get():

                self.on_event(event=event)

                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.on_mouse_left_down(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.on_mouse_left_up(mouse_pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.on_mouse_move(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self.on_key_down(key.name(event.key))

            dt = clock.tick(self.target_framerate) / 1000

            self.on_update(dt=dt)
            self.on_draw_scene(out=self.screen)
            self.on_draw_interface(out=self.screen)
            pygame.display.flip()

            self._last_dt = dt
            self._last_mouse_pos = mouse_pos
