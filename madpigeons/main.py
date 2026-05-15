import pygame
import pymunk
from typing import Any, Callable
from pygame import draw, mouse

from game import PhysGame
from ui import UIElement, Label, Frame, Image, UIDim2, Vec2
import objects
import assets


class InventoryItem:
    def __init__(
        self,
        name: str,
        image: pygame.Surface,
        create: Callable[[objects.EntityScope], objects.RigidEntity],
    ) -> None:
        self.name = name
        self.image = image

        self.create_entity = create


HOTBAR: list[InventoryItem] = [
    InventoryItem(
        "Box",
        assets.WOOD_BOX,
        lambda scope: objects.WoodBox(scope, 1),
    ),
    InventoryItem(
        "Ball",
        assets.WOOD_BALL,
        lambda scope: objects.WoodBall(scope, 1),
    ),
    InventoryItem(
        "Thin Plank",
        assets.WOOD_PLANK,
        lambda scope: objects.WoodPlankThin(scope, 1),
    ),
    InventoryItem(
        "Thick Plank",
        assets.WOOD_RECTANGLE,
        lambda scope: objects.WoodPlankThick(scope, 1),
    ),
    InventoryItem(
        "Triangle",
        assets.WOOD_TRIANGLE,
        lambda scope: objects.WoodTriangle(scope, 1),
    ),
    InventoryItem(
        "Wedge",
        assets.WOOD_WEDGE,
        lambda scope: objects.WoodWedge(scope, 1, True),
    ),
    InventoryItem(
        "Pig",
        assets.PIG_SMILING,
        lambda scope: objects.Piggy(scope, 1),
    ),
    InventoryItem(
        "Bird",
        assets.RED_BIRD,
        lambda scope: objects.RedBird(scope),
    ),
]
HOTBAR_SLOT_SIZE = 70


def point_in_body(point: tuple[float, float], body: pymunk.Body):
    for shape in body.shapes:
        if shape.point_query(point).distance <= 0:
            return True


class TheGame(PhysGame):
    window_width = 1000
    window_height = 564
    gravity = 500
    title = "Mad Pigeons™ (not angry birds)"
    icon = assets.RED_BIRD

    def setup(self):
        self.pause_simulation()

        scope = objects.EntityScope(self.space)

        floor_segment = pymunk.Segment(
            self.space.static_body,
            (-1e4, self.window_height * 0.9 + 70),
            (1e4, self.window_height * 0.9 + 70),
            90,
        )
        floor_segment.friction = 0.6
        floor_segment.elasticity = 0.4

        self.space.add(floor_segment)
        self.scope = scope

        self.current_dragging_entity: objects.RigidEntity | None = None

        self.background_image = pygame.transform.scale(
            assets.BACKGROUND_1,
            (self.window_width, self.window_height),
        )

    def setup_ui(self):
        screen_ui_container = UIElement(
            size=UIDim2(self.window_width, self.window_height)
        )

        self.screen_ui_container = screen_ui_container

        # setup hotbar
        hotbar_count = len(HOTBAR)
        hotbar_container = UIElement(
            screen_ui_container,
            size=UIDim2(0, HOTBAR_SLOT_SIZE, 0.6, 0),
            position=UIDim2(0, -5, 0.5, 1),
            anchor_point=Vec2(0.5, 1),
        )

        for index, item in enumerate(HOTBAR):
            frame = Frame(
                hotbar_container,
                Vec2(index / (hotbar_count - 1), 0),
                UIDim2(0, 0, index / (hotbar_count - 1), 0),
                UIDim2(HOTBAR_SLOT_SIZE, HOTBAR_SLOT_SIZE),
            )
            frame.background_color = (0, 0, 0, 80)
            frame._rerender()

            Image(
                frame,
                Vec2(0.5, 0.5),
                UIDim2(0, 0, 0.5, 0.5),
                UIDim2(0, 0, 0.9, 0.9),
                image=item.image,
            )

            name_label = Label(
                frame,
                Vec2(0, 1),
                size=UIDim2(0, 20, 1, 0),
                text=item.name,
                text_color=(0, 0, 0, 255),
            )
            name_label.visible = False

            def on_mouse_down(*_, item=item):
                new_entity = item.create_entity(self.scope)
                new_entity.body.position = mouse.get_pos()
                self.current_dragging_entity = new_entity

            def on_mouse_enter(*_, name_label=name_label):
                name_label.visible = True

            def on_mouse_leave(*_, name_label=name_label):
                name_label.visible = False

            frame.mouse_down.connect(on_mouse_down)
            frame.mouse_enter.connect(on_mouse_enter)
            frame.mouse_leave.connect(on_mouse_leave)

    def collision_handler(
        self, arbiter: pymunk.Arbiter, space: pymunk.Space, data: Any
    ):
        body_1, body_2 = arbiter.bodies

        entity_1 = self.scope.get_entity_from_body(body_1)
        if entity_1 is not None:
            entity_1.on_collision(arbiter)

        entity_2 = self.scope.get_entity_from_body(body_2)
        if entity_2 is not None:
            entity_2.on_collision(arbiter)

    def on_mouse_left_down(self, pos: tuple[int, int]):
        for entity in self.scope.entities:
            if point_in_body(pos, entity.body):
                self.current_dragging_entity = entity
                break

        self.screen_ui_container._on_mouse_down(*pos)

    def on_mouse_left_up(self, pos: tuple[int, int]):
        self.screen_ui_container._on_mouse_up(*pos)

        if self.current_dragging_entity != None:
            self.current_dragging_entity.body.position = pos
            self.current_dragging_entity = None

    def on_mouse_move(self, pos: tuple[int, int]):
        self.screen_ui_container._on_mouse_move(*pos)

    def on_key_down(self, key: str):
        if key == "space":
            if self.is_simulation_running:
                self.pause_simulation()
            else:
                self.resume_simulation()

    def on_update(self, dt: float):
        super().on_update(dt)

        entity = self.current_dragging_entity

        if entity != None:
            body = entity.body
            body.position = mouse.get_pos()
            body.velocity = (0, 0)

    def on_draw_scene(self, out: pygame.Surface):
        out.blit(self.background_image)

        for entity in self.scope.entities:
            entity.draw(out)

    def on_draw_interface(self, out: pygame.Surface):
        self.screen_ui_container.draw_descendants_to_surface(out)


game = TheGame()
game.start()
