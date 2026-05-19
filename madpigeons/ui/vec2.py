from __future__ import annotations

PointLike = tuple[float | int, float | int]


class Vec2:
    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    # Addition
    def __add__(self, other: Vec2 | PointLike) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        return Vec2(self.x + other[0], self.y + other[1])

    def __radd__(self, other: Vec2 | PointLike) -> Vec2:
        return self.__add__(other)

    # Subtraction
    def __sub__(self, other: Vec2 | PointLike) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return Vec2(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: Vec2 | PointLike) -> Vec2:
        return self.__sub__(other)

    # Multiplication
    def __mul__(self, other: Vec2 | PointLike | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        elif isinstance(other, tuple):
            return Vec2(self.x * other[0], self.y * other[1])
        return Vec2(self.x * other, self.y * other)

    # Division
    def __truediv__(self, other: Vec2 | PointLike | float) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        elif isinstance(other, tuple):
            return Vec2(self.x / other[0], self.y / other[1])
        return Vec2(self.x / other, self.y / other)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    @property
    def tup(self) -> tuple[float, float]:
        return (self.x, self.y)

    def max(self, other: Vec2) -> Vec2:
        return Vec2(max(self.x, other.x), max(self.y, other.y))

    def min(self, other: Vec2) -> Vec2:
        return Vec2(min(self.x, other.x), min(self.y, other.y))
