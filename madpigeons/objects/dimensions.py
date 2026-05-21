from typing import Sequence

# dimensions
STANDARD_PIG_RADIUS = 20
STANDARD_BIRD_RADIUS = 18

STANDARD_BOX_SIZE = 50
STANDARD_BALL_RADIUS = STANDARD_BOX_SIZE / 2

STANDARD_THIN_PLANK_LENGTH = 100
STANDARD_THICK_PLANK_LENGTH = 50


def generate_rectangle_polygon_points(size: float, xy_ratio: float = 1) -> Sequence[tuple[float, float]]:
    return ((-size // 2, -size // 2 // xy_ratio),
            (size // 2, -size // 2 // xy_ratio),
            (-size // 2, size // 2 // xy_ratio),
            (size // 2, size // 2 // xy_ratio))


def generate_wedge_polygon_points(size: float) -> Sequence[tuple[float, float]]:
    return (
        (-size // 2, -size // 2),
        (-size // 2, size // 2),
        (size // 2, size // 2),
    )


def generate_triangle_polygon_points(size: float) -> Sequence[tuple[float, float]]:
    return ((-size // 2, size // 2),
            (size // 2, size // 2), (0, -size // 2))
