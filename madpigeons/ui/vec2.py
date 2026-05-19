class Vec2:
    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    # Addition
    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    # Subtraction
    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    # Multiplication
    def __mul__(self, other: "Vec2 | float") -> "Vec2":
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)

    # Division
    def __truediv__(self, other: "Vec2 | float") -> "Vec2":
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        return Vec2(self.x / other, self.y / other)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    @property
    def tup(self) -> tuple[float, float]:
        return (self.x, self.y)

    def max(self, other: "Vec2") -> "Vec2":
        return Vec2(max(self.x, other.x), max(self.y, other.y))

    def min(self, other: "Vec2") -> "Vec2":
        return Vec2(min(self.x, other.x), min(self.y, other.y))
