from __future__ import annotations
from typing import Optional, Callable
from enum import Enum

import pygame
from pygame import draw, font


class HorizontalAlignment(Enum):
    Left = "left"
    Center = "center"
    Right = "right"


class VerticalAlignment(Enum):
    Top = "top"
    Center = "center"
    Bottom = "bottom"


class UIState(Enum):
    Idle = "idle"
    Hover = "hover"
    Press = "press"


class Vec2:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vec2 | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __truediv__(self, other: Vec2 | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        return Vec2(self.x / other, self.y / other)

    @property
    def tup(self) -> tuple[float, float]:
        return (self.x, self.y)

    def max(self, other: Vec2) -> Vec2:
        return Vec2(max(self.x, other.x), max(self.y, other.y))

    def min(self, other: Vec2) -> Vec2:
        return Vec2(min(self.x, other.x), min(self.y, other.y))


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


class EventSignal:
    def __init__(self) -> None:
        self.callbacks = []

    def connect(self, callback: Callable):
        self.callbacks.append(callback)

    def fire(self, *args):
        for callback in self.callbacks:
            callback(*args)


class UIElement:
    parent: Optional[UIElement]

    anchor_point: Vec2
    position: UIDim2
    size: UIDim2
    visible: bool

    buffer_texture: pygame.Surface

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

        self.state = UIState.Idle

        # signals
        self.mouse_down = EventSignal()
        self.mouse_up = EventSignal()
        self.mouse_enter = EventSignal()
        self.mouse_leave = EventSignal()

        self.set_parent(parent)
        self.rerender_self()

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
    def absolute_bounds(self) -> pygame.Rect:
        top_left = self.absolute_position
        size = self.absolute_size

        for child in self.children:
            child_bounds = child.absolute_bounds
            child_topleft = Vec2(*child_bounds.topleft)
            child_dimensions = Vec2(*child_bounds.size)

            top_left = top_left.min(child_topleft)
            size = size.max((child_topleft - self.absolute_position) + child_dimensions)

        return pygame.Rect(
            top_left.tup, (size + (self.absolute_position - top_left)).tup
        )

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

    def check_in_bounds(self, x: int, y: int):
        abs_size = self.absolute_size
        abs_pos = self.absolute_position

        return (
            x > abs_pos.x
            and x < abs_pos.x + abs_size.x
            and y > abs_pos.y
            and y < abs_pos.y + abs_size.y
        )

    def _on_mouse_down(self, x: int, y: int):
        if self.state == UIState.Hover:
            self.state = UIState.Press
            self.mouse_down.fire(x, y)

        # propogate to children
        for child in self.children:
            child._on_mouse_down(x, y)

    def _on_mouse_up(self, x: int, y: int):
        if self.state == UIState.Press:
            self.state = UIState.Hover
            self.mouse_up.fire(x, y)

        # propogate to children
        for child in self.children:
            child._on_mouse_up(x, y)

    def _on_mouse_move(self, x: int, y: int):
        if self.check_in_bounds(x, y):
            if self.state == UIState.Idle:
                self.state = UIState.Hover
                self.mouse_enter.fire(x, y)
        else:
            if self.state != UIState.Idle:
                self.state = UIState.Idle
                self.mouse_leave.fire(x, y)

        # propogate to children
        for child in self.children:
            child._on_mouse_move(x, y)

    def rerender_self(self):
        texture = pygame.Surface(self.absolute_bounds.size, pygame.SRCALPHA)

        self.buffer_texture = texture

    def rerender_ancestors(self):
        self.rerender_self()

        # draw.rect(
        #     self.buffer_texture,
        #     "purple",
        #     self.absolute_bounds.move((-self.absolute_position).tup),
        #     4,
        # )

        for child in self.children:
            # draw.rect(self.buffer_texture, "green", child.absolute_bounds.move((-)), 2)
            self.buffer_texture.blit(
                child.buffer_texture,
                (child.absolute_position - self.absolute_position).tup,
            )

        if self.parent != None:
            self.parent.rerender_ancestors()

    def draw_to_surface(self, out: pygame.Surface):
        out.blit(self.buffer_texture)
        # draw_next: list[UIElement] = []
        # draw_queue: list[UIElement] = [self]

        # while len(draw_queue) > 0:
        #     for element in draw_queue:
        #         if not element.visible:
        #             continue
        #         element.draw_to_surface(out)
        #         draw_next.extend(element.children)

        #     draw_queue.clear()
        #     draw_next, draw_queue = draw_queue, draw_next


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
        text_x_alignment: HorizontalAlignment = HorizontalAlignment.Center,
        text_y_alignment: VerticalAlignment = VerticalAlignment.Center,
    ) -> None:
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_x_alignment = text_x_alignment
        self.text_y_alignment = text_y_alignment

        self._font = font.Font(text_font, self.text_size)

        super().__init__(parent, anchor_point, position, size)

    def rerender_self(self):
        total_width, total_height = self.absolute_size.tup

        texture = pygame.Surface((total_width, total_height), pygame.SRCALPHA)

        txt_surface = self._font.render(self.text, True, self.text_color)

        rel_x_pos = 0
        rel_y_pos = 0

        if self.text_x_alignment == HorizontalAlignment.Center:
            rel_x_pos = total_width / 2 - txt_surface.width / 2
        elif self.text_x_alignment == HorizontalAlignment.Right:
            rel_x_pos = total_width - txt_surface.width

        if self.text_y_alignment == VerticalAlignment.Center:
            rel_y_pos = total_height / 2 - txt_surface.height / 2
        elif self.text_y_alignment == VerticalAlignment.Bottom:
            rel_y_pos = total_height - txt_surface.height

        texture.blit(txt_surface, (rel_x_pos, rel_y_pos))

        self.buffer_texture = texture


class Frame(UIElement):
    def __init__(
        self,
        parent: UIElement | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
    ) -> None:
        self.background_color: tuple[int, int, int, int] = (255, 255, 255, 255)

        super().__init__(parent, anchor_point, position, size)

    def rerender_self(self):
        texture = pygame.Surface(self.absolute_size.tup, pygame.SRCALPHA)
        texture.fill(self.background_color)

        self.buffer_texture = texture

    def set_background_color(self, new_background_color: tuple[int, int, int, int]):
        self.background_color = new_background_color
        self.rerender_ancestors()


class Image(UIElement):
    def __init__(
        self,
        parent: UIElement | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
        image: pygame.Surface = pygame.Surface((1, 1)),
    ) -> None:
        self.image = image

        super().__init__(parent, anchor_point, position, size)

    def rerender_self(self):
        texture = pygame.Surface(self.absolute_size.tup, pygame.SRCALPHA)
        scaled_image = pygame.transform.scale_by(
            self.image, min(self.absolute_size.tup) / max(self.image.size)
        )
        texture.blit(
            scaled_image, ((self.absolute_size / 2) - Vec2(*scaled_image.size) / 2).tup
        )

        self.buffer_texture = texture

    def set_image(self, new_image: pygame.Surface):
        self.image = new_image
        self.rerender_ancestors()
