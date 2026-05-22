from typing import Sequence


def generate_rectangle_polygon_points(
    size: float, xy_ratio: float = 1
) -> Sequence[tuple[float, float]]:
    return (
        (-size // 2, -size // 2 // xy_ratio),
        (size // 2, -size // 2 // xy_ratio),
        (-size // 2, size // 2 // xy_ratio),
        (size // 2, size // 2 // xy_ratio),
    )


def generate_wedge_polygon_points(size: float) -> Sequence[tuple[float, float]]:
    return (
        (-size // 2, -size // 2),
        (-size // 2, size // 2),
        (size // 2, size // 2),
    )


def generate_triangle_polygon_points(size: float) -> Sequence[tuple[float, float]]:
    return ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2))
