from typing import Sequence


def generate_rectangle(
    width: float, xy_ratio: float = 1
) -> Sequence[tuple[float, float]]:
    """
    Generates a sequence of tuple points in the shape of a
    rectangle with the specified width ratio.
    """
    return (
        (-width // 2, -width // 2 // xy_ratio),
        (width // 2, -width // 2 // xy_ratio),
        (-width // 2, width // 2 // xy_ratio),
        (width // 2, width // 2 // xy_ratio),
    )


def generate_wedge(size: float) -> Sequence[tuple[float, float]]:
    """
    Generates a sequence of tuple points in the shape of a
    right-facing, isoceles right triangle.
    """
    return (
        (-size // 2, -size // 2),
        (-size // 2, size // 2),
        (size // 2, size // 2),
    )


def generate_triangle(size: float) -> Sequence[tuple[float, float]]:
    """
    Generates a sequence of tuple points in the shape of an
    upright, (probably) equilateral triangle.
    """
    return ((-size // 2, size // 2), (size // 2, size // 2), (0, -size // 2))
