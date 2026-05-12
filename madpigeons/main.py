import pygame
import pymunk
from typing import Callable
from pygame import draw

from game import PhysGame
from ui import UIElement, Image, UIDim2, Vec2
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


IS_DEBUG = False

HOTBAR: list[InventoryItem] = [
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
HOTBAR_SLOT_SIZE = 70
HOTBAR_SLOT_PADDING = 4


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

        screen_container = UIElement(size=UIDim2(self.window_width, self.window_height))

        self.test_image = Image(
            screen_container, size=UIDim2(64, 32), image=assets.RED_BIRD
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

    def on_mouse_move(self):
        self.test_image.size = UIDim2(*pygame.mouse.get_pos())
        self.test_image.render()

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)

        for entity in self.scope.entities:
            entity.draw(out)
            if IS_DEBUG:
                entity.debug_draw(out)

    def on_draw_interface(self, out: pygame.Surface):
        total_width = len(HOTBAR) * (HOTBAR_SLOT_SIZE + HOTBAR_SLOT_PADDING)

        self.test_image.draw(out)
        self.test_image.debug_draw(out)

        for index, item in enumerate(HOTBAR):
            scaled_image = pygame.transform.scale_by(
                item.image, HOTBAR_SLOT_SIZE / max(*item.image.size)
            )

            x = (
                self.window_width / 2
                + (index * (HOTBAR_SLOT_SIZE + HOTBAR_SLOT_PADDING))
                - (total_width / 2)
            ) + HOTBAR_SLOT_PADDING / 2
            y = (
                self.window_height
                - HOTBAR_SLOT_SIZE
                - 10
                + (HOTBAR_SLOT_SIZE / 2 - scaled_image.height / 2)
            )

            out.blit(
                scaled_image,
                (x, y),
            )
            if IS_DEBUG:
                draw.rect(
                    out,
                    "pink",
                    pygame.Rect(x, y, *scaled_image.size),
                    width=1,
                )


game = TheGame()
game.start()
