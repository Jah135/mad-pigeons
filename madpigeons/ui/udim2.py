from .vec2 import Vec2


class UDim:
    offset: int
    scale: float

    def __init__(self, offset: int = 0, scale: float = 0) -> None:
        self.offset = offset
        self.scale = scale

    def __repr__(self) -> str:
        return f"UIDim({self.offset, self.scale})"

    # Addition
    def __add__(self, other: "UDim") -> "UDim":
        return UDim(self.offset + other.offset, self.scale + other.scale)

    # Subtraction
    def __sub__(self, other: "UDim") -> "UDim":
        return UDim(self.offset - other.offset, self.scale - other.scale)


class UDim2:
    def __init__(
        self,
        x_offset: int = 0,
        x_scale: float = 0,
        y_offset: int = 0,
        y_scale: float = 0,
    ) -> None:
        self.x = UDim(x_offset, x_scale)
        self.y = UDim(y_offset, y_scale)

    def __repr__(self) -> str:
        return (
            f"UIDim2({self.x.offset}, {self.x.scale}, {self.y.offset}, {self.y.scale})"
        )

    @property
    def offsets(self) -> Vec2:
        return Vec2(self.x.offset, self.y.offset)

    @property
    def scales(self) -> Vec2:
        return Vec2(self.x.scale, self.y.scale)
