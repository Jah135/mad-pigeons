import pygame
import pymunk

class Floor:
    def __init__(self, space: pymunk.Space, width: float = 100, height: float = 0, thickness: float = 10) -> None:
        body = pymunk.Body(1)
        segment = pymunk.Segment(body, (0, height), (width, height), thickness)

        space.add(body, segment)

class Box:
    def __init__(self, space: pymunk.Space, width: float = 5, height: float = 5) -> None:
        body = pymunk.Body(1)
        shape = pymunk.Poly(body, ((-width, -height), (width, -height), (-width, height), (width, height)))

        space.add(body, shape)
        self.body = body
    
    