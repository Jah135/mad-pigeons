from __future__ import annotations
from typing import Optional, Callable, Literal

import pygame
from pygame import draw, font


class Vec2:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vec2 | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other: Vec2 | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        return Vec2(self.x / other, self.y / other)

    @property
    def tup(self) -> tuple[float, float]:
        return (self.x, self.y)


class UIDim:
    def __init__(self, offset: int = 0, scale: float = 0) -> None:
        self.offset = offset
        self.scale = scale


class UIDim2:
    def __init__(
        self,
        x_offset: int = 0,
        y_offset: int = 0,
        x_scale: float = 0,
        y_scale: float = 0,
    ) -> None:
        self.x = UIDim(x_offset, x_scale)
        self.y = UIDim(y_offset, y_scale)

    @property
    def offsets(self) -> Vec2:
        return Vec2(self.x.offset, self.y.offset)

    @property
    def scales(self) -> Vec2:
        return Vec2(self.x.scale, self.y.scale)


class Signal:
    def __init__(self) -> None:
        self.callbacks = []

    def connect(self, callback: Callable):
        self.callbacks.append(callback)

    def fire(self, *args):
        for callback in self.callbacks:
            callback(*args)


XAlignment = Literal["left"] | Literal["center"] | Literal["right"]
YAlignment = Literal["top"] | Literal["center"] | Literal["bottom"]


class UIElement:
    parent: Optional[UIElement]

    anchor_point: Vec2
    position: UIDim2
    size: UIDim2
    visible: bool

    def __init__(
        self,
        parent: Optional[UIElement] = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
    ) -> None:
        self.parent: Optional[UIElement] = None
        self.children: set[UIElement] = set()

        self.anchor_point = anchor_point
        self.position = position
        self.size = size
        self.visible = True

        self.mouse_down = Signal()
        self.mouse_up = Signal()

        self.set_parent(parent)

    @property
    def absolute_size(self) -> Vec2:
        if self.parent == None:
            return self.size.offsets

        return self.size.offsets + self.size.scales * self.parent.absolute_size

    @property
    def absolute_position(self) -> Vec2:
        if self.parent == None:
            return self.position.offsets

        return (
            self.parent.absolute_position
            + self.position.offsets
            + self.parent.absolute_size * self.position.scales
        ) - (self.absolute_size * self.anchor_point)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.absolute_position.tup, self.absolute_size.tup)

    def set_parent(self, new_parent: Optional[UIElement]):
        cur_parent = self.parent

        if cur_parent != None:
            cur_parent.children.remove(self)

        self.parent = new_parent

        if new_parent != None:
            new_parent.children.add(self)

    def is_in_bounds(self, x: int, y: int):
        abs_size = self.absolute_size
        abs_pos = self.absolute_position

        return (
            x > abs_pos.x
            and x < abs_pos.x + abs_size.x
            and y > abs_pos.y
            and y < abs_pos.y + abs_size.y
        )

    def _on_mouse_down(self, x: int, y: int):
        if self.is_in_bounds(x, y):
            self.mouse_down.fire(x, y)

        for child in self.children:
            child._on_mouse_down(x, y)

    def _on_mouse_up(self, x: int, y: int):
        if self.is_in_bounds(x, y):
            self.mouse_up.fire(x, y)

        for child in self.children:
            child._on_mouse_up(x, y)

    def _draw(self, out: pygame.Surface): ...
    def draw_all_children(self, out: pygame.Surface):
        if not self.visible:
            return

        self._draw(out)

        for child in self.children:
            child.draw_all_children(out)


class Label(UIElement):
    def __init__(
        self,
        parent: UIElement | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
        text: str = "Label",
        text_size: int = 16,
        text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        text_font: str | None = None,
        text_x_alignment: XAlignment = "center",
        text_y_alignment: YAlignment = "center",
    ) -> None:
        super().__init__(parent, anchor_point, position, size)

        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_x_alignment = text_x_alignment
        self.text_y_alignment = text_y_alignment

        self._font = font.Font(text_font, self.text_size)

        self._rerender()

    def _rerender(self):
        total_width, total_height = self.absolute_size.tup

        surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)

        txt_surface = self._font.render(self.text, True, self.text_color)

        rel_x_pos = 0
        rel_y_pos = 0

        if self.text_x_alignment == "center":
            rel_x_pos = total_width / 2 - txt_surface.width / 2
        elif self.text_x_alignment == "right":
            rel_x_pos = total_width - txt_surface.width

        if self.text_y_alignment == "center":
            rel_y_pos = total_height / 2 - txt_surface.height / 2
        elif self.text_y_alignment == "bottom":
            rel_y_pos = total_height - txt_surface.height

        surface.blit(txt_surface, (rel_x_pos, rel_y_pos))

        self._surface = surface

    def _draw(self, out: pygame.Surface):
        out.blit(self._surface, self.absolute_position.tup)


class Frame(UIElement):
    def __init__(
        self,
        parent: UIElement | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
    ) -> None:
        super().__init__(parent, anchor_point, position, size)

        self.background_color: tuple[int, int, int, int] = (255, 255, 255, 255)

        self._rerender()

    def _rerender(self):
        surface = pygame.Surface(self.absolute_size.tup, pygame.SRCALPHA)
        surface.fill(self.background_color)

        self._surface = surface

    def _draw(self, out: pygame.Surface):
        out.blit(self._surface, self.absolute_position.tup)

    def set_background_color(self, new_background_color: tuple[int, int, int, int]):
        self.background_color = new_background_color
        self._rerender()


class Image(UIElement):
    def __init__(
        self,
        parent: UIElement | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
        image: pygame.Surface = pygame.Surface((1, 1)),
    ) -> None:
        super().__init__(parent, anchor_point, position, size)

        self.set_image(image)

    def _rerender(self):
        rendered = pygame.Surface(self.absolute_size.tup, pygame.SRCALPHA)
        scaled_image = pygame.transform.scale_by(
            self.image, min(self.absolute_size.tup) / max(self.image.size)
        )
        rendered.blit(
            scaled_image, ((self.absolute_size / 2) - Vec2(*scaled_image.size) / 2).tup
        )

        self._surface = rendered

    def _draw(self, out: pygame.Surface):
        out.blit(self._surface, self.absolute_position.tup)

    def set_image(self, new_image: pygame.Surface):
        self.image = new_image
        self._rerender()
