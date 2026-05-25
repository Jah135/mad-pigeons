class Color:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 0) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b
        yield self.a

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)
