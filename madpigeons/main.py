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
        self.create = fn
        self.name = name
        self.image = image


IS_DEBUG = False

HOTBAR: list[InventoryItem] = [
    InventoryItem(lambda scope: objects.WoodBox(scope, 1), "Wood Box", assets.WOOD_BOX),
    InventoryItem(
        lambda scope: objects.WoodBall(scope, 1), "Wood Ball", assets.WOOD_BALL
    ),
    InventoryItem(
        lambda scope: objects.WoodPlankThin(scope, 1), "Wood Plank", assets.WOOD_PLANK
    ),
    InventoryItem(
        lambda scope: objects.WoodPlankThick(scope, 1),
        "Wood Plank",
        assets.WOOD_RECTANGLE,
    ),
    InventoryItem(
        lambda scope: objects.WoodTriangle(scope, 1),
        "Wood Triangle",
        assets.WOOD_TRIANGLE,
    ),
    InventoryItem(
        lambda scope: objects.WoodWedge(scope, 1),
        "Wood Wedge",
        assets.WOOD_WEDGE,
    ),
    InventoryItem(
        lambda scope: objects.Piggy(scope, 1),
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
        self.screen_container = screen_container

        hotbar_container = UIElement(
            screen_container,
            size=UIDim2(0, HOTBAR_SLOT_SIZE, 0.5, 0),
            position=UIDim2(0, -5, 0.5, 1),
            anchor_point=Vec2(0.5, 1),
        )

        hotbar_count = len(HOTBAR)

        self.current_dragging_item: InventoryItem | None = None

        for index, item in enumerate(HOTBAR):
            image = Image(
                hotbar_container,
                Vec2(index / (hotbar_count - 1), 0),
                UIDim2(0, 0, index / (hotbar_count - 1), 0),
                UIDim2(HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE),
                image=item.image,
            )

            def on_mouse_down(*_, item=item):
                self.current_dragging_item = item

            image.mouse_down.connect(on_mouse_down)

        scope = objects.EntityScope(self.space)

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (-1e4, self.window_height * 0.9 + 70),
            (1e4, self.window_height * 0.9 + 70),
            90,
        )
        floor_segment.friction = 0.6

        self.space.add(floor_segment)
        self.scope = scope

    def on_mouse_left_down(self):
        self.screen_container._on_mouse_down(*pygame.mouse.get_pos())

    def on_mouse_left_up(self):
        mouse_position = pygame.mouse.get_pos()

        self.screen_container._on_mouse_up(*mouse_position)

        if self.current_dragging_item != None:
            object = self.current_dragging_item.create(self.scope)
            object.body.position = mouse_position

            self.current_dragging_item = None

    def on_draw(self, out: pygame.Surface):
        out.blit(self.background_image)

        for entity in self.scope.entities:
            entity.draw(out)
            if IS_DEBUG:
                entity.debug_draw(out)

    def on_draw_interface(self, out: pygame.Surface):
        self.screen_container.draw_all_children(out)

        if self.current_dragging_item != None:
            draw.circle(out, "red", pygame.mouse.get_pos(), 4)


game = TheGame()
game.start()
