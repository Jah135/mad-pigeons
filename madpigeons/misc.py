import pymunk

from ui import Vec2


def point_in_body(point: tuple[float, float], body: pymunk.Body) -> bool:
    for shape in body.shapes:
        if shape.point_query(point).distance <= 0:
            return True
    return False


def float_range(start: float = 0, end: float = 1, delta: float = 1):
    cur = start
    yield start
    while cur < end:
        cur += delta
        yield cur


def calculate_kinematic_position(
    initial_position: Vec2, initial_velocity: Vec2, acceleration: Vec2, t: float
) -> Vec2:
    return initial_position + (initial_velocity * t) + (acceleration * t**2) / 2


def calculate_kinematic_path(
    initial_position: Vec2,
    initial_velocity: Vec2,
    acceleration: Vec2,
    total_time: float = 5,
    time_resolution: float = 0.05,
) -> list[Vec2]:
    return [
        calculate_kinematic_position(
            initial_position, initial_velocity, acceleration, t
        )
        for t in float_range(0, total_time, time_resolution)
    ]
