import pygame
import pymunk
from typing import Callable

from game import PhysGame
import objects
import assets


class InventoryItem:
    def __init__(
        self,
        fn: Callable[[objects.EntityScope], objects.RigidEntity],
        name: str,
        image: pygame.Surface,
    ) -> None:
        self.fn = fn
        self.name = name
        self.image = image


INVENTORY: list[InventoryItem] = [
    InventoryItem(
        lambda scope: objects.WoodBall(scope, 30), "Wood Ball", assets.WOOD_BALL
    ),
    InventoryItem(
        lambda scope: objects.WoodPlank(scope, 30), "Wood Plank", assets.WOOD_PLANK
    ),
    InventoryItem(
        lambda scope: objects.WoodTriangle(scope, 30),
        "Wood Triangle",
        assets.WOOD_TRIANGLE,
    ),
    InventoryItem(
        lambda scope: objects.WoodWedge(scope, 30),
        "Wood Wedge",
        assets.WOOD_WEDGE,
    ),
    InventoryItem(
        lambda scope: objects.Piggy(scope, 30),
        "Pig",
        assets.PIG_SMILING,
    ),
]
INVENTORY_ITEM_SIZE = 50


class TheGame(PhysGame):
    window_width = 1000
    window_height = 564
    gravity = 500
    title = "Mad Pigeons™ (not angry birds)"
    icon = assets.RED_BIRD

    def __init__(self) -> None:
        super().__init__()

        self.background_image = pygame.transform.scale(
            assets.BACKGROUND_1,
            (self.window_width, self.window_height),
        )

        scope = objects.EntityScope(self.space)

        red = objects.RedBird(scope)
        red.body.position = (500, 300)

        for i in range(100):
            objects.Piggy(scope, 10 + i // 2).body.position = (500, 300 - 30 * i)

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (-1e4, self.window_height * 0.9 + 80),
            (1e4, self.window_height * 0.9 + 80),
            90,
        )
        floor_segment.friction = 0.6

        self.space.add(floor_segment)
        self.scope = scope

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)

        for entity in self.scope.entities:
            entity.draw(out)

        total_width = len(INVENTORY * INVENTORY_ITEM_SIZE)

        pygame.draw.line(
            out,
            "blue",
            (self.window_width / 2, 0),
            (self.window_width / 2, self.window_height),
        )

        for index, item in enumerate(INVENTORY):
            scaled_image = pygame.transform.scale_by(
                item.image, INVENTORY_ITEM_SIZE / max(*item.image.size)
            )

            out.blit(
                scaled_image,
                (
                    (self.window_width / 2)
                    - total_width
                    - (index * INVENTORY_ITEM_SIZE),
                    self.window_height
                    - INVENTORY_ITEM_SIZE / 2
                    - scaled_image.height / 2,
                ),
            )
            pygame.draw.circle(
                out,
                "red",
                (
                    self.window_width / 2
                    + total_width / 2
                    - (index + 1) * INVENTORY_ITEM_SIZE,
                    20,
                ),
                4,
            )


game = TheGame()
game.start()
