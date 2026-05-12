from __future__ import annotations
from typing import Optional

import pygame
from pygame import draw


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


class UIElement:
    parent: Optional[UIElement]

    anchor_point: Vec2
    position: UIDim2
    size: UIDim2

    def __init__(
        self,
        parent: Optional[UIElement] = None,
        anchor_point: Vec2 = Vec2(),
        position: UIDim2 = UIDim2(),
        size: UIDim2 = UIDim2(),
    ) -> None:
        self.parent = parent

        self.anchor_point = anchor_point
        self.position = position
        self.size = size

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

    def debug_draw(self, out: pygame.Surface):
        draw.rect(out, "red", self.rect, 1)


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

        self.image = image
        self.render()

    def render(self):
        rendered = pygame.Surface(self.absolute_size.tup, pygame.SRCALPHA)
        scaled_image = pygame.transform.scale_by(
            self.image, min(self.absolute_size.tup) / max(self.image.size)
        )
        rendered.blit(
            scaled_image, ((self.absolute_size / 2) - Vec2(*scaled_image.size) / 2).tup
        )

        self.rendered = rendered

    def draw(self, out: pygame.Surface):
        out.blit(self.rendered, self.absolute_position.tup)
