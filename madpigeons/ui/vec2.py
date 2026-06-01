from __future__ import annotations
import math

PointLike = tuple[float | int, float | int]


class Vec2:
    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Vec2):
            return False
        return self.x == value.x and self.y == value.y

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

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

    def __rmul__(self, other: Vec2 | PointLike | float) -> Vec2:
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

    # Negate
    def __neg__(self):
        return Vec2(-self.x, -self.y)

    @property
    def xy(self) -> tuple[float, float]:
        """
        Returns a x, y tuple representation of this vector.
        """
        return (self.x, self.y)
    
    @property
    def yx(self) -> tuple[float, float]:
        """
        Returns a y, x tuple representation of this vector.
        """
        return (self.y, self.x)

    @property
    def length_squared(self) -> float:
        """
        Returns the square length of this vector.
        """
        return self.x**2 + self.y**2

    @property
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.length_squared)

    @property
    def normalized(self) -> Vec2:
        """
        Returns a new vector with the same direction as this vector, but with a length of 1.0.
        """
        length = self.length

        if length == 0:
            return self
        else:
            return self / length

    @property
    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def constrain_length(self, max_length: float, min_length: float = 0) -> Vec2:
        """
        Returns a new vector with the same direction as this vector, but with it's length clamped between the set values.
        """
        length = self.length

        if length < min_length:
            return self.normalized * min_length
        elif length > max_length:
            return self.normalized * max_length
        return self

    def max(self, other: Vec2) -> Vec2:
        return Vec2(max(self.x, other.x), max(self.y, other.y))

    def min(self, other: Vec2) -> Vec2:
        return Vec2(min(self.x, other.x), min(self.y, other.y))
